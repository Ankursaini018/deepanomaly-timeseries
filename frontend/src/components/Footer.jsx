import { REPO_URL } from "../constants";

export default function Footer() {
  return (
    <footer className="footer">
      <p>DeepAnomaly · Self-supervised anomaly detection in time series</p>
      <p className="footer-sub">
        B.Tech AI Final Year Project · Ankur Saini (23EBKAI009) ·{" "}
        <a href={REPO_URL} target="_blank" rel="noreferrer">
          Source code
        </a>
      </p>
    </footer>
  );
}