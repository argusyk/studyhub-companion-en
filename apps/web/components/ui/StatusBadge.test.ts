import { describe, expect, it } from "vitest";
import { badgeFor } from "./StatusBadge";

describe("badgeFor", () => {
  it("shows text for every non-plain status", () => {
    expect(badgeFor({ labNumber: 1, score: null, status: "missing", isLate: false })?.text).toBe("Not submitted");
    expect(badgeFor({ labNumber: 1, score: 56, status: "reviewed", isLate: true })?.text).toBe("Late: 56");
  });
  it("returns null for a normal graded cell", () => {
    expect(badgeFor({ labNumber: 1, score: 90, status: "reviewed", isLate: false })).toBeNull();
  });
});
