// front3/src/pages/MachinesPage/MachinesPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { getMachines } from "../../redux/machines";
import MachineCard from "../../components/MachineCard/MachineCard";
import "./MachinesPage.css";

const MachinesPage = () => {
  const dispatch = useDispatch<any>();
  const machines = useSelector((state: RootState) =>
    Object.values(state.machines.all)
  );

  useEffect(() => {
    dispatch(getMachines());
  }, [dispatch]);

  return (
    <div className="machines-page">
      <h1>Machines</h1>
      <div className="machine-list">
        {machines.map((machine) => (
          <MachineCard key={machine.id} machine={machine} />
        ))}
      </div>
    </div>
  );
};

export default MachinesPage;