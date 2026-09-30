import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from "recharts";

export default function ReconstructionChart({ original, reconstructed }) {
  const data = original.map((val, i) => ({
    time: i,
    original: val,
    reconstructed: reconstructed[i],
  }));

  return (
    <div className="chart-card">
      <h3>Original vs Reconstructed</h3>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2d3a" />
          <XAxis dataKey="time" stroke="#6b7280" tick={{ fontSize: 11 }} />
          <YAxis stroke="#6b7280" tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{ background: "#1a1d2e", border: "1px solid #2a2d3a" }}
          />
          <Legend />
          <Line type="monotone" dataKey="original" stroke="#6366f1" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="reconstructed" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="4 4" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}