import React from "react";
import "./BaseModal.css";

interface BaseModalProps {
  title?: string;
  onClose: () => void;
  onSave?: () => void;
  showButtons?: boolean;
  children: React.ReactNode;
}

const BaseModal = ({
  title,
  onClose,
  onSave,
  showButtons = true,
  children,
}: BaseModalProps) => {
  return (
    <div className="modal-overlay">
      <div className="modal-container">
        {title && <h2 className="modal-title">{title}</h2>}
        <div className="modal-content">{children}</div>

        {showButtons && (
          <div className="modal-buttons">
            <button className="btn-edit" onClick={onSave}>
              SAVE
            </button>
            <button className="btn-delete" onClick={onClose}>
              CANCEL
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BaseModal;