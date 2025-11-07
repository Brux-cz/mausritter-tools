/**
 * Hex Grid Math Library
 * Handles coordinate transformations for a pointy-top hexagon grid
 */

// Pointy-top hexagon constants
const HEX_RADIUS = 30; // px (distance from center to corner)

export interface HexCoord {
  q: number; // Axial coordinate (cube x)
  r: number; // Axial coordinate (cube z)
}

export interface ScreenCoord {
  x: number;
  y: number;
}

/**
 * Convert offset coordinates (col, row) to axial coordinates (q, r)
 * Using "odd-r" horizontal layout (odd rows shifted right)
 * @param col Column index (0-4 for 5x5 grid)
 * @param row Row index (0-4 for 5x5 grid)
 */
export function offsetToAxial(col: number, row: number): HexCoord {
  const q = col - (row - (row & 1)) / 2;
  const r = row;
  return { q, r };
}

/**
 * Convert axial coordinates to screen coordinates
 * Pointy-top orientation (hexagons with points up/down)
 * @param q Axial q coordinate (column-like)
 * @param r Axial r coordinate (row-like)
 */
export function axialToScreen(q: number, r: number): ScreenCoord {
  // Constants for Pointy-Top conversion
  const SQRT_3 = Math.sqrt(3);

  // x = R * (sqrt(3) * q + (sqrt(3) / 2) * r)
  const x = HEX_RADIUS * (SQRT_3 * q + (SQRT_3 / 2) * r);
  // y = R * (3 / 2) * r
  const y = HEX_RADIUS * ((3 / 2) * r);

  // Tato funkce vrací souřadnice RELATIVNÍ ke středu mřížky (0,0).
  // Při vykreslování v SVG/Canvasu MUSÍTE posunout (x, y) o polovinu šířky/výšky Viewportu.
  return { x, y };
}

/**
 * Convert offset grid position to screen coordinates (combines above)
 * @param col Column index
 * @param row Row index
 */
export function offsetToScreen(col: number, row: number): ScreenCoord {
  const axial = offsetToAxial(col, row);
  return axialToScreen(axial.q, axial.r);
}

/**
 * Calculate SVG viewBox dimensions for a hex grid
 * @param cols Number of columns (default: 5)
 * @param rows Number of rows (default: 5)
 */
export function getGridViewBox(cols: number = 5, rows: number = 5) {
  const padding = 80;
  const width = HEX_RADIUS * 3 * (cols / 2) + HEX_RADIUS + padding;
  const height = HEX_RADIUS * Math.sqrt(3) * (rows + 0.5) + padding;

  return {
    minX: -padding / 2,
    minY: -padding / 2,
    width,
    height,
    viewBox: `${-padding / 2} ${-padding / 2} ${width} ${height}`,
  };
}

/**
 * Generate SVG polygon points for a hexagon centered at (centerX, centerY)
 * @param centerX Center X coordinate
 * @param centerY Center Y coordinate
 * @returns Space-separated points string for SVG polygon
 */
export function hexagonPoints(centerX: number, centerY: number): string {
  const points: string[] = [];
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 3) * i - Math.PI / 6; // Posun pro Pointy-Top
    const px = centerX + HEX_RADIUS * Math.cos(angle);
    const py = centerY + HEX_RADIUS * Math.sin(angle);
    points.push(`${px},${py}`);
  }
  return points.join(" ");
}

/**
 * Check if a point is inside a hexagon
 * @param point Screen point to test
 * @param center Hexagon center
 * @returns True if point is inside hexagon
 */
export function isPointInHexagon(
  point: ScreenCoord,
  center: ScreenCoord
): boolean {
  const dx = point.x - center.x;
  const dy = point.y - center.y;
  const distance = Math.sqrt(dx * dx + dy * dy);
  return distance <= HEX_RADIUS;
}

/**
 * Get neighboring hex coordinates (6 neighbors for any hex)
 * @param col Column index
 * @param row Row index
 * @returns Array of neighbor coordinates (may include out-of-bounds)
 */
export function getNeighbors(
  col: number,
  row: number
): Array<{ col: number; row: number }> {
  const isOddRow = row % 2 === 1;
  const neighbors = [
    { col: col, row: row - 1 }, // Top
    { col: col, row: row + 1 }, // Bottom
    { col: col - 1, row: row }, // Left
    { col: col + 1, row: row }, // Right
    // Diagonal neighbors depend on odd/even row
    {
      col: isOddRow ? col + 1 : col - 1,
      row: row - 1,
    }, // Top diagonal
    {
      col: isOddRow ? col + 1 : col - 1,
      row: row + 1,
    }, // Bottom diagonal
  ];

  // Filter out-of-bounds (for 5x5 grid)
  return neighbors.filter(
    (n) => n.col >= 0 && n.col < 5 && n.row >= 0 && n.row < 5
  );
}

/**
 * Generate hexagon-shaped layout for variable number of hexes
 * Returns array of {col, row, x, y} for each hex index
 */
export interface HexLayout {
  col: number; // Axial q
  row: number; // Axial r
  x: number;
  y: number;
  label?: number;
}

/**
 * 19-hexagonový klastr ve tvaru květu (plástve): 1 hex uprostřed, 6 vnitřní prstenec, 12 vnější prstenec.
 */
export function get19HexLayout(): HexLayout[] {
  const axialCoords = [
    // Střed
    { q: 0, r: 0, label: 1 },

    // Vnitřní prstenec (přímí sousedé centra)
    { q: -1, r: 0, label: 2 },
    { q: 0, r: -1, label: 3 },
    { q: 1, r: -1, label: 4 },
    { q: 1, r: 0, label: 5 },
    { q: 0, r: 1, label: 6 },
    { q: -1, r: 1, label: 7 },

    // Vnější prstenec (hexagony ve vzdálenosti 2 od centra)
    { q: -2, r: 0, label: 8 },
    { q: -1, r: -1, label: 9 },
    { q: 0, r: -2, label: 10 },
    { q: 1, r: -2, label: 11 },
    { q: 2, r: -2, label: 12 },
    { q: 2, r: -1, label: 13 },
    { q: 2, r: 0, label: 14 },
    { q: 1, r: 1, label: 15 },
    { q: 0, r: 2, label: 16 },
    { q: -1, r: 2, label: 17 },
    { q: -2, r: 2, label: 18 },
    { q: -2, r: 1, label: 19 },
  ];

  return axialCoords.map(({ q, r, label }) => {
    const { x, y } = axialToScreen(q, r);
    return { col: q, row: r, x, y, label };
  });
}

/**
 * 25-hex layout for hexcrawl generator (5x5 grid pattern)
 */
export function get25HexLayout(): HexLayout[] {
  const axialCoords = [
    // Row r=-2 (top, 3 hexes)
    { q: 0, r: -2 },   // #1
    { q: 1, r: -2 },   // #2
    { q: 2, r: -2 },   // #3

    // Row r=-1 (4 hexes)
    { q: -1, r: -1 },  // #4
    { q: 0, r: -1 },   // #5
    { q: 1, r: -1 },   // #6
    { q: 2, r: -1 },   // #7

    // Row r=0 (center, 5 hexes)
    { q: -2, r: 0 },   // #8
    { q: -1, r: 0 },   // #9
    { q: 0, r: 0 },    // #10 (center)
    { q: 1, r: 0 },    // #11
    { q: 2, r: 0 },    // #12

    // Row r=1 (4 hexes)
    { q: -1, r: 1 },   // #13
    { q: 0, r: 1 },    // #14
    { q: 1, r: 1 },    // #15
    { q: 2, r: 1 },    // #16

    // Row r=2 (3 hexes)
    { q: 0, r: 2 },    // #17
    { q: 1, r: 2 },    // #18
    { q: 2, r: 2 },    // #19

    // Row r=3 (3 hexes)
    { q: 0, r: 3 },    // #20
    { q: 1, r: 3 },    // #21
    { q: 2, r: 3 },    // #22

    // Row r=4 (bottom, 3 hexes)
    { q: 0, r: 4 },    // #23
    { q: 1, r: 4 },    // #24
    { q: 2, r: 4 },    // #25
  ];

  return axialCoords.map(({ q, r }) => {
    const { x, y } = axialToScreen(q, r);
    return { col: q, row: r, x, y };
  });
}

/**
 * Default layout function (for backwards compatibility)
 * Uses 19-hex layout for standalone map generator
 * Note: HexMap component for hexcrawl still explicitly uses get25HexLayout()
 */
export function getHexagonLayout(): HexLayout[] {
  return get19HexLayout();
}
