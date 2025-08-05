// components/Navigation/Navigation.tsx

import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import "./Navigation.css";

function Navigation() {
  const user = useSelector((state: RootState) => state.session.user);
  const location = useLocation();
  const navigate = useNavigate();

  const isAdmin = !!user;

  const pageTitles: Record<string, string> = {
    "/": "Surface Clean",
    "/admin": "🔒 Admin",
    "/machines": "🧹 Machines",
    "/images": "🖼️ Images",
    "/testimonials": "⭐ Testimonials",
    "/faqs": "❓ FAQs",
  };

  const currentTitle = pageTitles[location.pathname] || "Surface Clean";

  return (
    <nav className="navbar">
      <button className="brand-btn" onClick={() => navigate("/")}>
        <img src="/logo192.png" alt="Surface Clean" className="brand-logo" />
      </button>

      <h1 className="nav-title">{currentTitle}</h1>

      {isAdmin && (
        <ul className="nav-list">
          <li>
            <NavLink to="/" className="nav-link">
              Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/machines" className="nav-link">
              Machines
            </NavLink>
          </li>
          <li>
            <NavLink to="/images" className="nav-link">
              Images
            </NavLink>
          </li>
          <li>
            <NavLink to="/testimonials" className="nav-link">
              Testimonials
            </NavLink>
          </li>
          <li>
            <NavLink to="/faqs" className="nav-link">
              FAQs
            </NavLink>
          </li>
        </ul>
      )}
    </nav>
  );
}

export default Navigation;