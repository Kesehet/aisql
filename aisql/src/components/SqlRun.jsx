import React, { useState } from "react";
import ChartDisplay from "./ChartDisplay";
import {createChartData, getDatabaseName } from "../utils/chartUtils";
import QueryCard from "./QueryCard";

const SqlRun = () => {
    const [query, setQuery] = useState("");
    const [databaseName, setDatabaseName] = useState(getDatabaseName());
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleRunSql = async () => {
        try {
            const res = await fetch("/run-sql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    query,
                    databaseName,
                }),
            });
            if (!res.ok) {
                throw new Error((await res.json()).error);
            }
            setResponse(await res.json());
            setError(null);
        } catch (err) {
            setError(err.message || "An error occurred");
            setResponse(null);
        }
    };

    return (
        <div className="w3-container">
            <h1 className="w3-blue w3-padding w3-center">SQL Runner</h1>
            <div className="w3-row-padding">
                <textarea
                    className="w3-input w3-border"
                    placeholder="Enter SQL query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
            </div>
            <div className="w3-row-padding">
                <input
                    type="text"
                    className="w3-input w3-border"
                    placeholder="Enter database name"
                    value={databaseName}
                    onChange={(e) => setDatabaseName(e.target.value)}
                />
            </div>
            <button
                className="w3-button w3-blue w3-round w3-margin"
                onClick={handleRunSql}
            >
                Run SQL
            </button>
            {response && (
                <QueryCard response={response} />
            )}
            {error && (
                <p className="w3-red w3-padding">{error}</p>
            )}
        </div>
    );
};

export default SqlRun;