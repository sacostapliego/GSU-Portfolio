import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

export const fetchParkingLots = (params = {}) =>
  API.get("/parking", { params }).then((r) => r.data);

export const fetchCheapestLots = () =>
  API.get("/parking/cheapest").then((r) => r.data);

export const fetchSmallLots = () =>
  API.get("/parking/small").then((r) => r.data);

export const fetchNearbyLots = (lat, lng, radius = 2) =>
  API.get("/parking/nearby", { params: { lat, lng, radius } }).then(
    (r) => r.data
  );

export const fetchLotById = (id) =>
  API.get(`/parking/${id}`).then((r) => r.data);

export const createLot = (data) =>
  API.post("/admin/parking", data).then((r) => r.data);

export const updateLot = (id, data) =>
  API.put(`/admin/parking/${id}`, data).then((r) => r.data);

export const deleteLot = (id) => API.delete(`/admin/parking/${id}`);

export default API;
