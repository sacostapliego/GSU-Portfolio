import React, { useState, useEffect, useCallback } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ParkingMap from "./components/ParkingMap";
import ParkingList from "./components/ParkingList";
import ParkingDetail from "./components/ParkingDetail";
import Filters from "./components/Filters";
import AdminPanel from "./components/AdminPanel";
import { fetchParkingLots } from "./api";
import "./App.css";

function HomePage() {
  const [lots, setLots] = useState([]);
  const [filteredLots, setFilteredLots] = useState([]);
  const [selectedLot, setSelectedLot] = useState(null);
  const [filters, setFilters] = useState({
    lotType: "all",
    maxPrice: 30,
    sortBy: "name",
  });
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      const data = await fetchParkingLots();
      setLots(data);
    } catch (err) {
      console.error("Failed to fetch parking data:", err);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadData();
    // Refresh every 30s 
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [loadData]);

  useEffect(() => {
    let result = [...lots];

    if (filters.lotType === "small") {
      result = result.filter((l) => l.is_small_lot);
    } else if (filters.lotType === "large") {
      result = result.filter((l) => !l.is_small_lot);
    }

    result = result.filter((l) => l.hourly_price <= filters.maxPrice);

    if (filters.sortBy === "price") {
      result.sort((a, b) => a.hourly_price - b.hourly_price);
    } else if (filters.sortBy === "availability") {
      result.sort((a, b) => b.available_count - a.available_count);
    } else {
      result.sort((a, b) => a.name.localeCompare(b.name));
    }

    setFilteredLots(result);
  }, [lots, filters]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading parking data...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="sidebar">
        <Filters filters={filters} onFilterChange={handleFilterChange} />
        <div className="lot-count">{filteredLots.length} lots found</div>
        <ParkingList
          lots={filteredLots}
          onSelectLot={setSelectedLot}
          selectedLotId={selectedLot?.id}
        />
      </div>
      <div className="map-container">
        <ParkingMap
          lots={filteredLots}
          selectedLot={selectedLot}
          onSelectLot={setSelectedLot}
        />
        {selectedLot && (
          <ParkingDetail
            lot={selectedLot}
            onClose={() => setSelectedLot(null)}
          />
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
