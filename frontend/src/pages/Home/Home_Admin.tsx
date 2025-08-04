import { useAuth } from "../../hooks/useAuth";
import LoginModal from "../../components/Admin/LoginModal";
import AdminBanner from "../../components/Admin/AdminBanner";

const HomeAdmin = () => {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="home-admin">
      {isLoggedIn ? (
        <>
          <AdminBanner />
          <h1>Welcome to the Admin Dashboard</h1>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <LoginModal />
      )}
    </div>
  );
};

export default HomeAdmin;