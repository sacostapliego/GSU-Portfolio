import React, { useState, useEffect, useCallback } from "react";
import { fetchParkingLots, createLot, updateLot, deleteLot } from "../api";
import AdminLotForm from "./AdminLotForm";

export default function AdminPanel() {
  const [lots, setLots] = useState([]);
  const [editing, setEditing] = useState(null); // null = not editing, {} = new, lot = editing
  const [loading, setLoading] = useState(true);

  const loadLots = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchParkingLots();
      setLots(data);
    } catch (err) {
      console.error("Failed to load lots:", err);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadLots();
  }, [loadLots]);

  const handleSubmit = async (data) => {
    try {
      if (editing && editing.id) {
        await updateLot(editing.id, data);
      } else {
        await createLot(data);
      }
      setEditing(null);
      loadLots();
    } catch (err) {
      console.error("Failed to save:", err);
      alert("Failed to save parking lot.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this parking lot?")) return;
    try {
      await deleteLot(id);
      loadLots();
    } catch (err) {
      console.error("Failed to delete:", err);
    }
  };

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h2>Manage Parking Lots</h2>
        <button className="btn btn-primary" onClick={() => setEditing({})}>
          + Add New Lot
        </button>
      </div>

      {editing !== null && (
        <AdminLotForm
          lot={editing.id ? editing : null}
          onSubmit={handleSubmit}
          onCancel={() => setEditing(null)}
        />
      )}

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Address</th>
              <th>Type</th>
              <th>Price</th>
              <th>Spots</th>
              <th>Available</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {lots.map((lot) => (
              <tr key={lot.id}>
                <td>{lot.name}</td>
                <td>{lot.address}</td>
                <td>{lot.is_small_lot ? "Small" : "Large"}</td>
                <td>${lot.hourly_price.toFixed(2)}</td>
                <td>{lot.slot_count}</td>
                <td>{lot.available_count}</td>
                <td>
                  <button
                    className="btn-icon"
                    onClick={() => setEditing(lot)}
                    title="Edit"
                  >
                    Edit
                  </button>
                  <button
                    className="btn-icon btn-danger"
                    onClick={() => handleDelete(lot.id)}
                    title="Delete"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
