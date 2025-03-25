import React from "react";
import { Card } from "primereact/card";

const ResponseDisplay = ({ response }) => (
  <Card className="p-4 w-full md:w-6 mt-4">
    <h2 className="text-center">Response</h2>
    <pre className="text-green-600 overflow-auto" style={{ maxHeight: "300px" }}>
      {JSON.stringify(response, null, 2)}
    </pre>
  </Card>
);

export default ResponseDisplay;
