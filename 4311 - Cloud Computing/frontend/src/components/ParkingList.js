import React from "react";

function getAvailabilityClass(lot) {
  const pct = lot.available_count / lot.slot_count;
  if (pct <= 0) return "status-full";
  if (pct < 0.2) return "status-low";
  if (pct < 0.5) return "status-medium";
  return "status-high";
}

export default function ParkingList({ lots, onSelectLot, selectedLotId }) {
  if (!lots.length) {
    return <div className="parking-list-empty">No parking lots found.</div>;
  }

  return (
    <div className="parking-list">
      {lots.map((lot) => (
        <div
          key={lot.id}
          className={`parking-card ${selectedLotId === lot.id ? "selected" : ""}`}
          onClick={() => onSelectLot(lot)}
        >
          <div className="parking-card-header">
            <h4>{lot.name}</h4>
            {lot.is_small_lot && <span className="badge-small">Small Lot</span>}
          </div>
          <p className="parking-card-address">{lot.address}</p>
          <div className="parking-card-details">
            <span className="parking-card-price">
              ${lot.hourly_price.toFixed(2)}/hr
            </span>
            <span className={`parking-card-availability ${getAvailabilityClass(lot)}`}>
              {lot.available_count}/{lot.slot_count} available
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
