import React from "react";

export default function Filters({ filters, onFilterChange }) {
  return (
    <div className="filters">
      <h3>Filters</h3>

      <div className="filter-group">
        <label>Lot Type</label>
        <select
          value={filters.lotType}
          onChange={(e) => onFilterChange("lotType", e.target.value)}
        >
          <option value="all">All Lots</option>
          <option value="small">Small Lots Only</option>
          <option value="large">Large Lots Only</option>
        </select>
      </div>

      <div className="filter-group">
        <label>Max Price: ${filters.maxPrice}/hr</label>
        <input
          type="range"
          min="1"
          max="30"
          value={filters.maxPrice}
          onChange={(e) => onFilterChange("maxPrice", Number(e.target.value))}
        />
      </div>

      <div className="filter-group">
        <label>Sort By</label>
        <select
          value={filters.sortBy}
          onChange={(e) => onFilterChange("sortBy", e.target.value)}
        >
          <option value="name">Name</option>
          <option value="price">Price (Low to High)</option>
          <option value="availability">Availability</option>
        </select>
      </div>
    </div>
  );
}
