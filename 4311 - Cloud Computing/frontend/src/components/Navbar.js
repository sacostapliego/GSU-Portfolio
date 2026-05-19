import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="navbar-icon">P</span>
        <Link to="/">Smart Parking Finder</Link>
      </div>
      <div className="navbar-links">
        <Link to="/" className={location.pathname === "/" ? "active" : ""}>
          Map
        </Link>
        <Link
          to="/admin"
          className={location.pathname === "/admin" ? "active" : ""}
        >
          Admin
        </Link>
      </div>
    </nav>
  );
}
