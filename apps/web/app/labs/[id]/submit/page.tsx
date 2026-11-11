"use client";
import { useParams } from "next/navigation";
import { useState } from "react";
import { useSubmitLab } from "../../../../lib/hooks/useSubmitLab";

export default function SubmitPage() {
  const params = useParams<{ id: string }>();
  const labId = Number(params.id);
  const { submit, result, error, pending } = useSubmitLab(labId);
  const [studentId, setStudentId] = useState("1");
  const [file, setFile] = useState<File | null>(null);

  return (
    <main>
      <h1>Submit lab {labId}</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void submit(Number(studentId), file);
        }}
      >
        <p>
          <label htmlFor="student">Student ID (a teaching simplification)</label>
          <br />
          <input id="student" type="number" min={1} value={studentId}
                 onChange={(e) => setStudentId(e.target.value)} required />
        </p>
        <p>
          <label htmlFor="file">Report file (up to 10 MB)</label>
          <br />
          <input id="file" type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </p>
        <button type="submit" disabled={pending}>
          {pending ? "Sending…" : "Submit"}
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
      {result && <p role="status">Accepted: {result.filename} (#{result.id})</p>}
    </main>
  );
}
