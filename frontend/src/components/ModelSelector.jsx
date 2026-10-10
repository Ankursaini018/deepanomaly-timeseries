import { MODEL_LABELS } from "../constants";

export default function ModelSelector({
  value,
  onChange,
  available,
  disabled,
}) {
  const options = available.map((m) => ({
    id: m,
    label: MODEL_LABELS[m] ?? m,
  }));

  return (
    <div className="model-selector">
      {options.map((o) => (
        <button
          key={o.id}
          disabled={disabled}
          className={`model-btn ${value === o.id ? "active" : ""}`}
          onClick={() => onChange(o.id)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}