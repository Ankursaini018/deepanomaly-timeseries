import { ArrowRight } from "lucide-react";
import metrics from "../data/metrics.json";
import { MODEL_LABELS, REPO_URL } from "../constants";

const PIPELINE = [
  "ECG5000 dataset",
  "Preprocess (normal-only train split)",
  "Train autoencoders",
  "Model artifacts",
  "FastAPI inference",
  "React dashboard",
];

const TECH = [
  { group: "Machine learning", items: ["PyTorch", "scikit-learn", "NumPy", "Pandas"] },
  { group: "Backend", items: ["FastAPI", "Pydantic", "Uvicorn", "Docker"] },
  { group: "Frontend", items: ["React", "Vite", "Recharts", "React Router"] },
  { group: "Deployment", items: ["Railway", "GitHub"] },
];

const LIMITATIONS = [
  "Evaluated on a single dataset (ECG5000), which is relatively easy; results may not transfer to noisier industrial sensors.",
  "The 95th-percentile threshold fixes the false-alarm rate on normal data at about 5% by design. Real systems should tune it to the cost of a false alarm.",
  "The model detects that a sequence is abnormal, not which type of abnormality it is.",
  "Input is a single signal (univariate). Multivariate data such as NASA Turbofan is future work.",
];

const COLUMNS = [
  ["precision", "Precision"],
  ["recall", "Recall"],
  ["f1", "F1"],
  ["roc_auc", "ROC-AUC"],
  ["pr_auc", "PR-AUC"],
  ["false_positive_rate", "False alarm rate"],
];

export default function About() {
  return (
    <div className="page about">
      <header className="about-hero">
        <h1>About DeepAnomaly</h1>
        <p>
          A final-year B.Tech project on detecting anomalies in time series
          without labelled anomalies, built end to end: model, API, and
          dashboard.
        </p>
      </header>

      <section className="about-section">
        <h2>The problem</h2>
        <p>
          Sensors and medical devices produce continuous signals. Rarely, those
          signals contain abnormal patterns: a machine about to fail, a
          cardiac arrhythmia. Labelling such events by hand is slow and
          expensive, and abnormal events are so rare and varied that a
          supervised classifier rarely has enough examples to learn from.
        </p>
      </section>

      <section className="about-section">
        <h2>The approach</h2>
        <p>
          An <b>autoencoder</b> is a neural network that compresses its input
          into a small code and then rebuilds the original from that code. We
          train it only on <b>normal</b> sequences, so it becomes good at
          rebuilding normal patterns and poor at rebuilding anything else. The
          gap between input and reconstruction, the <b>reconstruction error</b>,
          is the anomaly score.
        </p>
        <p>
          The decision threshold is the 95th percentile of error on a held-out
          validation set that contains normal data only. No anomaly labels and
          no test data are used to fit it.
        </p>
      </section>

      <section className="about-section">
        <h2>System pipeline</h2>
        <div className="pipeline">
          {PIPELINE.map((step, i) => (
            <div key={step} className="pipeline-item">
              <div className="pipe-box">{step}</div>
              {i < PIPELINE.length - 1 && (
                <ArrowRight size={18} className="pipe-arrow" />
              )}
            </div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h2>The two models</h2>
        <div className="model-grid">
          <div className="model-card">
            <h3>Dense autoencoder</h3>
            <p>
              Treats the 140 timesteps as a flat vector and compresses it
              through fully connected layers (140 → 128 → 64 → 32 → 16). Fast
              to train, but has no built-in notion of timestep order.
            </p>
          </div>

          <div className="model-card">
            <h3>LSTM autoencoder</h3>
            <p>
              Reads the sequence one step at a time and carries a hidden state
              forward, so temporal order is part of what it learns. Slower to
              train because the recurrence cannot be parallelised.
            </p>
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2>Results</h2>
        <p>
          Measured on a held-out test set containing unseen normal beats and
          every anomaly. Accuracy is not reported: the test set is mostly
          anomalous, so a classifier that flags everything would score high
          without detecting anything.
        </p>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Model</th>
                {COLUMNS.map(([, label]) => (
                  <th key={label}>{label}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {Object.entries(metrics).map(([name, m]) => (
                <tr key={name}>
                  <td>{MODEL_LABELS[name] ?? name}</td>
                  {COLUMNS.map(([key]) => (
                    <td key={key}>{m[key].toFixed(3)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="about-section">
        <h2>Dataset</h2>
        <p>
          <a
            href="https://www.timeseriesclassification.com/description.php?Dataset=ECG5000"
            target="_blank"
            rel="noreferrer"
          >
            ECG5000
          </a>{" "}
          from the UCR Time Series Archive: 5,000 single-lead ECG heartbeats,
          each resampled to 140 timesteps. One class is a normal heartbeat; the
          other four are different abnormalities, which are grouped together as
          "anomaly" for this project.
        </p>
      </section>

      <section className="about-section">
        <h2>Tech stack</h2>
        <div className="tech-grid">
          {TECH.map((t) => (
            <div key={t.group} className="tech-card">
              <h3>{t.group}</h3>
              <div className="chips">
                {t.items.map((i) => (
                  <span key={i} className="chip">
                    {i}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h2>Limitations</h2>
        <ul className="limit-list">
          {LIMITATIONS.map((l) => (
            <li key={l}>{l}</li>
          ))}
        </ul>
      </section>

      <section className="about-section about-author">
        <h2>Author</h2>
        <p>
          <b>Ankur Saini</b> · Roll no. 23EBKAI009 · B.Tech Artificial
          Intelligence, 7th semester
        </p>

        <a
          href={REPO_URL}
          target="_blank"
          rel="noreferrer"
          className="btn btn-ghost"
        >
          View source code
        </a>
      </section>
    </div>
  );
}