// components/LogoutButton/LogoutButton.tsx

import { useDispatch } from "react-redux";
import { thunkLogout } from "../../redux/session";

function LogoutButton() {
  const dispatch = useDispatch<any>();

  const handleLogout = () => {
    dispatch(thunkLogout());
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Logout
    </button>
  );
}

export default LogoutButton;