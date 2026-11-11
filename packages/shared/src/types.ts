// Shared API types (a mirror of the FastAPI schemas in apps/api/app/schemas).
export interface Lab {
  id: number;
  number: number;
  title: string;
  deadline: string; // ISO 8601, UTC
  max_score: number;
}

export type SubmissionStatus = "submitted" | "reviewed" | "returned";

export interface Submission {
  id: number;
  student_id: number;
  lab_id: number;
  submitted_at: string; // ISO 8601, UTC
  file_url: string;
  filename: string;
  size_bytes: number;
  status: SubmissionStatus;
  score: number | null;
  is_late?: boolean; // appears in Chapter 10
}
