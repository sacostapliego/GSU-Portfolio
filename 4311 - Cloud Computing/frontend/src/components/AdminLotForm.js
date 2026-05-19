import React, { useState, useEffect } from "react";

const EMPTY_FORM = {
  name: "",
  address: "",
  is_small_lot: false,
  hourly_price: "",
  website: "",
  slot_count: "",
  occupied_count: "0",
  latitude: "",
  longitude: "",
};

export default function AdminLotForm({ lot, onSubmit, onCancel }) {
  const [form, setForm] = useState(EMPTY_FORM);

  useEffect(() => {
    if (lot) {
      setForm({
        name: lot.name,
        address: lot.address,
        is_small_lot: lot.is_small_lot,
        hourly_price: String(lot.hourly_price),
        website: lot.website || "",
        slot_count: String(lot.slot_count),
        occupied_count: String(lot.occupied_count),
        latitude: String(lot.latitude),
        longitude: String(lot.longitude),
      });
    } else {
      setForm(EMPTY_FORM);
    }
  }, [lot]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: form.name,
      address: form.address,
      is_small_lot: form.is_small_lot,
      hourly_price: parseFloat(form.hourly_price),
      website: form.website || null,
      slot_count: parseInt(form.slot_count),
      occupied_count: parseInt(form.occupied_count),
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
    });
  };

  return (
    <form className="admin-form" onSubmit={handleSubmit}>
      <h3>{lot ? "Edit Parking Lot" : "Add New Parking Lot"}</h3>

      <div className="form-row">
        <div className="form-group">
          <label>Name</label>
          <input name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Address</label>
          <input name="address" value={form.address} onChange={handleChange} required />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Hourly Price ($)</label>
          <input name="hourly_price" type="number" step="0.5" min="0" value={form.hourly_price} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Website</label>
          <input name="website" value={form.website} onChange={handleChange} />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Total Spots</label>
          <input name="slot_count" type="number" min="1" value={form.slot_count} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Occupied Spots</label>
          <input name="occupied_count" type="number" min="0" value={form.occupied_count} onChange={handleChange} required />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Latitude</label>
          <input name="latitude" type="number" step="any" value={form.latitude} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Longitude</label>
          <input name="longitude" type="number" step="any" value={form.longitude} onChange={handleChange} required />
        </div>
      </div>

      <div className="form-group checkbox-group">
        <label>
          <input name="is_small_lot" type="checkbox" checked={form.is_small_lot} onChange={handleChange} />
          Small Lot
        </label>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          {lot ? "Update" : "Create"}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}
