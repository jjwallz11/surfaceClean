import { useState } from "react";
import { useDispatch } from "react-redux";
import * as machineActions from "../../redux/machines";
import BaseModal from "../BaseModal/BaseModal";
import "../BaseModal/BaseModal.css";

const AddMachineModal = () => {
  const dispatch = useDispatch<any>();
  const [showModal, setShowModal] = useState(false);

  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [condition, setCondition] = useState("");
  const [description, setDescription] = useState("");
  const [hoursUsed, setHoursUsed] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const handleSubmit = async() => {
    dispatch(
      machineActions.createMachine({
        name,
        price: parseFloat(price),
        condition,
        description,
        hours_used: parseInt(hoursUsed),
      })
    );
    await dispatch(machineActions.getMachines());
    setShowModal(false);
  };

  return (
    <>
      {/* match FAQ button sizing/styling */}
      <button onClick={() => setShowModal(true)} className="add-machine-btn">
        ADD MACHINE
      </button>

      {showModal && (
        <BaseModal
          title="Add Machine"
          onClose={() => setShowModal(false)}
          onSave={handleSubmit}
        >
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
          <input
            className="modal-input"
            placeholder="Image URL"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
          />
        </BaseModal>
      )}
    </>
  );
};

export default AddMachineModal;