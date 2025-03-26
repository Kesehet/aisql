const getColor = (i) => {
    const colors = [
      "rgba(75, 192, 192, 0.6)",
      "rgba(255, 99, 132, 0.6)",
      "rgba(255, 205, 86, 0.6)",
      "rgba(54, 162, 235, 0.6)",
    ];
    return colors[i % colors.length];
  };
  
  export const createChartData = ({ result }, config) => {
    const [headers, rows] = result;
    const {
      chartType,
      xField,
      yFields,
      rField,
      labelsField,
      customXAxisLabel,
      customYAxisLabel,
    } = config;
  
    const xIndex = headers.indexOf(xField);
    if (xIndex === -1) throw new Error(`xField "${xField}" not found in headers`);

    const yIndices = yFields.map((f) => {
      const idx = headers.indexOf(f);
      if (idx === -1) throw new Error(`yField "${f}" not found in headers`);
      return idx;
    });

    const rIndex = rField ? headers.indexOf(rField) : null;
    const labelIndex = labelsField ? headers.indexOf(labelsField) : null;
  
    const labels = rows.map((row) => row[xIndex]);
  
    const commonOptions = {
      plugins: {
        legend: { display: true },
      },
      scales: {
        x: {
          title: {
            display: !!customXAxisLabel,
            text: customXAxisLabel || "",
          },
        },
        y: {
          title: {
            display: !!customYAxisLabel,
            text: customYAxisLabel || "",
          },
        },
      },
    };
  
    if (["bar", "line", "radar"].includes(chartType)) {
      return {
        data: {
          labels,
          datasets: yFields.map((field, i) => ({
            label: field,
            data: rows.map((row) => Number(row[yIndices[i]]) || 0),
            backgroundColor: getColor(i),
            borderColor: getColor(i),
            fill: chartType === "radar",
          })),
        },
        options: commonOptions,
      };
    }
  
    if (["pie", "doughnut", "polarArea"].includes(chartType)) {
      const data = rows.map((row) => Number(row[yIndices[0]]) || 0);
      const pieLabels = labelIndex !== null ? rows.map((row) => row[labelIndex]) : labels;
      return {
        data: {
          labels: pieLabels,
          datasets: [
            {
              data,
              backgroundColor: data.map((_, i) => getColor(i)),
            },
          ],
        },
      };
    }
  
    if (chartType === "bubble") {
      return {
        data: {
          datasets: yFields.map((field, i) => ({
            label: field,
            data: rows.map((row) => ({
              x: Number(row[xIndex]) || 0,
              y: Number(row[yIndices[i]]) || 0,
              r: rIndex !== null ? Number(row[rIndex]) || 5 : 5,
            })),
            backgroundColor: getColor(i),
          })),
        },
        options: commonOptions,
      };
    }
  
    if (chartType === "scatter") {
      return {
        data: {
          datasets: yFields.map((field, i) => ({
            label: field,
            data: rows.map((row) => ({
              x: Number(row[xIndex]) || 0,
              y: Number(row[yIndices[i]]) || 0,
            })),
            backgroundColor: getColor(i),
          })),
        },
        options: commonOptions,
      };
    }
  
    throw new Error("Unsupported chart type");
  };
  
  