from pathlib import Path
from typing import List, Tuple

# =========================
# Global PCB Settings
# =========================
PRECISION = "FSLAX24Y24"
UNITS = "MOIN"  # Inches
SCALE_FACTOR = 1000  # Coordinate scaling

DEFAULT_TRACE_WIDTH = 0.010  # 10 mil (~0.25 mm)


# =========================
# Types
# =========================
Point = Tuple[float, float]
Trace = Tuple[Point, Point]


# =========================
# Utility Functions
# =========================
def _format_coord(x: float, y: float) -> str:
    """Convert coordinates into Gerber format."""
    return f"X{int(x * SCALE_FACTOR)}Y{int(y * SCALE_FACTOR)}"


def _ensure_folder(folder: Path) -> None:
    """Ensure output directory exists."""
    folder.mkdir(parents=True, exist_ok=True)


def write_gerber_file(filename: str, content: str, folder: Path) -> None:
    """Write Gerber content to file."""
    _ensure_folder(folder)
    filepath = folder / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Generated: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Failed to write {filename}: {e}")


# =========================
# Gerber Generators
# =========================
def generate_top_layer(
    pads: List[Point],
    traces: List[Trace],
    folder: Path,
    trace_width: float = DEFAULT_TRACE_WIDTH
) -> None:
    """Generate top copper layer (GTL)."""

    if not pads:
        raise ValueError("Pads list cannot be empty")

    if trace_width <= 0:
        raise ValueError("Trace width must be positive")

    content = f"""G04 Top Copper Layer*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD10C,0.062*%
%ADD11C,{trace_width:.3f}*%
G54D10*
"""

    # Pads (flash)
    for x, y in pads:
        content += f"{_format_coord(x, y)}D03*\n"

    # Traces
    content += "G54D11*\nD11*\n"
    for (x1, y1), (x2, y2) in traces:
        content += f"{_format_coord(x1, y1)}D02*\n"
        content += f"{_format_coord(x2, y2)}D01*\n"

    content += "M02*\n"

    write_gerber_file("top_layer.gtl", content, folder)


def generate_board_outline(
    width: float,
    height: float,
    folder: Path
) -> None:
    """Generate board outline (GKO)."""

    if width <= 0 or height <= 0:
        raise ValueError("Board dimensions must be positive")

    content = f"""G04 Board Outline*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD10C,0.020*%
G54D10*
D10*
X0Y0D02*
{_format_coord(width, 0)}D01*
{_format_coord(width, height)}D01*
{_format_coord(0, height)}D01*
X0Y0D01*
M02*
"""

    write_gerber_file("board_outline.gko", content, folder)


def generate_drill_file(
    holes: List[Point],
    folder: Path
) -> None:
    """Generate drill file (DRL)."""

    if not holes:
        raise ValueError("Drill holes list cannot be empty")

    content = """M48
INCH,TZ
T1C0.0315
%
T1
"""

    for x, y in holes:
        content += f"{_format_coord(x, y)}\n"

    content += "M30\n"

    write_gerber_file("drill_through.drl", content, folder)


def generate_silkscreen(
    positions: List[Point],
    folder: Path
) -> None:
    """Generate top silkscreen layer (GTO)."""

    if not positions:
        raise ValueError("Silkscreen positions cannot be empty")

    content = f"""G04 Top Silkscreen*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD12C,0.030*%
G54D12*
D12*
"""

    for x, y in positions:
        content += f"{_format_coord(x, y)}D02*\n"

    content += "M02*\n"

    write_gerber_file("top_silkscreen.gto", content, folder)