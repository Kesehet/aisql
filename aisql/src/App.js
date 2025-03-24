import React, { useState } from "react";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";
import "primereact/resources/themes/lara-light-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

const getColor = (i) => {
  const colors = [
    "rgba(75, 192, 192, 0.6)",
    "rgba(255, 99, 132, 0.6)",
    "rgba(255, 205, 86, 0.6)",
    "rgba(54, 162, 235, 0.6)"
  ];
  return colors[i % colors.length];
};

const createChartData = ({ result }, config) => {
  const [headers, rows] = result;
  const { chartType, xField, yFields, rField, labelsField } = config;

  const xIndex = headers.indexOf(xField);
  const yIndices = yFields.map(f => headers.indexOf(f));
  const rIndex = rField ? headers.indexOf(rField) : null;
  const labelIndex = labelsField ? headers.indexOf(labelsField) : null;

  const labels = rows.map(row => row[xIndex]);

  if (["bar", "line", "radar"].includes(chartType)) {
    return {
      labels,
      datasets: yFields.map((field, i) => ({
        label: field,
        data: rows.map(row => Number(row[yIndices[i]]) || 0),
        backgroundColor: getColor(i),
        borderColor: getColor(i),
        fill: chartType === "radar"
      }))
    };
  }

  if (["pie", "doughnut", "polarArea"].includes(chartType)) {
    const data = rows.map(row => Number(row[yIndices[0]]) || 0);
    const pieLabels = labelIndex !== null ? rows.map(row => row[labelIndex]) : labels;
    return {
      labels: pieLabels,
      datasets: [{
        data,
        backgroundColor: data.map((_, i) => getColor(i))
      }]
    };
  }

  if (chartType === "bubble") {
    return {
      datasets: yFields.map((field, i) => ({
        label: field,
        data: rows.map(row => ({
          x: Number(row[xIndex]) || 0,
          y: Number(row[yIndices[i]]) || 0,
          r: rIndex !== null ? Number(row[rIndex]) || 5 : 5
        })),
        backgroundColor: getColor(i)
      }))
    };
  }

  if (chartType === "scatter") {
    return {
      datasets: yFields.map((field, i) => ({
        label: field,
        data: rows.map(row => ({
          x: Number(row[xIndex]) || 0,
          y: Number(row[yIndices[i]]) || 0
        })),
        backgroundColor: getColor(i)
      }))
    };
  }

  throw new Error("Unsupported chart type");
};

const App = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [chartType, setChartType] = useState("bar");

  const onSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch("http://localhost:5000/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const result = await response.json();
    setResponse(result);

    if (result && result.result) {
      const [headers] = result.result;
      const xField = headers[0];
      const yFields = headers.slice(1);

      const config = {
        chartType,
        xField,
        yFields
      };

      const data = createChartData(result, config);
      setChartData(data);
    }
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
          <Chart type={chartType} data={chartData} options={{ responsive: true, maintainAspectRatio: false }} style={{ height: '400px' }} />
        </Card>
      )}

      {response && (
        <Card className="p-4 w-full md:w-6 mt-4">
          <h2 className="text-center">Response</h2>
          <pre className="text-green-600 overflow-auto" style={{ maxHeight: '300px' }}>{JSON.stringify(response, null, 2)}</pre>
        </Card>
      )}
    </div>
  );
};

export default App;
