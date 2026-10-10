export default function ErrorBanner({ message, onClose }) {
  if (!message) return null;

  return (
    <div
      style={{
        marginTop: "1rem",
        padding: "0.75rem 1rem",
        borderRadius: "8px",
        background: "rgba(239, 68, 68, 0.12)",
        border: "1px solid rgba(239, 68, 68, 0.4)",
        color: "#fca5a5",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "1rem",
      }}
    >
      <span>{message}</span>

      <button
        onClick={onClose}
        style={{
          background: "transparent",
          border: "none",
          color: "inherit",
          cursor: "pointer",
          fontSize: "1.1rem",
        }}
        aria-label="Close error"
      >
        ×
      </button>
    </div>
  );
}