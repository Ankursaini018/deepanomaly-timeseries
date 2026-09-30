import { useState } from "react";
import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
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
      {results && <p>Total: {results.total} | Anomalies: {results.anomalies_found}</p>}
    </div>
  );
}

export default App;