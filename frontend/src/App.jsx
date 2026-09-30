import { useState } from "react";
import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import SummaryCards from "./components/SummaryCards";
import ResultsTable from "./components/ResultsTable";
import { predictFromCSV } from "./api/client";

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictFromCSV(file);
      setResults(data);
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
          <ResultsTable results={results.results} />
        </>
      )}
    </div>
  );
}

export default App;