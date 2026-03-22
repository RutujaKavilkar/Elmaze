from pathlib import Path
import sys
import gerber_generator as gg
from auto_placer import auto_place_components
from footprints import generate_all_pads, generate_pad_map
from grid_router import Grid, a_star, block_pads, path_to_traces


BASE_OUTPUT_DIR = Path(r"D:\El-Maze\Elmaze\gerber_files")

COMPONENTS = [
    "Power Supply",
    "Resistor",
    "LED",
]


def get_board_dimensions():
    width = float(input("Enter PCB width (in inches): ").strip())
    height = float(input("Enter PCB height (in inches): ").strip())
    return width, height


def get_output_folder() -> Path:
    project_name = input("Enter project name (optional): ").strip()
    output_path = BASE_OUTPUT_DIR / project_name if project_name else BASE_OUTPUT_DIR
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


# =========================
# 🔥 AUTO CONNECTION GENERATOR
# =========================
def generate_all_connections(pad_map):
    connections = []

    components = list(pad_map.keys())

    # connect every component to every other component
    for i in range(len(components)):
        for j in range(i + 1, len(components)):
            comp1 = components[i]
            comp2 = components[j]

            pads1 = pad_map[comp1]
            pads2 = pad_map[comp2]

            # connect ALL pads of comp1 to ALL pads of comp2
            for p1 in range(len(pads1)):
                for p2 in range(len(pads2)):
                    connections.append(((comp1, p1), (comp2, p2)))

    return connections


# =========================
# 🔥 GRID ROUTER (FULL LOOP)
# =========================
def generate_traces_auto(pad_map, width, height):
    print("🧠 Auto-routing ALL footprint connections...")

    grid = Grid(width, height, resolution=0.1)

    # block pads
    all_pads = []
    for pads in pad_map.values():
        all_pads.extend(pads)

    block_pads(grid, all_pads, radius=0)

    print(f"Grid: {grid.cols} x {grid.rows}")
    print(f"Blocked cells: {len(grid.blocked)}")

    # 🔥 generate all connections
    connections = generate_all_connections(pad_map)

    print(f"Total connections: {len(connections)}")

    traces = []

    for (comp1, p1), (comp2, p2) in connections:

        start = grid.to_grid(*pad_map[comp1][p1])
        end = grid.to_grid(*pad_map[comp2][p2])

        # temp grid (important)
        temp_grid = Grid(width, height, grid.resolution)
        temp_grid.blocked = set(grid.blocked)

        temp_grid.blocked.discard(start)
        temp_grid.blocked.discard(end)

        path = a_star(temp_grid, start, end)

        if not path:
            print(f"⚠️ Skipped: {comp1}[{p1}] → {comp2}[{p2}]")
            continue

        traces.extend(path_to_traces(grid, path))

        # block path with clearance
        for node in path:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    grid.blocked.add((node[0] + dx, node[1] + dy))

    return traces


def generate_silkscreen(component_positions):
    return [(x + 0.2, y + 0.2) for x, y in component_positions.values()]


# =========================
# MAIN LOGIC
# =========================
def generate_pcb(output_path: Path, width: float, height: float):

    print("📍 Auto-placing components...")
    component_positions = auto_place_components(COMPONENTS, width, height)

    pad_map = generate_pad_map(component_positions)
    pads = generate_all_pads(component_positions)

    # 🔥 NEW AUTO ROUTING
    traces = generate_traces_auto(pad_map, width, height)

    silkscreen = generate_silkscreen(component_positions)

    print("⚙️ Generating Gerbers...")

    gg.generate_top_layer(pads, traces, output_path)
    gg.generate_board_outline(width, height, output_path)
    gg.generate_drill_file(pads, output_path)
    gg.generate_silkscreen(silkscreen, output_path)

    print(f"\n✅ Done: {output_path.resolve()}")


def main():
    try:
        print("\n🛠 PCB Generator (Auto Full Connectivity Routing)\n")

        out = get_output_folder()
        w, h = get_board_dimensions()

        generate_pcb(out, w, h)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()