import type { Lab } from "@studyhub/shared";

// The single point of access to the API: components -> hooks -> lib/api.ts -> types from packages/shared.
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function apiGet<T>(path: string): Promise<T> {
  const resp = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!resp.ok) throw new Error(`GET ${path}: ${resp.status}`);
  return (await resp.json()) as T;
}

export const fetchLabs = () => apiGet<Lab[]>("/labs");
