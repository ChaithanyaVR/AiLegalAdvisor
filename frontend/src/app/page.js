"use client";

import { useState, useEffect } from "react";
import ContractChat from "../components/ContractChat/page.jsx";
import { uploadDocument, fetchAnalyses } from "../../utils/api";

function ClauseViewer({ clauses }) {
  let parsed = clauses;

  if (typeof clauses === "string") {
    try {
      parsed = JSON.parse(clauses);
    } catch {
      return (
        <div
          className="
          text-zinc-300
        "
        >
          {clauses}
        </div>
      );
    }
  }

  return (
    <div
      className="
      grid
      gap-4
    "
    >
      {Object.entries(parsed || {}).map(([key, value]) => (
        <div
          key={key}
          className="
                bg-zinc-900
                border
                border-zinc-800
                rounded-xl
                p-5
              "
        >
          <h3
            className="
                text-blue-400
                text-lg
                font-semibold
                mb-3
              "
          >
            {key

              .replaceAll("_", " ")

              .replace(
                /\b\w/g,

                (c) => c.toUpperCase(),
              )}
          </h3>

          <p
            className="
                text-zinc-300
                leading-relaxed
              "
          >
            {value || "Clause not found"}
          </p>
        </div>
      ))}
    </div>
  );
}

export default function Home() {
  const [file, setFile] = useState(null);

  const [result, setResult] = useState(null);

  const [analyses, setAnalyses] = useState([]);

  const [loading, setLoading] = useState(false);

  async function loadHistory() {
    try {
      const data = await fetchAnalyses();

      setAnalyses(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function uploadFile() {
    if (!file) {
      alert("Select file");

      return;
    }

    try {
      setLoading(true);

      const data = await uploadDocument(file);

      setResult(data);

      await loadHistory();
    } catch (err) {
      console.error(err);

      alert(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <main
        className="
      min-h-screen
      bg-zinc-950
      text-white
      p-20
    "
      >
        <div
          className="
        max-w-7xl
        mx-auto
        grid
        grid-cols-1
        lg:grid-cols-2
        gap-8
      "
        >
          {/* LEFT PANEL */}

          <div
            className="
          bg-zinc-900
          border
          border-zinc-800
          rounded-2xl
          p-8
        "
          >
            <h1
              className="
            text-3xl
            font-bold
            mb-3
          "
            >
              AI Legal Advisor
            </h1>

            <p
              className="
            text-zinc-400
            mb-8
          "
            >
              Upload legal contract
            </p>

            <label
              className="
              flex
              flex-col
              items-center
              justify-center
              border-2
              border-dashed
              border-zinc-700
              rounded-xl
              p-10
              cursor-pointer
              hover:border-blue-500
            "
            >
              <span
                className="
              text-zinc-300
              mb-3
            "
              >
                Choose PDF Document
              </span>

              <input
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            {file && (
              <div
                className="
                mt-5
                text-green-400
              "
              >
                Selected: {file.name}
              </div>
            )}

            <button
              onClick={uploadFile}
              disabled={loading}
              className="
              mt-8
              w-full
              bg-blue-600
              hover:bg-blue-700
              rounded-xl
              py-3
              font-semibold
              disabled:opacity-50
            "
            >
              {loading ? "Analyzing..." : "Upload & Analyze"}
            </button>

            <div className="mt-4 text-yellow-400">
              Contract ID:
              {result?.contract_id || "NOT FOUND"}
            </div>

            <ContractChat contractId={result?.contract_id || 1} />

            {/* CURRENT RESULT */}

            {result && (
              <div
                className="
                mt-10
              "
              >
                <h2
                  className="
                  text-2xl
                  font-bold
                  mb-5
                "
                >
                  Latest Analysis
                </h2>

                <div
                  className="
                  mb-5
                  text-green-400
                "
                >
                  {result.filename}
                </div>

                <ClauseViewer clauses={result.clauses} />
              </div>
            )}
          </div>

          {/* RIGHT PANEL */}

          <div
            className="
          bg-zinc-900
          border
          border-zinc-800
          rounded-2xl
          p-8
        "
          >
            <h2
              className="
            text-2xl
            font-bold
            mb-6
          "
            >
              Analysis History
            </h2>

            {analyses.length === 0 ? (
              <p
                className="
                text-zinc-500
              "
              >
                No analyses found
              </p>
            ) : (
              <div
                className="
                space-y-6
              "
              >
                {analyses.map((analysis) => (
                  <div
                    key={analysis.id}
                    className="
                          bg-zinc-950
                          border
                          border-zinc-800
                          rounded-xl
                          p-6
                        "
                  >
                    <h3
                      className="
                          text-blue-400
                          text-xl
                          font-bold
                          mb-2
                        "
                    >
                      {analysis.filename}
                    </h3>

                    <p
                      className="
                          text-xs
                          text-zinc-500
                          mb-5
                        "
                    >
                      {analysis.created_at}
                    </p>

                    <ClauseViewer clauses={analysis.clauses} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}
