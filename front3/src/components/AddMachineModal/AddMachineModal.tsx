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
  const [files, setFiles] = useState<File[]>([]);
  const [modalError, setModalError] = useState<string | null>(null);

  const handleSubmit = async () => {
    try {
      const created = await dispatch(
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

      if (created?.id && files.length > 0) {
        (async () => {
          try {
            await Promise.all(
              files.map((file) => {
                const form = new FormData();
                form.append("file", file);
                form.append("machine_id", String(created.id));
                form.append("description", "");
                return dispatch(imageActions.createImage(form)).catch((e) => {
                  console.warn("Failed to upload image:", file.name, e);
                  return null;
                });
              })
            );

            await dispatch(machineActions.getMachineDetails(created.id));
          } catch (e) {
            console.warn("Image upload failed:", e);
          }
        })();
      }
    } catch (err: any) {
      console.error("Create machine failed:", err);
      if (err?.response?.data?.detail) {
        setModalError(`Machine creation failed: ${err.response.data.detail}`);
      } else {
        setModalError("Something went wrong while creating the machine.");
      }
    } finally {
      setName("");
      setPrice("");
      setCondition("");
      setDescription("");
      setHoursUsed("");
      setFiles([]);
    }
  };

  return (
    <>
      <button
        onClick={() => {
          setModalError(null);
          setShowModal(true);
        }}
        className="add-machine-btn"
      >
        ADD MACHINE or PART
      </button>

      {showModal && (
        <BaseModal
          title="Add Machine or Part"
          onClose={() => setShowModal(false)}
          onSave={handleSubmit}
        >
          {modalError && <div className="modal-error">{modalError}</div>}
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

          <ImageUploader onUpload={(fs) => setFiles(fs)} multiple />
        </BaseModal>
      )}
    </>
  );
};

export default AddMachineModal;
