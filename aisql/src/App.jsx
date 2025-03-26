import React, { useState, useEffect } from "react";
import DatabaseSetup from "./components/DatabaseSetup";
import MainApp from "./components/MainApp";

const App = () => {
  const [dbReady, setDbReady] = useState(false);
  const [dbName, setDbName] = useState(null);

  useEffect(() => {
    const savedDb = localStorage.getItem("databaseName");
    const expiry = localStorage.getItem("databaseExpiry");
    if (savedDb && expiry && new Date().getTime() < Number(expiry)) {
      setDbName(savedDb);
      setDbReady(true);
    }
  }, []);

  const handleDatabaseCreated = (name) => {
    const expiry = new Date().getTime() + 2 * 24 * 60 * 60 * 1000; // 2 days
    localStorage.setItem("databaseName", name);
    localStorage.setItem("databaseExpiry", expiry);
    setDbName(name);
    setDbReady(true);
  };

  const handleResetDatabase = () => {
    localStorage.removeItem("databaseName");
    localStorage.removeItem("databaseExpiry");
    setDbName(null);
    setDbReady(false);
  };

  return dbReady ? (
    <MainApp dbName={dbName} onReset={handleResetDatabase} />
  ) : (
    <DatabaseSetup onSuccess={handleDatabaseCreated} />
  );
};

export default App;
