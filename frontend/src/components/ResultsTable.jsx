export default function ResultsTable({ results }) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Reconstruction Error</th>
            <th>Threshold</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={i} className={r.is_anomaly ? "row-anomaly" : ""}>
              <td>{i + 1}</td>
              <td>{r.reconstruction_error.toFixed(6)}</td>
              <td>{r.threshold.toFixed(6)}</td>
              <td>
                <span className={`badge ${r.is_anomaly ? "badge-anomaly" : "badge-normal"}`}>
                  {r.is_anomaly ? "Anomaly" : "Normal"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}