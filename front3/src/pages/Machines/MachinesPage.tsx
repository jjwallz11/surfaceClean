// front3/src/pages/MachinesPage/MachinesPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { machineActions } from "../../redux";
import { NavLink } from "react-router-dom";

const MachinesPage = () => {
  const dispatch = useDispatch<any>();
  const machines = useSelector((state: RootState) =>
    Object.values(state.machines.all)
  );

  useEffect(() => {
    dispatch(machineActions.getMachines());
  }, [dispatch]);

  return (
    <div>
      <h1>Available Machines</h1>
      <ul>
        {machines.map((machine) => (
          <li key={machine.id}>
            <NavLink to={`/machines/${machine.id}`}>
              <img
                src={machine.image_url || "/placeholder.jpg"}
                alt={machine.name}
              />
              <div>
                <h3>{machine.name}</h3>
                <p>${machine.price}</p>
                <p>{machine.condition}</p>
              </div>
            </NavLink>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MachinesPage;