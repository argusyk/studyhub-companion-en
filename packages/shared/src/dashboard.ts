import example from "./dashboard.example.json";

export type CellStatus = "submitted" | "reviewed" | "returned" | "missing";

export interface DashboardCell {
  labNumber: number;
  score: number | null;
  status: CellStatus;
  isLate: boolean;
}

export interface DashboardData {
  group: string;
  labs: { number: number; title: string }[];
  rows: { student: string; cells: DashboardCell[] }[];
  stats: { average: number; submitted: number; total: number; late: number };
}

// Teaching data for Lab 8 (there is no group statistics endpoint yet).
export const dashboardExample = example as DashboardData;
