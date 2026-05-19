import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Fix Leaflet default marker icons (webpack issue)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

function getMarkerIcon(lot) {
  const pct = lot.available_count / lot.slot_count;
  let color;
  if (pct <= 0) color = "#6b7280";      // gray - full
  else if (pct < 0.2) color = "#ef4444"; // red
  else if (pct < 0.5) color = "#f59e0b"; // yellow
  else color = "#22c55e";                 // green

  return L.divIcon({
    className: "custom-marker",
    html: `<div style="
      background: ${color};
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 11px;
      font-weight: bold;
    ">${lot.available_count}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

export default function ParkingMap({ lots, selectedLot, onSelectLot }) {
  const center = [33.749, -84.388];

  return (
    <MapContainer
      center={center}
      zoom={14}
      className="parking-map"
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {lots.map((lot) => (
        <Marker
          key={lot.id}
          position={[lot.latitude, lot.longitude]}
          icon={getMarkerIcon(lot)}
          eventHandlers={{ click: () => onSelectLot(lot) }}
        >
          <Popup>
            <div className="map-popup">
              <h3>{lot.name}</h3>
              <p>{lot.address}</p>
              <p>
                <strong>${lot.hourly_price.toFixed(2)}/hr</strong>
              </p>
              <p>
                {lot.available_count}/{lot.slot_count} spots available
              </p>
              {lot.is_small_lot && <p><em>Small Lot</em></p>}
              <a
                href={`https://www.google.com/maps/dir/?api=1&destination=${lot.latitude},${lot.longitude}`}
                target="_blank"
                rel="noopener noreferrer"
                className="directions-link"
              >
                Get Directions
              </a>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
