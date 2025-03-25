import React from "react";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { Card } from "primereact/card";

const QueryForm = ({ query, setQuery, onSubmit }) => (
  <Card className="p-4 w-full md:w-6">
    <h2 className="text-center">Request Form</h2>
    <form onSubmit={onSubmit} className="flex flex-column gap-3">
      <label className="font-bold">Enter your query</label>
      <InputText value={query} onChange={(e) => setQuery(e.target.value)} className="w-full" />
      <Button label="Submit" icon="pi pi-send" className="p-button-primary" type="submit" />
    </form>
  </Card>
);

export default QueryForm;
