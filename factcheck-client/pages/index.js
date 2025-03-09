import { useState } from "react";
import FactCheckForm from "../components/FactCheckForm";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFactCheck = async (text) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/fact-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      console.log("API Response:", data); // Debugging

      if (response.ok) {
        setResult(data); // Update the result state
      } else {
        setError(data.detail || "An unknown error occurred.");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Failed to connect to the backend. Please check your connection.");
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">FactCheck AI</h1>
      <FactCheckForm onSubmit={handleFactCheck} isLoading={isLoading} />
      {isLoading && <p className="text-blue-500 mt-4">Checking...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      <ResultCard result={result} />
    </div>
  );
}
