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
  price: number;
  condition: string;
  description: string;
  hours_used: number;
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
  const [price, setPrice] = useState(machine.price);
  const [condition, setCondition] = useState(machine.condition);
  const [description, setDescription] = useState(machine.description);
  const [hoursUsed, setHoursUsed] = useState(machine.hours_used);
  const [imageUrl, setImageUrl] = useState(machine.image_url);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    if (updatedMachine) {
      setName(updatedMachine.name);
      setPrice(updatedMachine.price);
      setCondition(updatedMachine.condition);
      setDescription(updatedMachine.description);
      setHoursUsed(updatedMachine.hours_used);
      setImageUrl(updatedMachine.image_url);
    }
  }, [updatedMachine]);

  const handleEdit = async () => {
    if (
      editing &&
      (name !== machine.name ||
        price !== machine.price ||
        condition !== machine.condition ||
        description !== machine.description ||
        hoursUsed !== machine.hours_used ||
        imageUrl !== machine.image_url)
    ) {
      await dispatch(
        machineActions.editMachine(machine.id, {
          name,
          price,
          condition,
          description,
          hours_used: hoursUsed,
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
          <input
            className="machine-edit-input"
            type="number"
            value={price}
            onChange={(e) => setPrice(Number(e.target.value))}
            placeholder="Price"
          />
          <input
            className="machine-edit-input"
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
            placeholder="Condition"
          />
          <textarea
            className="machine-edit-textarea"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <input
            className="machine-edit-input"
            type="number"
            value={hoursUsed}
            onChange={(e) => setHoursUsed(Number(e.target.value))}
            placeholder="Hours Used"
          />
          <input
            className="machine-edit-input"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="Image URL"
          />
        </div>
      ) : (
        <div key="view">
          <h3 className="machine-name">{name}</h3>
          <img src={imageUrl} alt={name} className="machine-image" />
          <p className="machine-description">{description}</p>
          <p className="machine-price">Price: ${price}</p>
          <p className="machine-condition">
            <strong>Condition:</strong> {condition}
          </p>
          <p className="machine-hours">Hours Used: {hoursUsed}</p>
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
