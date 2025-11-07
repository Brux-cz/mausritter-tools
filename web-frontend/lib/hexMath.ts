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
 * Pointy-top orientation
 * @param q Axial q coordinate
 * @param r Axial r coordinate
 */
export function axialToScreen(q: number, r: number): ScreenCoord {
  const x = HEX_RADIUS * ((3 / 2) * q);
  const y = HEX_RADIUS * ((Math.sqrt(3) / 2) * q + Math.sqrt(3) * r);
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
 * Generate hexagon-shaped layout for 25 hexes (centered pattern)
 * Pattern: 3-4-5-4-3-3-3 rows (total 25)
 * Returns array of {col, row, centerX, centerY} for each hex index
 */
export interface HexLayout {
  col: number;
  row: number;
  x: number;
  y: number;
}

export function getHexagonLayout(): HexLayout[] {
  // Hexagon shape pattern (row: [start_col, num_hexes])
  // Adjusted for 25 hexes total in diamond/hexagon shape
  const pattern = [
    { row: 0, startCol: 1, count: 3 },  // Top: 3 hexes (indices 0-2)
    { row: 1, startCol: 0.5, count: 4 },  // 4 hexes (indices 3-6)
    { row: 2, startCol: 0, count: 5 },    // Center: 5 hexes (indices 7-11)
    { row: 3, startCol: 0.5, count: 4 },  // 4 hexes (indices 12-15)
    { row: 4, startCol: 1, count: 3 },  // 3 hexes (indices 16-18)
    { row: 5, startCol: 1, count: 3 },  // 3 hexes (indices 19-21)
    { row: 6, startCol: 1, count: 3 },  // Bottom: 3 hexes (indices 22-24)
  ];

  const layout: HexLayout[] = [];
  let hexIndex = 0;

  for (const { row, startCol, count } of pattern) {
    for (let i = 0; i < count; i++) {
      const col = startCol + i;
      const { x, y } = offsetToScreen(col, row);
      layout.push({ col, row, x, y });
      hexIndex++;
      if (hexIndex >= 25) break;
    }
    if (hexIndex >= 25) break;
  }

  return layout;
}
