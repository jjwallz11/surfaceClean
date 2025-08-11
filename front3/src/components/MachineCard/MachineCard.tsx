// front3/src/components/MachineCard/MachineCard.tsx

import { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
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
  hours_used: number;
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
  const [hoursUsed, setHoursUsed] = useState(machine.hours_used);
  const [showConfirm, setShowConfirm] = useState(false);

  useEffect(() => {
    if (updatedMachine) {
      setName(updatedMachine.name);
      setPrice(updatedMachine.price);
      setCondition(updatedMachine.condition);
      setHoursUsed(updatedMachine.hours_used);
    }
  }, [updatedMachine]);

  const handleEdit = async () => {
    if (
      editing &&
      (name !== machine.name ||
        price !== machine.price ||
        condition !== machine.condition ||
        hoursUsed !== machine.hours_used)
    ) {
      await dispatch(
        machineActions.editMachine(machine.id, {
          name,
          price,
          condition,
          hours_used: hoursUsed,
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
          <input
            className="machine-edit-input"
            type="number"
            value={hoursUsed}
            onChange={(e) => setHoursUsed(Number(e.target.value))}
            placeholder="Hours Used"
          />
        </div>
      ) : (
        <NavLink
          to={`/machines/${machine.id}`}
          key="view"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          <div className="machine-details">
            <h3 className="machine-name">{name}</h3>
            <div className="machine-image-container">
              
            </div>
            <p className="machine-price">Price: ${price}</p>
            <p className="machine-condition">
              <strong>Condition:</strong> {condition}
            </p>
            <p className="machine-hours">Hours Used: {hoursUsed}</p>
          </div>
        </NavLink>
      )}

      {user && (
        <div className="machine-actions">
          <button onClick={handleEdit} className="btn-edit">
            {editing ? "Save" : "EDIT"}
          </button>
          <button onClick={handleDelete} className="btn-delete">
            DELETE
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
