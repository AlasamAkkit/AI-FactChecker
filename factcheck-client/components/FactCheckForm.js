import { useState } from "react";

export default function FactCheckForm({ onSubmit, isLoading }) {
  const [inputText, setInputText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim()) {
      onSubmit(inputText);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-6 rounded-lg shadow-lg">
      <label className="block text-gray-700 font-semibold mb-2">Enter a claim to fact-check:</label>
      <textarea
        className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        rows="3"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Example: The Earth is flat."
      ></textarea>
      <button
        type="submit"
        className={`w-full mt-4 p-3 font-bold text-white rounded-lg ${
          isLoading ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
        }`}
        disabled={isLoading}
      >
        {isLoading ? "Checking..." : "Fact Check"}
      </button>
    </form>
  );
}
