import { describe, expect, it } from "vitest";
import { average, formatScore, lateBadge } from "@studyhub/shared";

describe("gradebook (characterization tests of the ported JS)", () => {
  it("average keeps legacy denominator including nulls", () => {
    expect(average([80, null, 100])).toBe(60);
    expect(average([])).toBe(0);
  });
  it("lateBadge", () => {
    expect(lateBadge(0)).toBe("");
    expect(lateBadge(2)).toBe("Late by 2 d.");
    expect(lateBadge(6)).toBe("Not accepted");
  });
  it("formatScore", () => {
    expect(formatScore(null)).toBe("–");
    expect(formatScore(76)).toBe("76");
  });
});
