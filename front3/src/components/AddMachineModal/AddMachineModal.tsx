// front3/src/components/AddMachineModal/AddMachineModal.tsx
import { useState } from "react";
import { useDispatch } from "react-redux";
import * as machineActions from "../../redux/machines";
import * as imageActions from "../../redux/images";
import ImageUploader from "../ImageUploader/ImageUploader";
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
  const [files, setFiles] = useState<File[]>([]); // ⬅️ new

  const handleSubmit = async () => {
    // 1️⃣ Create the machine first
    const created = await dispatch(
      machineActions.createMachine({
        name,
        price: parseFloat(price),
        condition,
        description,
        hours_used: parseInt(hoursUsed),
      })
    );

    // 2️⃣ If we have files, upload them
    if (created?.id && files.length > 0) {
      const form = new FormData();
      form.append("file", files[0]);
      form.append("machine_id", String(created.id));
      form.append("description", ""); // required by backend

      await dispatch(imageActions.createImage(form));
    }

    // 3️⃣ Refresh machines and close
    await dispatch(machineActions.getMachines());
    setShowModal(false);
  };

  return (
    <>
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

          {/* ⬇️ replace Image URL input with the uploader */}
          <ImageUploader onUpload={(fs) => setFiles(fs)} multiple />
        </BaseModal>
      )}
    </>
  );
};

export default AddMachineModal;
