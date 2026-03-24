from pathlib import Path
import sys
import gerber_generator as gg
from auto_placer import auto_place_components
from footprints import generate_all_pads, generate_pad_map


# =========================
# Configuration
# =========================
BASE_OUTPUT_DIR = Path(r"../output")

COMPONENTS = [
    "Power Supply",
    "Resistor",
    "LED",
]

# ✅ PIN-LEVEL CONNECTIONS
PIN_CONNECTIONS = [
    (("Power Supply", 0), ("Resistor", 0)),
    (("Resistor", 1), ("LED", 0)),
    (("LED", 1), ("Power Supply", 1)),
]


# =========================
# Input Functions
# =========================
def get_board_dimensions():
    try:
        width = float(input("Enter PCB width (in inches): ").strip())
        height = float(input("Enter PCB height (in inches): ").strip())

        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive numbers")

        return width, height

    except ValueError as e:
        raise ValueError(f"Invalid input for PCB dimensions: {e}")


def get_output_folder() -> Path:
    project_name = input("Enter project name (optional): ").strip()

    output_path = BASE_OUTPUT_DIR / project_name if project_name else BASE_OUTPUT_DIR

    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create folder: {e}")

    return output_path


# =========================
# Utility Functions
# =========================
def validate_connections(components, pin_connections):
    for (comp1, _), (comp2, _) in pin_connections:
        if comp1 not in components:
            raise ValueError(f"Invalid component: {comp1}")
        if comp2 not in components:
            raise ValueError(f"Invalid component: {comp2}")


def generate_traces_from_pins(pad_map, pin_connections):
    """
    Improved routing:
    - Separate routing corridors
    - Avoid shared paths
    """

    traces = []
    used_segments = []

    def segment_intersects(seg1, seg2):
        (x1, y1), (x2, y2) = seg1
        (x3, y3), (x4, y4) = seg2

        if x1 == x2 and x3 == x4:
            return x1 == x3 and not (max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2))
        if y1 == y2 and y3 == y4:
            return y1 == y3 and not (max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2))

        return False

    def is_valid(path):
        for seg in path:
            for used in used_segments:
                if segment_intersects(seg, used):
                    return False
        return True

    base_offset = 0.3  # BIGGER spacing between nets

    for i, ((comp1, pad1), (comp2, pad2)) in enumerate(pin_connections):

        start = pad_map[comp1][pad1]
        end = pad_map[comp2][pad2]

        x1, y1 = start
        x2, y2 = end

        success = False

        # Give each net its own routing "lane"
        offset = (i + 1) * base_offset

        for attempt in range(5):
            extra = attempt * 0.1

            # Strategy 1: go UP first then across
            mid1 = (x1, y1 + offset + extra)
            mid2 = (x2, y1 + offset + extra)

            path1 = [
                (start, mid1),
                (mid1, mid2),
                (mid2, end)
            ]

            if is_valid(path1):
                traces.extend(path1)
                used_segments.extend(path1)
                success = True
                break

            # Strategy 2: go RIGHT first then down
            mid1 = (x1 + offset + extra, y1)
            mid2 = (x1 + offset + extra, y2)

            path2 = [
                (start, mid1),
                (mid1, mid2),
                (mid2, end)
            ]

            if is_valid(path2):
                traces.extend(path2)
                used_segments.extend(path2)
                success = True
                break

        if not success:
            # fallback simple L
            fallback = [(start, (x2, y1)), ((x2, y1), end)]
            traces.extend(fallback)
            used_segments.extend(fallback)

    return traces

def generate_silkscreen(component_positions):
    return [(x + 0.2, y + 0.2) for x, y in component_positions.values()]


# =========================
# Main Logic
# =========================
def generate_pcb(output_path: Path, width: float, height: float):

    print("📍 Auto-placing components...")
    component_positions = auto_place_components(COMPONENTS, width, height)

    print("🔍 Validating design...")
    validate_connections(component_positions, PIN_CONNECTIONS)

    print("📐 Preparing layout data...")

    pad_map = generate_pad_map(component_positions)
    pads = generate_all_pads(component_positions)
    holes = pads

    # ✅ FIXED: true pin-to-pin routing
    traces = generate_traces_from_pins(pad_map, PIN_CONNECTIONS)

    silkscreen = generate_silkscreen(component_positions)

    print("⚙️ Generating Gerber files...")

    gg.generate_top_layer(pads, traces, output_path)
    gg.generate_board_outline(width, height, output_path)
    gg.generate_drill_file(holes, output_path)
    gg.generate_silkscreen(silkscreen, output_path)

    print(f"\n✅ Gerber files generated successfully in: {output_path.resolve()}")


# =========================
# Entry Point
# =========================
def main():
    try:
        print("\n🛠 PCB Generator\n")

        output_path = get_output_folder()
        pcb_width, pcb_height = get_board_dimensions()

        generate_pcb(output_path, pcb_width, pcb_height)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()