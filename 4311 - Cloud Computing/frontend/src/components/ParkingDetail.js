import React from "react";

export default function ParkingDetail({ lot, onClose }) {
  if (!lot) return null;

  const pct = lot.available_count / lot.slot_count;
  let statusLabel, statusClass;
  if (pct <= 0) { statusLabel = "FULL"; statusClass = "status-full"; }
  else if (pct < 0.2) { statusLabel = "Almost Full"; statusClass = "status-low"; }
  else if (pct < 0.5) { statusLabel = "Filling Up"; statusClass = "status-medium"; }
  else { statusLabel = "Available"; statusClass = "status-high"; }

  return (
    <div className="parking-detail">
      <button className="detail-close" onClick={onClose}>&times;</button>
      <h2>{lot.name}</h2>
      {lot.is_small_lot && <span className="badge-small">Small Lot</span>}
      <p className="detail-address">{lot.address}</p>

      <div className="detail-stats">
        <div className="detail-stat">
          <span className="detail-stat-value">${lot.hourly_price.toFixed(2)}</span>
          <span className="detail-stat-label">Per Hour</span>
        </div>
        <div className="detail-stat">
          <span className={`detail-stat-value ${statusClass}`}>
            {lot.available_count}
          </span>
          <span className="detail-stat-label">Spots Open</span>
        </div>
        <div className="detail-stat">
          <span className="detail-stat-value">{lot.slot_count}</span>
          <span className="detail-stat-label">Total Spots</span>
        </div>
      </div>

      <div className={`detail-status ${statusClass}`}>{statusLabel}</div>

      <div className="detail-actions">
        <a
          href={`https://www.google.com/maps/dir/?api=1&destination=${lot.latitude},${lot.longitude}`}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-primary"
        >
          Get Directions
        </a>
        {lot.website && (
          <a
            href={lot.website}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary"
          >
            Visit Website
          </a>
        )}
      </div>

      {lot.last_updated && (
        <p className="detail-updated">
          Last updated: {new Date(lot.last_updated).toLocaleString()}
        </p>
      )}
    </div>
  );
}
