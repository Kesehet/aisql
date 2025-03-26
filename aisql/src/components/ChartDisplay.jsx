import React from "react";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";

const ChartDisplay = ({ chartType, chartData, title }) => (
  <Card className="p-4 w-full md:w-6 mt-4">
    <h2 className="text-center">{title}</h2>
    <Chart
      type={chartType}
      data={chartData.data}
      options={chartData.options}
    />
  </Card>
);

export default ChartDisplay;
