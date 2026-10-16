import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="page not-found">
      <h1>404</h1>
      <p>That page does not exist.</p>
      <Link to="/" className="btn btn-primary">
        Back to Home
      </Link>
    </div>
  );
}