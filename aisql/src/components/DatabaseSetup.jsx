import React, { useState } from "react";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { Card } from "primereact/card";
import { Message } from "primereact/message";

const DatabaseSetup = ({ onSuccess }) => {
  const [dbName, setDbName] = useState("");
  const [csvFiles, setCsvFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMessages, setErrorMessages] = useState([]);

  const handleFileChange = (e) => {
    setCsvFiles(Array.from(e.target.files));
  };

  const readFileAsText = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsText(file);
    });

  const handleSubmit = async () => {
    if (!dbName || csvFiles.length === 0) {
      alert("Please enter a database name and select at least one CSV file.");
      return;
    }

    setLoading(true);
    setErrorMessages([]);

    try {
      for (const file of csvFiles) {
        const csvString = await readFileAsText(file);

        const response = await fetch("http://localhost:5000/create-database", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            csv_title: file.name,
            csv_string: csvString,
            db_name: dbName,
          }),
        });

        const result = await response.json();
        if (result.status !== "success") {
          setErrorMessages((prev) => [
            ...prev,
            `Failed to process ${file.name}`,
          ]);
        }
      }

      if (errorMessages.length === 0) {
        onSuccess(dbName);
      }
    } catch (err) {
      setErrorMessages([`Something went wrong: ${err.message}`]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 flex justify-center">
      <Card title="Setup Your Database" className="w-full max-w-xl">
        <div className="p-fluid space-y-4">
          <div>
            <label htmlFor="dbName" className="block mb-2 font-semibold">
              Database Name
            </label>
            <InputText
              id="dbName"
              value={dbName}
              onChange={(e) => setDbName(e.target.value)}
              placeholder="Enter database name"
              className="w-full"
              required
            />
          </div>

          <div>
            <label className="block mb-2 font-semibold">Select CSV Files</label>
            <input
              type="file"
              multiple
              accept=".csv"
              onChange={handleFileChange}
              className="w-full"
            />
          </div>

          {errorMessages.map((msg, idx) => (
            <Message key={idx} severity="error" text={msg} />
          ))}

          <div className="pt-2">
            <Button
              label={loading ? "Uploading..." : "Create Database"}
              icon={loading ? "pi pi-spin pi-spinner" : "pi pi-database"}
              onClick={handleSubmit}
              disabled={loading}
              className="w-full"
            />
          </div>
        </div>
      </Card>
    </div>
  );
};

export default DatabaseSetup;
