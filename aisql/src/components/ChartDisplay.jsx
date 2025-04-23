import React from "react";
import { Card } from "primereact/card";
import { Chart } from "primereact/chart";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const ChartDisplay = ({ chartType, chartData, title }) => (
  <Card className="p-4 w-full md:w-6 mt-4">
    <h2 className="text-center">{title}</h2>
    {chartType === "table" ? (
      <DataTable value={chartData.data}>
        {chartData.options.columns.map((col) => (
          <Column key={col.field} field={col.field} header={col.header} />
        ))}
      </DataTable>
    ) : (
      <Chart
        type={chartType}
        data={chartData.data}
        options={chartData.options}
      />
    )}
  </Card>
);

export default ChartDisplay;
