// front3/src/components/ChangePasswordModal/ChangePasswordModal.tsx
import { useState } from "react";
import BaseModal from "../BaseModal/BaseModal";
import { csrfFetch } from "../../redux/csrf";
import "../BaseModal/BaseModal.css";

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
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
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
      <input
        className="modal-input"
        type="password"
        placeholder="Current password"
        value={currentPassword}
        onChange={(e) => setCurrentPassword(e.target.value)}
      />
      <input
        className="modal-input"
        type="password"
        placeholder="New password"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
      />
      <input
        className="modal-input"
        type="password"
        placeholder="Confirm new password"
        value={confirm}
        onChange={(e) => setConfirm(e.target.value)}
      />
      {error && <p style={{ color: "#AE2335", marginTop: 8 }}>{error}</p>}
      {saving && <p>Saving…</p>}
    </BaseModal>
  );
}