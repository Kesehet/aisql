import React, { useState } from "react";
import { Dialog } from "primereact/dialog";
import QueryForm from "./QueryForm";
import QueryCard from "./QueryCard";
import SqlRun from "./SqlRun";

const MainApp = ({ dbName, onReset }) => {
  const [query, setQuery] = useState("");
  const [submittedQueries, setSubmittedQueries] = useState([]);
  const [selectedQuery, setSelectedQuery] = useState(null);

  const onSubmit = (event) => {
    event.preventDefault();
    if (query.trim()) {
      setSubmittedQueries((prev) => [...prev, query]);
      setQuery("");
    }
  };

  return (
    <div className="w3-container">
      <div className="w3-blue w3-padding w3-row">
        <div className="w3-col s10">
            <h3>Current Database: <code>{dbName}</code></h3>
        </div>
        <div className="w3-col s2 w3-right-align">
            <button onClick={onReset} className="w3-button w3-red">Reset Database</button>
        </div>
    </div>


      <QueryForm query={query} setQuery={setQuery} onSubmit={onSubmit} />

      <div className="w3-row">
        {submittedQueries.map((q, idx) => (
          <div
            key={idx}
            onClick={() => setSelectedQuery(q)}
            style={{ cursor: "pointer" }}
            className={
              "w3-padding w3-animate-zoom" +
              (q.length < 20
                ? " w3-third"
                : q.length < 40
                ? " w3-half"
                : q.length < 80
                ? " w3-quarter"
                : "")
            }
          >
            <QueryCard query={q} />
          </div>
        ))}
      </div>

      <SqlRun />

      <Dialog
        visible={!!selectedQuery}
        style={{ width: "90vw" }}
        onHide={() => setSelectedQuery(null)}
        maximizable
        modal
      >
        {selectedQuery && <QueryCard query={selectedQuery} />}
      </Dialog>
      
    </div>
  );
};

export default MainApp;
