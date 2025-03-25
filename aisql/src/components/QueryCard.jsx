import React, { useEffect, useState } from "react";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";
import { createChartData } from "../utils/chartUtils";
import { ProgressSpinner } from "primereact/progressspinner";
import ChartDisplay from "./ChartDisplay";

const QueryCard = ({ query, chartType = "bar" }) => {
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState(null);
  const [response, setResponse] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const res = await fetch("http://localhost:5000/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const result = await res.json();
      setResponse(result);

      if (result?.result) {
        const [headers] = result.result;
        const xField = headers[0];
        const yFields = headers.slice(1);
        const config = { chartType, xField, yFields };
        const data = createChartData(result, config);
        setChartData(data);
      }

      setLoading(false);
    };

    if (query) {
      fetchData();
    }
  }, [query, chartType]);

  return (
    <div>
        {loading ? (
            <div className="w3-center">
                <ProgressSpinner />
            </div>
        ) : chartData ? (
                <ChartDisplay chartType={chartType} chartData={chartData} title={query} />
        ) : (
            <p>No data to display.</p>
        )}
    </div>

  );
};

export default QueryCard;
