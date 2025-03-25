import React, { useState } from "react";
import { Dialog } from "primereact/dialog";
import QueryForm from "./components/QueryForm";
import QueryCard from "./components/QueryCard";

const App = () => {
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
      <QueryForm query={query} setQuery={setQuery} onSubmit={onSubmit} />

      <div className="w3-row" >
        {submittedQueries.map((q, idx) => (
          <div
            key={idx}
            onClick={() => setSelectedQuery(q)}
            style={{ cursor: "pointer" }}
            className="w3-third w3-padding w3-animate-zoom"
          >
            <QueryCard query={q} />
          </div>
        ))}
      </div>



      <Dialog
        visible={!!selectedQuery}
        style={{ width: "90vw",}}
        onHide={() => setSelectedQuery(null)}
        maximizable
        modal
      >
        {selectedQuery && (
          
            <QueryCard query={selectedQuery} />
          
        )}
      </Dialog>
    </div>
  );
};

export default App;
