import { MODEL_LABELS, MODEL_ORDER } from "../constants";

export default function ComparisonPanel({ resultsByModel, selectedIndex, onSelectRow }) {
  const names = MODEL_ORDER.filter((n) => resultsByModel[n]);
  if (names.length < 2) return null;

  const total = resultsByModel[names[0]].total;
  const [a, b] = names;

  const agreement = resultsByModel[a].results.filter(
    (r, i) => r.is_anomaly === resultsByModel[b].results[i].is_anomaly
  ).length;

  const meanError = (n) =>
    resultsByModel[n].results.reduce((s, r) => s + r.reconstruction_error, 0) / total;

  return (
    <>
      <div className="compare-grid">
        {names.map((n) => (
          <div key={n} className="summary-card compare-card">
            <div>
              <div className="summary-label">{MODEL_LABELS[n]}</div>
              <div className="summary-value">
                {resultsByModel[n].anomalies_found} / {total} flagged
              </div>
              <div className="summary-label">mean error {meanError(n).toFixed(5)}</div>
            </div>
          </div>
        ))}
        <div className="summary-card compare-card">
          <div>
            <div className="summary-label">Models agree on</div>
            <div className="summary-value">
              {agreement} / {total}
            </div>
            <div className="summary-label">{((agreement / total) * 100).toFixed(1)}% agreement</div>
          </div>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>#</th>
              {names.map((n) => (
                <th key={n}>{MODEL_LABELS[n]}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {resultsByModel[a].results.map((_, i) => (
              <tr
                key={i}
                className={selectedIndex === i ? "row-selected" : ""}
                onClick={() => onSelectRow(i)}
              >
                <td>{i + 1}</td>
                {names.map((n) => {
                  const r = resultsByModel[n].results[i];
                  return (
                    <td key={n}>
                      {r.reconstruction_error.toFixed(5)}{" "}
                      <span className={`badge ${r.is_anomaly ? "badge-anomaly" : "badge-normal"}`}>
                        {r.is_anomaly ? "Anomaly" : "Normal"}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}