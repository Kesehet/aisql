import React, { useEffect, useState } from "react";
import { ProgressSpinner } from "primereact/progressspinner";
import { Dropdown } from "primereact/dropdown";
import { MultiSelect } from "primereact/multiselect";
import { createChartData } from "../utils/chartUtils";
import ChartDisplay from "./ChartDisplay";
import { Accordion, AccordionTab } from "primereact/accordion";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const QueryCard = ({ query, chartType = "bar", response: initialResponse = null }) => {
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState(null);
  const [response, setResponse] = useState(initialResponse);
  const [sqlQuery, setSqlQuery] = useState("");
  const [selectedChartType, setSelectedChartType] = useState(chartType);

  const [xField, setXField] = useState(null);
  const [yFields, setYFields] = useState([]);

  const chartTypes = [
    { label: "Table", value:"table"},
    { label: "Bar", value: "bar" },
    { label: "Line", value: "line" },
    { label: "Pie", value: "pie" },
    { label: "Doughnut", value: "doughnut" },
    { label: "Radar", value: "radar" },
    { label: "Bubble", value: "bubble" },
    { label: "Scatter", value: "scatter" },
  ];

  const processResponse = (result) => {
    if (result?.result) {
      const [headers, rows] = result.result;

      // Set default x/y fields if not already set
      if (!xField) setXField(headers[0]);
      if (yFields.length === 0) setYFields(headers.slice(1));

      const config = {
        chartType: selectedChartType,
        xField: xField || headers[0],
        yFields: yFields.length > 0 ? yFields : headers.slice(1),
        customXAxisLabel: xField,
        customYAxisLabel: yFields.join(", "),
      };

      const data = createChartData(result, config);
      setChartData(data);
      setSqlQuery(result.query);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    const databaseName = localStorage.getItem("databaseName");
    const baseURL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/request`;

    const res = await fetch(baseURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, databaseName }),
    });

    const result = await res.json();
    setResponse(result);
    processResponse(result);
    setLoading(false);
  };

  useEffect(() => {
    if (response) {
      processResponse(response);
      setLoading(false);
    } else if (query) {
      fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, response, selectedChartType, xField, yFields]);

  const columnOptions =
    response?.result?.[0]?.map((col) => ({ label: col, value: col })) || [];

  return (
    <div>
      <div className="card">
        <Accordion>
          <AccordionTab header={query}>
            {loading ? (
              <div className="w3-center">
                <ProgressSpinner />
              </div>
            ) : chartData ? (
              <>
                <div className="mb-3 flex gap-3 flex-wrap align-items-center">
                  <Dropdown
                    value={selectedChartType}
                    options={chartTypes}
                    onChange={(e) => setSelectedChartType(e.value)}
                    placeholder="Select Chart Type"
                  />
                  <Dropdown
                    value={xField}
                    options={columnOptions}
                    onChange={(e) => setXField(e.value)}
                    placeholder="Select X Field"
                    disabled={["pie", "doughnut", "polarArea"].includes(selectedChartType)}
                  />
                  <MultiSelect
                    value={yFields}
                    options={columnOptions}
                    onChange={(e) => setYFields(e.value)}
                    placeholder="Select Y Field(s)"
                    display="chip"
                    disabled={["pie", "doughnut", "polarArea"].includes(selectedChartType)}
                    style={{ minWidth: "200px" }}
                  />
                </div>

                {selectedChartType === "table" ? (
                  <DataTable value={chartData.data}>
                    {chartData.options.columns.map((col) => (
                      <Column key={col.field} field={col.field} header={col.header} />
                    ))}
                  </DataTable>
                ) : (
                  <ChartDisplay
                    chartType={selectedChartType}
                    chartData={chartData}
                    title={query}
                  />
                )}
                <pre>
                  <code>{sqlQuery}</code>
                </pre>
              </>
            ) : (
              <p>No data to display.</p>
            )}
          </AccordionTab>
        </Accordion>
      </div>
    </div>
  );
};

export default QueryCard;
