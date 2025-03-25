import React, { useState } from "react";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";
import QueryForm from "./components/QueryForm";
import ResponseDisplay from "./components/ResponseDisplay";
import ChartDisplay from "./components/ChartDisplay";
import { createChartData } from "./utils/chartUtils";

const App = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [chartType, setChartType] = useState("bar");

  const onSubmit = async (event) => {
    event.preventDefault();
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
  };

  return (
    <div className="p-4 flex flex-column align-items-center">
      <QueryForm query={query} setQuery={setQuery} onSubmit={onSubmit} />
      {chartData && <ChartDisplay chartType={chartType} chartData={chartData} />}
      {response && <ResponseDisplay response={response} />}
    </div>
  );
};

export default App;
