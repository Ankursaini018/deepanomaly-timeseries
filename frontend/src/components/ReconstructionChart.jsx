import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import { MODEL_COLORS, MODEL_LABELS } from "../constants";

export default function ReconstructionChart({
  original,
  reconstructions,
}) {
  const names = Object.keys(reconstructions);

  const data = original.map((val, i) => {
    const row = {
      time: i,
      original: val,
    };

    names.forEach((n) => {
      row[n] = reconstructions[n][i];
    });

    return row;
  });

  return (
    <div className="chart-card">
      <h3>Original vs Reconstructed</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#2a2d3a"
          />

          <XAxis
            dataKey="time"
            stroke="#6b7280"
            tick={{ fontSize: 11 }}
          />

          <YAxis
            stroke="#6b7280"
            tick={{ fontSize: 11 }}
          />

          <Tooltip
            contentStyle={{
              background: "#1a1d2e",
              border: "1px solid #2a2d3a",
            }}
          />

          <Legend />

          <Line
            type="monotone"
            dataKey="original"
            name="Original"
            stroke="#6366f1"
            strokeWidth={2}
            dot={false}
          />

          {names.map((n) => (
            <Line
              key={n}
              type="monotone"
              dataKey={n}
              name={`${MODEL_LABELS[n] ?? n} (reconstructed)`}
              stroke={MODEL_COLORS[n] ?? "#f59e0b"}
              strokeWidth={2}
              dot={false}
              strokeDasharray="4 4"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}