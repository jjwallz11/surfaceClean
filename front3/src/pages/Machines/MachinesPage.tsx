// front3/src/pages/MachinesPage/MachinesPage.tsx

import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import {
  getMachines,
  removeMachine,
  editMachine,
} from "../../redux/machines";
import ConfirmationModal from "../../components/ConfirmationModal/ConfirmationModal";
import { useModal } from "../../context/Modal";
import MachineCard from "../../components/MachineCard/MachineCard";
import "./MachinesPage.css";

const MachinesPage = () => {
  const dispatch = useDispatch<any>();
  const { setModalContent } = useModal();
  const machines = useSelector((state: RootState) => state.machines.all);
  const user = useSelector((state: RootState) => state.session.user);

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editFields, setEditFields] = useState({
    name: "",
    price: "",
    description: "",
    hours_used: "",
  });

  const editRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    dispatch(getMachines());
  }, [dispatch]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        editRef.current &&
        !editRef.current.contains(e.target as Node)
      ) {
        setEditingId(null);
      }
    };
    if (editingId !== null) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [editingId]);

  const machineList = Object.values(machines || {});

  const handleEdit = async (id: number) => {
    await dispatch(editMachine(id, {
      name: editFields.name,
      price: parseFloat(editFields.price),
      description: editFields.description,
      hours_used: parseFloat(editFields.hours_used),
    }));
    setEditingId(null);
  };

  const handleDelete = (id: number) => {
    setModalContent(
      <ConfirmationModal
        title="Confirm Delete"
        message="Are you sure you want to delete this machine?"
        onConfirm={() => dispatch(removeMachine(id))}
        onCancel={() => setModalContent(null)}
      />
    );
  };

  return (
    <div className="machines-page-container">
      <h1>Machines</h1>
      <div className="machines-grid">
        {machineList.map((machine) => (
          <div key={machine.id} className="machine-wrapper">
            <MachineCard machine={machine} />
            {user && (
              <div className="admin-controls" ref={editRef}>
                {editingId === machine.id ? (
                  <>
                    <input
                      type="text"
                      value={editFields.name}
                      onChange={(e) =>
                        setEditFields({ ...editFields, name: e.target.value })
                      }
                      placeholder="Name"
                    />
                    <input
                      type="text"
                      value={editFields.price}
                      onChange={(e) =>
                        setEditFields({ ...editFields, price: e.target.value })
                      }
                      placeholder="Price"
                    />
                    <input
                      type="text"
                      value={editFields.description}
                      onChange={(e) =>
                        setEditFields({ ...editFields, description: e.target.value })
                      }
                      placeholder="Description"
                    />
                    <input
                      type="text"
                      value={editFields.hours_used}
                      onChange={(e) =>
                        setEditFields({ ...editFields, hours_used: e.target.value })
                      }
                      placeholder="Hours Used"
                    />
                    <button onClick={() => handleEdit(machine.id)}>Save</button>
                    <button onClick={() => setEditingId(null)}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => {
                      setEditFields({
                        name: machine.name,
                        price: machine.price.toString(),
                        description: machine.description,
                        hours_used: machine.hours_used.toString()
                      });
                      setEditingId(machine.id);
                    }}>
                      Edit
                    </button>
                    <button onClick={() => handleDelete(machine.id)}>Delete</button>
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MachinesPage;