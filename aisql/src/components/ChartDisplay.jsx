import React from "react";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";

const ChartDisplay = ({ chartType, chartData }) => (
  <Card className="p-4 w-full md:w-6 mt-4">
    <h2 className="text-center">Chart</h2>
    <Chart
      type={chartType}
      data={chartData}
      options={{ responsive: true, maintainAspectRatio: false }}
      style={{ height: "400px" }}
    />
  </Card>
);

export default ChartDisplay;
