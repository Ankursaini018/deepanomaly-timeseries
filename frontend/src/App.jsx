import { useState } from "react";
import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import SummaryCards from "./components/SummaryCards";
import ResultsTable from "./components/ResultsTable";
import ReconstructionChart from "./components/ReconstructionChart";
import { predictFromCSV } from "./api/client";

function parseCSVText(text) {
  return text
    .trim()
    .split("\n")
    .map((row) => row.split(",").map(Number));
}

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [originalSequences, setOriginalSequences] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const text = await file.text();
      setOriginalSequences(parseCSVText(text));

      const data = await predictFromCSV(file);
      setResults(data);
      setSelectedIndex(0);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Header />
      <FileUpload onUpload={handleUpload} loading={loading} />
      {error && <p className="error">{error}</p>}
      {results && (
        <>
          <SummaryCards results={results} />
          <ResultsTable
            results={results.results}
            onSelectRow={setSelectedIndex}
            selectedIndex={selectedIndex}
          />
          {originalSequences && (
            <ReconstructionChart
              original={originalSequences[selectedIndex]}
              reconstructed={results.results[selectedIndex].reconstructed}
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;