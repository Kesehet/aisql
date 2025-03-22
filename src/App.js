import React, { useState } from "react";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";
import "primereact/resources/themes/lara-light-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

const App = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [chartData, setChartData] = useState(null);

  const onSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch("http://localhost:5000/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const result = await response.text();
    setResponse(result);

    if (result.function && result.function.length > 0 && result.function[0].output) {
      updateChart(result.function[0].output);
    }
  };

  const updateChart = (data) => {
    setChartData({
      labels: data.labels,
      datasets: data.datasets.map((dataset) => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      })),
    });
  };

  return (
    <div className="p-4 flex flex-column align-items-center">
      <Card className="p-4 w-full md:w-6">
        <h2 className="text-center">Request Form</h2>
        <form onSubmit={onSubmit} className="flex flex-column gap-3">
          <label className="font-bold">Enter your query</label>
          <InputText value={query} onChange={(e) => setQuery(e.target.value)} className="w-full" />
          <Button label="Submit" icon="pi pi-send" className="p-button-primary" type="submit" />
        </form>
      </Card>

      {chartData && (
        <Card className="p-4 w-full md:w-6 mt-4">
          <h2 className="text-center">Chart</h2>
          <Chart type="bar" data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
        </Card>
      )}

      {response && (
        <Card className="p-4 w-full md:w-6 mt-4">
          <h2 className="text-center">Response</h2>
          <pre className="text-green-600">{JSON.stringify(response, null, 2)}</pre>
        </Card>
      )}
    </div>
  );
};

export default App;