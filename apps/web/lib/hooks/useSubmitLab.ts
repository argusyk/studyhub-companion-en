"use client";
import { useState } from "react";
import type { Submission } from "@studyhub/shared";
import { MAX_UPLOAD_BYTES } from "@studyhub/shared";
import { submitLab } from "../api";

export function validateFile(file: File | null): string | null {
  if (!file) return "Choose a file";
  if (file.size === 0) return "The file is empty";
  if (file.size > MAX_UPLOAD_BYTES) return "File is larger than 10 MB";
  return null;
}

export function useSubmitLab(labId: number) {
  const [result, setResult] = useState<Submission | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function submit(studentId: number, file: File | null) {
    const problem = validateFile(file);
    if (problem) return setError(problem);
    setPending(true);
    setError(null);
    try {
      setResult(await submitLab(labId, studentId, file as File));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error");
    } finally {
      setPending(false);
    }
  }
  return { submit, result, error, pending };
}
