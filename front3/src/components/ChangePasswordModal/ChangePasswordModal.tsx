// front3/src/components/ChangePasswordModal/ChangePasswordModal.tsx
import { useState } from "react";
import BaseModal from "../BaseModal/BaseModal";
import { csrfFetch } from "../../redux/csrf";
import "../BaseModal/BaseModal.css";
import "./ChangePasswordModal.css"; // ⬅️ add a tiny style file below

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function ChangePasswordModal({ open, onClose }: Props) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // visibility toggles
  const [showCurrent, setShowCurrent] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const onSave = async () => {
    setError(null);
    if (newPassword !== confirm) {
      setError("New passwords do not match.");
      return;
    }
    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    try {
      setSaving(true);
      const res = await csrfFetch("/api/session/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (!res.ok) throw new Error("Failed to change password");
      onClose();
    } catch (e: any) {
      setError(e?.message || "Unable to change password");
    } finally {
      setSaving(false);
    }
  };

  if (!open) return null;

  return (
    <BaseModal title="Change Password" onClose={onClose} onSave={onSave}>
      <label className="pw-label">Current password</label>
      <div className="pw-input-wrap">
        <input
          className="modal-input pw-input"
          type={showCurrent ? "text" : "password"}
          placeholder="Current password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          autoComplete="current-password"
        />
        <button
          type="button"
          className="pw-toggle"
          onClick={() => setShowCurrent((s) => !s)}
          aria-label={showCurrent ? "Hide current password" : "Show current password"}
        >
          {showCurrent ? "🙈" : "👁️"}
        </button>
      </div>

      <label className="pw-label">New password</label>
      <div className="pw-input-wrap">
        <input
          className="modal-input pw-input"
          type={showNew ? "text" : "password"}
          placeholder="New password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          autoComplete="new-password"
        />
        <button
          type="button"
          className="pw-toggle"
          onClick={() => setShowNew((s) => !s)}
          aria-label={showNew ? "Hide new password" : "Show new password"}
        >
          {showNew ? "🙈" : "👁️"}
        </button>
      </div>

      <label className="pw-label">Confirm new password</label>
      <div className="pw-input-wrap">
        <input
          className="modal-input pw-input"
          type={showConfirm ? "text" : "password"}
          placeholder="Confirm new password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          autoComplete="new-password"
        />
        <button
          type="button"
          className="pw-toggle"
          onClick={() => setShowConfirm((s) => !s)}
          aria-label={showConfirm ? "Hide confirmed password" : "Show confirmed password"}
        >
          {showConfirm ? "🙈" : "👁️"}
        </button>
      </div>

      {error && <p style={{ color: "#AE2335", marginTop: 8 }}>{error}</p>}
      {saving && <p>Saving…</p>}
    </BaseModal>
  );
}