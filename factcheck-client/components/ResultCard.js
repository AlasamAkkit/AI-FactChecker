export default function ResultCard({ result }) {
  if (!result || Object.keys(result).length === 0) {
    return <p className="text-gray-500 mt-4">No results yet. Enter a claim to fact-check.</p>;
  }

  return (
    <div className="mt-6 p-6 w-full max-w-lg bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-gray-700 mb-3">Fact-Check Result</h2>
      <p className="text-gray-600 mb-2">
        <strong>Claim:</strong> {result.text || "No claim provided."}
      </p>
      
      <p className="text-gray-700 mb-2">
        <strong>Best Verdict:</strong>{" "}
        {result.best_ai_verdict && result.google_fact_checks && result.google_fact_checks.length > 0 ? (
          <span className="text-green-600"> {result.best_ai_verdict} (Verified by Google)</span>
        ) : (
          <span className="text-yellow-600"> {result.best_ai_verdict} (AI Generated)</span>
        )}
      </p>

      {result.ai_verdicts && result.ai_verdicts.length > 0 ? (
        <>
          <h3 className="font-semibold text-gray-700 mt-4">AI Confidence Levels:</h3>
          <ul className="list-disc list-inside mt-2">
            {result.ai_verdicts.map((item, index) => (
              <li key={index} className="text-gray-600">
                {item.label}: {item.confidence}%
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="text-gray-500 mt-2">No AI confidence data available.</p>
      )}

      {result.google_fact_checks && result.google_fact_checks.length > 0 && (
        <>
          <h3 className="font-semibold text-gray-700 mt-4">Google Fact Checks:</h3>
          <ul className="list-disc list-inside mt-2">
            {result.google_fact_checks.map((item, index) => (
              <li key={index} className="text-gray-600">
                <strong>{item.claim}</strong>: {item.verdict}
                <a href={item.source_url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
                  {" "} (Read More)
                </a>
              </li>
            ))}
          </ul>
        </>
      )}

      {result.google_search_results && result.google_search_results.length > 0 && (
        <>
          <h3 className="font-semibold text-gray-700 mt-4">Google Search Results:</h3>
          <ul className="list-disc list-inside mt-2">
            {result.google_search_results.map((item, index) => (
              <li key={index} className="text-gray-600">
                <strong>{item.title}</strong>: {item.snippet}
                <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-500">
                  {" "} (Read More)
                </a>
              </li>
            ))}
          </ul>
        </>
      )}

      {result.wikipedia_summary ? (
        <>
          <h3 className="font-semibold text-gray-700 mt-4">Wikipedia Summary:</h3>
          <p className="text-gray-600">
            {result.wikipedia_summary.summary || "No summary available."}
          </p>
          <a href={result.wikipedia_summary.url || "#"} target="_blank" rel="noopener noreferrer" className="text-blue-500">
            Read More
          </a>
        </>
      ) : (
        <p className="text-gray-500 mt-2">No Wikipedia summary found.</p>
      )}
    </div>
  );
}
