// front3/src/components/MachineCard/MachineCard.tsx

import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { machineActions } from "../../redux";
import ConfirmationModal from "../ConfirmationModal/ConfirmationModal";
import "./MachineCard.css";

interface Machine {
  id: number;
  name: string;
  description: string;
  image_url: string;
  created_at: string;
}

interface MachineCardProps {
  machine: Machine;
}

const MachineCard = ({ machine }: MachineCardProps) => {
  const dispatch = useDispatch<any>();
  const user = useSelector((state: RootState) => state.session.user);
  const updatedMachine = useSelector(
    (state: RootState) => state.machines.all[machine.id]
  );

  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(machine.name);
  const [description, setDescription] = useState(machine.description);
  const [imageUrl, setImageUrl] = useState(machine.image_url);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    if (updatedMachine) {
      setName(updatedMachine.name);
      setDescription(updatedMachine.description);
      setImageUrl(updatedMachine.image_url);
    }
  }, [updatedMachine]);

  const handleEdit = async () => {
    if (
      editing &&
      (name !== machine.name ||
        description !== machine.description ||
        imageUrl !== machine.image_url)
    ) {
      await dispatch(
        machineActions.editMachine(machine.id, {
          name,
          description,
          image_url: imageUrl,
        })
      );
    }
    setEditing(!editing);
  };

  const handleDelete = () => {
    setShowConfirm(true);
  };

  const confirmDelete = () => {
    dispatch(machineActions.removeMachine(machine.id));
    setShowConfirm(false);
  };

  return (
    <div className="machine-card">
      {editing ? (
        <div key="edit">
          <input
            className="machine-edit-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <textarea
            className="machine-edit-textarea"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <input
            className="machine-edit-input"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
          />
        </div>
      ) : (
        <div key="view">
          <h3 className="machine-name">{name}</h3>
          <img src={imageUrl} alt={name} className="machine-image" />
          <p className="machine-description">{description}</p>
        </div>
      )}

      {user && (
        <div className="machine-actions">
          <button onClick={handleEdit} className="btn-edit">
            {editing ? "Save" : "Edit"}
          </button>
          <button onClick={handleDelete} className="btn-delete">
            Delete
          </button>
        </div>
      )}

      {showConfirm && (
        <ConfirmationModal
          title="Confirm Deletion"
          message="Are you sure you want to delete this machine?"
          onConfirm={confirmDelete}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
};

export default MachineCard;