import { Link } from "react-router-dom";
import { Brain, ScanSearch, ShieldAlert, Download } from "lucide-react";
import Detector from "../components/Detector";

const STATS = [
  { value: "5,000", label: "ECG heartbeats in the dataset" },
  { value: "140", label: "timesteps per sequence" },
  { value: "2", label: "models: dense and LSTM" },
  { value: "0", label: "anomaly labels used in training" },
];

const STEPS = [
  {
    icon: Brain,
    title: "1. Learn what normal looks like",
    text: "An autoencoder is trained only on normal heartbeats. It learns to compress each beat to a small code and rebuild it.",
  },
  {
    icon: ScanSearch,
    title: "2. Reconstruct new data",
    text: "Each uploaded sequence is passed through the model. Normal beats come back almost unchanged; unusual ones do not.",
  },
  {
    icon: ShieldAlert,
    title: "3. Flag what it cannot explain",
    text: "If the reconstruction error is above a threshold learned from normal data, the sequence is flagged as an anomaly.",
  },
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <span className="hero-badge">
          Self-supervised · No anomaly labels needed
        </span>

        <h1>
          Detect anomalies in time series, without ever labelling one.
        </h1>

        <p>
          DeepAnomaly learns what normal ECG heartbeats look like and flags
          anything it cannot reconstruct. Upload a CSV and see which sequences
          are abnormal, and where.
        </p>

        <div className="hero-actions">
          <a href="#detector" className="btn btn-primary">
            Try the detector
          </a>

          <Link to="/about" className="btn btn-ghost">
            About the project
          </Link>
        </div>
      </section>

      <div className="page">
        <section className="stats-strip">
          {STATS.map((s) => (
            <div key={s.label} className="stat">
              <div className="stat-value">{s.value}</div>
              <div className="stat-label">{s.label}</div>
            </div>
          ))}
        </section>

        <section className="home-section">
          <h2 className="section-title">How it works</h2>

          <div className="steps-grid">
            {STEPS.map((s) => (
              <div key={s.title} className="step-card">
                <s.icon size={22} color="#6366f1" />
                <h3>{s.title}</h3>
                <p>{s.text}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="detector" className="home-section">
          <h2 className="section-title">Try the detector</h2>

          <p className="section-sub">
            Upload a CSV where each row is one sequence of 140 values and there
            is no header. No file handy? Download the sample: 10 normal and 10
            anomalous heartbeats.
          </p>

          <a href="/demo_sequences.csv" download className="sample-link">
            <Download size={16} /> Download sample CSV
          </a>

          <Detector />

          <div className="legend-card">
            <h3>Reading the results</h3>

            <ul>
              <li>
                <span className="dot dot-normal" /> <b>Normal:</b>{" "}
                reconstruction error is below the threshold.
              </li>

              <li>
                <span className="dot dot-anomaly" /> <b>Anomaly:</b> error is
                above the threshold; the model could not rebuild the sequence.
              </li>

              <li>
                <b>Chart:</b> click a row. Where the dashed reconstruction
                departs from the original is the part the model could not
                explain.
              </li>

              <li>
                <b>Compare both:</b> runs the dense and LSTM models on the same
                file and shows where they agree.
              </li>
            </ul>
          </div>
        </section>
      </div>
    </>
  );
}