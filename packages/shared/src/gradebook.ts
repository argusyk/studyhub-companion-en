// Ported from legacy/static/js/gradebook.js (Lab 10, step 4) preserving the behavior.

/** Warning (Questionable: yes): the denominator includes empty (null) scores, as in legacy. */
export function average(grades: Array<number | null>): number {
  let sum = 0;
  for (const g of grades) {
    if (g !== null) sum += g;
  }
  return grades.length ? Math.round((sum / grades.length) * 10) / 10 : 0;
}

export function lateBadge(days: number): string {
  if (days === 0) return "";
  if (days > 5) return "Not accepted";
  return `Late by ${days} d.`;
}

export function formatScore(x: number | null): string {
  return x === null ? "–" : String(x);
}
