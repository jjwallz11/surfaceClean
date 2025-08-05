// src/router/Layout.tsx

import { Outlet, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { RootState } from "../redux/store";

export default function Layout() {
  const location = useLocation();
  const user = useSelector((state: RootState) => state.session.user);
  const isAdminRoute = location.pathname.startsWith("/admin");

  return (
    <ModalProvider>
      {isAdminRoute && user && <div className="admin-banner">ADMIN MODE - ACTIVATED</div>}
      <div className="content-container">
        <Outlet />
      </div>
      <Modal />
    </ModalProvider>
  );
}