import { useState, useEffect, useRef } from "react";
import "./CatFact.css";

function CatFact() {
  // 1. State variables to store the data, loading status, and any errors
  const [fact, setFact] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Keep track of the active AbortController to cancel previous fetches
  const abortControllerRef = useRef(null);

  // 2. A function to fetch the cat fact from the public API
  const fetchFact = async (showLoadingState = false) => {
    // Abort any previous pending request to prevent race conditions
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create a new AbortController for this fetch session
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      if (showLoadingState) {
        setLoading(true);
      }
      setError(null);

      const response = await fetch("https://catfact.ninja/fact", {
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      // Verify this request is still the active one before setting state
      if (abortControllerRef.current === controller) {
        setFact(data.fact);
      }
    } catch (err) {
      // Ignore AbortError as it is an intentional cancellation
      if (err.name !== "AbortError") {
        setError(err.message);
      }
    } finally {
      // Only turn off loading state if this was the last initiated request
      if (abortControllerRef.current === controller) {
        setLoading(false);
      }
    }
  };

  // 3. useEffect hook runs when the component mounts
  useEffect(() => {
    // Initial fetch
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchFact(false);

    // Cleanup on unmount to abort any pending request
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  // 4. Conditional rendering based on API status
  return (
    <div className="cat-fact-container">
      <h2 className="cat-fact-title">🐱 Random Cat Fact</h2>

      {loading && <p className="cat-fact-loading">Fetching a cool fact for you...</p>}

      {error && (
        <div className="cat-fact-error-container">
          <p className="cat-fact-error">Error: {error}</p>
          <button className="cat-fact-retry-button" onClick={() => fetchFact(true)}>
            Try Again
          </button>
        </div>
      )}

      {!loading && !error && (
        <div>
          <p className="cat-fact-text">"{fact}"</p>
          <button className="cat-fact-button" onClick={() => fetchFact(true)}>
            Get Another Fact
          </button>
        </div>
      )}
    </div>
  );
}

export default CatFact;
