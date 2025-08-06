// components/LoginModal/LoginModal.tsx

import { useState, FormEvent } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkLogin } from "../../redux/session";
import "./LoginModal.css";

function LoginModal() {
  const dispatch = useDispatch<any>();
  const { closeModal } = useModal();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const serverResponse = await dispatch(
      thunkLogin({ email, password }) as any
    );

    if (serverResponse) {
      setErrors(serverResponse);
    } else {
      closeModal();
      navigate("/");
    }
  };

  return (
    <div className="login-modal">
      <h1>Admin Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        {errors.email && <p className="error-message">{errors.email}</p>}

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {errors.password && <p className="error-message">{errors.password}</p>}

        <button type="submit" className="login-modal-btn">
          Log In
        </button>
      </form>
    </div>
  );
}

export default LoginModal;