// front3/src/pages/MachinesPage/MachinesPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { machineActions } from "../../redux";
import MachineCard from "../../components/MachineCard/MachineCard";
import "./MachinesPage.css";

const MachinesPage = () => {
  const dispatch = useDispatch<any>();
  const machines = useSelector((state: RootState) =>
    Object.values(state.machines.all)
  );

  useEffect(() => {
    dispatch(machineActions.getMachines());
  }, [dispatch]);

  return (
    <div className="machines-page">
      <h1>Available Machines</h1>
      <ul className="machine-list">
        {machines.map((machine) => (
          <li key={machine.id}>
            <MachineCard machine={machine} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MachinesPage;