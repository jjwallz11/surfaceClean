// src/router/Layout.tsx

import { Outlet, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { RootState } from "../redux/store";
import { thunkLogout } from "../redux/session";

export default function Layout() {
  const location = useLocation();
  const dispatch = useDispatch<any>();
  const user = useSelector((state: RootState) => state.session.user);
  const isAdminRoute = location.pathname.startsWith("/admin");

  const handleLogout = () => {
    dispatch(thunkLogout());
  };

  return (
    <ModalProvider>
      {isAdminRoute && user && (
        <div className="admin-banner">
          <span>ADMIN MODE - ACTIVATED</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      )}
      <div className="content-container">
        <Outlet />
      </div>
      <Modal />
    </ModalProvider>
  );
}