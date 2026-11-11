import type { DashboardData } from "@studyhub/shared";
import { StatusBadge } from "./ui/StatusBadge";

export function GradesTable({ data }: { data: DashboardData }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <caption style={{ textAlign: "left", fontWeight: 700, padding: "var(--sh-space-1) 0" }}>
        Scores by lab
      </caption>
      <thead>
        <tr>
          <th scope="col" style={{ textAlign: "left" }}>Student</th>
          {data.labs.map((lab) => (
            <th scope="col" key={lab.number} title={lab.title}>Lab {lab.number}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.rows.map((row) => (
          <tr key={row.student} style={{ borderTop: "1px solid var(--sh-border)" }}>
            <th scope="row" style={{ textAlign: "left", fontWeight: 400 }}>{row.student}</th>
            {row.cells.map((cell) => (
              <td key={cell.labNumber} style={{ textAlign: "center", padding: "var(--sh-space-1)" }}>
                <StatusBadge cell={cell} />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
