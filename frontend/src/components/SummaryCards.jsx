import { AlertTriangle, CheckCircle, Activity } from "lucide-react";

export default function SummaryCards({ results }) {
  const { total, anomalies_found } = results;
  const normalCount = total - anomalies_found;
  const anomalyRate = ((anomalies_found / total) * 100).toFixed(1);

  const cards = [
    { label: "Total Sequences", value: total, icon: Activity, color: "#6366f1" },
    { label: "Normal", value: normalCount, icon: CheckCircle, color: "#22c55e" },
    { label: "Anomalies", value: anomalies_found, icon: AlertTriangle, color: "#ef4444" },
    { label: "Anomaly Rate", value: `${anomalyRate}%`, icon: AlertTriangle, color: "#f59e0b" },
  ];

  return (
    <div className="summary-grid">
      {cards.map((c) => (
        <div key={c.label} className="summary-card">
          <c.icon size={20} color={c.color} />
          <div>
            <div className="summary-value">{c.value}</div>
            <div className="summary-label">{c.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}