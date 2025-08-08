// front3/src/pages/MachineDetailsPage/MachineDetailsPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { machineActions } from "../../redux";
import { RootState } from "../../redux/store";

const MachineDetailsPage = () => {
  const { machineId } = useParams<{ machineId: string }>();
  const dispatch = useDispatch<any>();
  const navigate = useNavigate();

  const machine = useSelector(
    (state: RootState) => state.machines.single.details
  );

  useEffect(() => {
    if (machineId) dispatch(machineActions.getMachineDetails(machineId));
  }, [dispatch, machineId]);

  if (!machine || !machine.id) return <div>Loading...</div>;

  return (
    <div>
      <button onClick={() => navigate("/machines")}>Back to Machines</button>
      <h1>{machine.name}</h1>
      <img
        src={machine.image_url || "/placeholder.jpg"}
        alt={machine.name}
      />
      <p><strong>Condition:</strong> {machine.condition}</p>
      <p><strong>Price:</strong> ${machine.price}</p>
      {machine.hours_used !== null && (
        <p><strong>Hours Used:</strong> {machine.hours_used}</p>
      )}
      {machine.description && (
        <p><strong>Description:</strong> {machine.description}</p>
      )}
    </div>
  );
};

export default MachineDetailsPage;