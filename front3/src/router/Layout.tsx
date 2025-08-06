import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { RootState } from "../redux/store";
import { thunkLogout, getCurrentUser } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";

export default function Layout() {
  const dispatch = useDispatch<any>();
  const user = useSelector((state: RootState) => state.session.user);

  useEffect(() => {
    dispatch(getCurrentUser());
  }, [dispatch]);

  useEffect(() => {
    console.log("Layout: user is", user);
  }, [user]);

  const handleLogout = () => {
    dispatch(thunkLogout());
  };

  return (
    <ModalProvider>
      {user && (
        <div
          style={{
            backgroundColor: "#AE2335", // Patriotic Red
            color: "white",
            padding: "8px 16px",
            textAlign: "center",
            fontWeight: "bold",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <span>ADMIN MODE - ACTIVATED</span>
          <button
            onClick={handleLogout}
            style={{
              backgroundColor: "white",
              color: "#AE2335",
              border: "none",
              padding: "6px 12px",
              cursor: "pointer",
              fontWeight: "bold",
              borderRadius: "4px",
            }}
          >
            Logout
          </button>
        </div>
      )}

      <Navigation />

      <div className="content-container">
        <Outlet />
      </div>

      <Modal />
    </ModalProvider>
  );
}