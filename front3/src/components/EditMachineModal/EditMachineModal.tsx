import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import * as machineActions from "../../redux/machines";
import BaseModal from "../BaseModal/BaseModal";
import "../BaseModal/BaseModal.css";

interface Machine {
  id: number;
  name: string;
  price: number;
  condition: string;
  description: string;
  hours_used: number;
}

interface Props {
  machine: Machine;
  open: boolean;
  onClose: () => void;
}

export default function EditMachineModal({ machine, open, onClose }: Props) {
  const dispatch = useDispatch<any>();

  // prefill with existing values
  const [name, setName] = useState(machine.name);
  const [price, setPrice] = useState(String(machine.price));
  const [condition, setCondition] = useState(machine.condition);
  const [description, setDescription] = useState(machine.description);
  const [hoursUsed, setHoursUsed] = useState(
    machine.hours_used !== null && machine.hours_used !== undefined
      ? String(machine.hours_used)
      : ""
  );

  // keep modal in sync if parent passes a different machine
  useEffect(() => {
    setName(machine.name);
    setPrice(String(machine.price));
    setCondition(machine.condition);
    setDescription(machine.description);
    setHoursUsed(
      machine.hours_used !== null && machine.hours_used !== undefined
        ? String(machine.hours_used)
        : ""
    );
  }, [machine]);

  const handleSave = async () => {
    await dispatch(
      machineActions.editMachine(machine.id, {
        name,
        price: parseFloat(price),
        condition,
        description,
        hours_used: hoursUsed === "" ? null as any : Number(hoursUsed),
      })
    );
    // optional: refresh the list so cards reflect server truth
    await dispatch(machineActions.getMachines());
    onClose();
  };

  if (!open) return null;

  return (
    <BaseModal title="Edit Machine" onClose={onClose} onSave={handleSave}>
      <input
        className="modal-input"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        className="modal-input"
        placeholder="Price"
        type="number"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <input
        className="modal-input"
        placeholder="Condition"
        value={condition}
        onChange={(e) => setCondition(e.target.value)}
      />
      <textarea
        className="modal-textarea"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        className="modal-input"
        placeholder="Hours Used"
        type="number"
        value={hoursUsed}
        onChange={(e) => setHoursUsed(e.target.value)}
      />
    </BaseModal>
  );
}