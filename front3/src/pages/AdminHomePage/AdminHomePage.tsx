// src/pages/AdminHomePage/AdminHomePage.tsx

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { useModal } from "../../context/Modal";
import LoginModal from "../../components/LoginModal/LoginModal";
import "./AdminHomePage.css";

function AdminHomePage() {
  const navigate = useNavigate();
  const { setModalContent } = useModal();
  const user = useSelector((state: RootState) => state.session.user);

  useEffect(() => {
    if (!user) {
      setModalContent(<LoginModal />);
    }
  }, [user, setModalContent]);

  const adminLinks = [
    { path: "/machines", label: "🧹 Manage Machines" },
    { path: "/testimonials", label: "⭐ Manage Testimonials" },
    { path: "/faqs", label: "❓ Manage FAQs" },
  ];

  return (
    <div className="admin-home-container">
      <h2 className="admin-home-heading">Admin Dashboard</h2>
      <div className="admin-home-buttons">
        {adminLinks.map(({ path, label }) => (
          <button
            key={path}
            className="admin-home-button"
            onClick={() => navigate(path)}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default AdminHomePage;