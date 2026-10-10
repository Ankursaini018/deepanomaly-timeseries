import { useEffect, useState } from "react";
import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import ModelSelector from "./components/ModelSelector";
import SummaryCards from "./components/SummaryCards";
import ResultsTable from "./components/ResultsTable";
import ReconstructionChart from "./components/ReconstructionChart";
import ErrorBanner from "./components/ErrorBanner";
import { fetchModels, predictFromCSV } from "./api/client";

function parseCSVText(text) {
  return text.trim().split("\n").map((row) => row.split(",").map(Number));
}

function App() {
  const [availableModels, setAvailableModels] = useState(["dense"]);
  const [mode, setMode] = useState("dense");
  const [file, setFile] = useState(null);
  const [originalSequences, setOriginalSequences] = useState(null);
  const [resultsByModel, setResultsByModel] = useState({});
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchModels()
      .then(setAvailableModels)
      .catch(() => setError("Could not reach the server. Is the backend running?"));
  }, []);

  const activeNames = mode === "compare" ? availableModels : [mode];

  // Fetch predictions for any active model we haven't cached for this file yet.
  useEffect(() => {
    if (!file) return;
    const needed = activeNames.filter((m) => !resultsByModel[m]);
    if (needed.length === 0) return;

    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const entries = await Promise.all(
          needed.map(async (m) => [m, await predictFromCSV(file, m)])
        );
        if (!cancelled) {
          setResultsByModel((prev) => ({ ...prev, ...Object.fromEntries(entries) }));
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err.code === "ECONNABORTED"
              ? "Request timed out. Try a smaller file."
              : err.response?.data?.detail || "Prediction failed."
          );
        }
      } finally {
        setLoading(false);
      }
    })();

    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [file, mode, availableModels]);

  const handleUpload = async (f) => {
    const text = await f.text();
    setOriginalSequences(parseCSVText(text));
    setResultsByModel({});
    setSelectedIndex(0);
    setFile(f);
  };

  const ready = file && originalSequences && activeNames.every((m) => resultsByModel[m]);

  const reconstructions = ready
    ? Object.fromEntries(
        activeNames.map((m) => [m, resultsByModel[m].results[selectedIndex].reconstructed])
      )
    : null;

  return (
    <div className="app">
      <Header />
      <FileUpload onUpload={handleUpload} loading={loading} />
      <ModelSelector
        value={mode}
        onChange={setMode}
        available={availableModels}
        disabled={loading}
      />
      <ErrorBanner message={error} onClose={() => setError(null)} />

      {ready && mode !== "compare" && (
        <>
          <SummaryCards results={resultsByModel[mode]} />
          <ResultsTable
            results={resultsByModel[mode].results}
            onSelectRow={setSelectedIndex}
            selectedIndex={selectedIndex}
          />
        </>
      )}

      {ready && (
        <ReconstructionChart
          original={originalSequences[selectedIndex]}
          reconstructions={reconstructions}
        />
      )}
    </div>
  );
}

export default App;