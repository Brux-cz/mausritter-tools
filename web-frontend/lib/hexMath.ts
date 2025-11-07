/**
 * Hex Grid Math Library
 * Handles coordinate transformations for a pointy-top hexagon grid
 */

// Pointy-top hexagon constants
const HEX_RADIUS = 60; // px (distance from center to corner)

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
  // Pointy-top hexagon formulas
  const x = HEX_RADIUS * (Math.sqrt(3) * q + (Math.sqrt(3) / 2) * r);
  const y = HEX_RADIUS * ((3 / 2) * r);
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
    const angle = (Math.PI / 3) * i; // 60 degrees between points
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
  col: number;
  row: number;
  x: number;
  y: number;
}

/**
 * Classic 19-hex pattern (spiral from center)
 * Pattern matches traditional Mausritter hex map:
 *       8
 *     19  9
 *   18  2  10
 *  7  1  3  11
 * 17  6  4  12
 *  16  5  13
 *    15 14
 */
export function get19HexLayout(): HexLayout[] {
  const axialCoords = [
    // Center hex #1
    { q: 0, r: 0 },    // #1 (center)

    // Ring 1: 6 hexes around center (clockwise from top)
    { q: 0, r: -1 },   // #2 (top)
    { q: 1, r: -1 },   // #3 (top-right)
    { q: 1, r: 0 },    // #4 (right)
    { q: 0, r: 1 },    // #5 (bottom-right)
    { q: -1, r: 1 },   // #6 (bottom-left)
    { q: -1, r: 0 },   // #7 (left)

    // Ring 2: 12 hexes (clockwise from top)
    { q: 0, r: -2 },   // #8 (top)
    { q: 1, r: -2 },   // #9 (top-right)
    { q: 2, r: -2 },   // #10 (top-right-right)
    { q: 2, r: -1 },   // #11 (right-top)
    { q: 2, r: 0 },    // #12 (right)
    { q: 1, r: 1 },    // #13 (right-bottom)
    { q: 0, r: 2 },    // #14 (bottom-right)
    { q: -1, r: 2 },   // #15 (bottom)
    { q: -2, r: 2 },   // #16 (bottom-left-left)
    { q: -2, r: 1 },   // #17 (left-bottom)
    { q: -2, r: 0 },   // #18 (left)
    { q: -1, r: -1 },  // #19 (left-top)
  ];

  return axialCoords.map(({ q, r }) => {
    const { x, y } = axialToScreen(q, r);
    return { col: q, row: r, x, y };
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
