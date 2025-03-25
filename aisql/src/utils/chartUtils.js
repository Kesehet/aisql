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
    const { chartType, xField, yFields, rField, labelsField } = config;
  
    const xIndex = headers.indexOf(xField);
    const yIndices = yFields.map((f) => headers.indexOf(f));
    const rIndex = rField ? headers.indexOf(rField) : null;
    const labelIndex = labelsField ? headers.indexOf(labelsField) : null;
  
    const labels = rows.map((row) => row[xIndex]);
  
    if (["bar", "line", "radar"].includes(chartType)) {
      return {
        labels,
        datasets: yFields.map((field, i) => ({
          label: field,
          data: rows.map((row) => Number(row[yIndices[i]]) || 0),
          backgroundColor: getColor(i),
          borderColor: getColor(i),
          fill: chartType === "radar",
        })),
      };
    }
  
    if (["pie", "doughnut", "polarArea"].includes(chartType)) {
      const data = rows.map((row) => Number(row[yIndices[0]]) || 0);
      const pieLabels = labelIndex !== null ? rows.map((row) => row[labelIndex]) : labels;
      return {
        labels: pieLabels,
        datasets: [
          {
            data,
            backgroundColor: data.map((_, i) => getColor(i)),
          },
        ],
      };
    }
  
    if (chartType === "bubble") {
      return {
        datasets: yFields.map((field, i) => ({
          label: field,
          data: rows.map((row) => ({
            x: Number(row[xIndex]) || 0,
            y: Number(row[yIndices[i]]) || 0,
            r: rIndex !== null ? Number(row[rIndex]) || 5 : 5,
          })),
          backgroundColor: getColor(i),
        })),
      };
    }
  
    if (chartType === "scatter") {
      return {
        datasets: yFields.map((field, i) => ({
          label: field,
          data: rows.map((row) => ({
            x: Number(row[xIndex]) || 0,
            y: Number(row[yIndices[i]]) || 0,
          })),
          backgroundColor: getColor(i),
        })),
      };
    }
  
    throw new Error("Unsupported chart type");
  };
  