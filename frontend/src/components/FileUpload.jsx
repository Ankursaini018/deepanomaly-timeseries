import { useState, useRef } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";

export default function FileUpload({ onUpload, loading }) {
  const [fileName, setFileName] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleFile = (file) => {
    if (!file) return;
    if (!file.name.endsWith(".csv")) {
      alert("Please upload a .csv file");
      return;
    }
    setFileName(file.name);
    onUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files[0]);
  };

  return (
    <div
      className={`upload-zone ${dragActive ? "drag-active" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
      onDragLeave={() => setDragActive(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        hidden
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {loading ? (
        <>
          <Loader2 className="icon spin" size={36} />
          <p>Running inference...</p>
        </>
      ) : fileName ? (
        <>
          <FileText size={36} className="icon" />
          <p>{fileName}</p>
          <span className="hint">Click to upload a different file</span>
        </>
      ) : (
        <>
          <Upload size={36} className="icon" />
          <p>Drag & drop a CSV file, or click to browse</p>
          <span className="hint">Each row = one time series (140 values)</span>
        </>
      )}
    </div>
  );
}