import { useState } from "react";
import { useDispatch } from "react-redux";
import * as machineActions from "../../redux/machines";
import BaseModal from "../BaseModal/BaseModal";

const AddMachineModal = () => {
  const dispatch = useDispatch<any>();
  const [showModal, setShowModal] = useState(false);

  const [name, setName] = useState("");
  const [price, setPrice] = useState(0);
  const [condition, setCondition] = useState("");
  const [description, setDescription] = useState("");
  const [hoursUsed, setHoursUsed] = useState(0);
  const [imageUrl, setImageUrl] = useState("");

  const handleSubmit = () => {
    dispatch(
      machineActions.createMachine({
        name,
        price,
        condition,
        description,
        hours_used: hoursUsed,
        image_url: imageUrl,
      })
    );
    setShowModal(false);
  };

  return (
    <>
      <button onClick={() => setShowModal(true)} className="btn-add">
        Add Machine
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
            onChange={(e) => setPrice(parseFloat(e.target.value))}
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
            onChange={(e) => setHoursUsed(parseInt(e.target.value))}
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
