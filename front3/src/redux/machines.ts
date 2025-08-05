// redux/machines.ts

/******************************* TYPES *******************************************/

interface Machine {
  id: number;
  name: string;
  price: number;
  description: string;
  hours_used: number;
  created_at: string;
}

interface MachinesState {
  all: Record<number, Machine>;
}

interface LoadMachinesAction {
  type: typeof LOAD_MACHINES;
  payload: Machine[];
}

interface AddMachineAction {
  type: typeof ADD_MACHINE;
  payload: Machine;
}

interface UpdateMachineAction {
  type: typeof UPDATE_MACHINE;
  payload: Machine;
}

interface DeleteMachineAction {
  type: typeof DELETE_MACHINE;
  payload: number;
}

type MachinesActionTypes =
  | LoadMachinesAction
  | AddMachineAction
  | UpdateMachineAction
  | DeleteMachineAction;

/******************************* ACTION TYPES *******************************************/

const LOAD_MACHINES = 'machines/load';
const ADD_MACHINE = 'machines/add';
const UPDATE_MACHINE = 'machines/update';
const DELETE_MACHINE = 'machines/delete';

/******************************* ACTION CREATORS *******************************************/

export const loadMachines = (machines: Machine[]): LoadMachinesAction => ({
  type: LOAD_MACHINES,
  payload: machines,
});

export const addMachine = (machine: Machine): AddMachineAction => ({
  type: ADD_MACHINE,
  payload: machine,
});

export const updateMachine = (machine: Machine): UpdateMachineAction => ({
  type: UPDATE_MACHINE,
  payload: machine,
});

export const deleteMachine = (id: number): DeleteMachineAction => ({
  type: DELETE_MACHINE,
  payload: id,
});

/******************************* THUNKS *******************************************/

import { csrfFetch } from './csrf';
import { setLoading } from './session';

// Get all machines
export const getMachines = () => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/machines');
    const data = await res.json();
    dispatch(loadMachines(data.machines));
  } catch (err) {
    console.error('Failed to fetch machines:', err);
  } finally {
    dispatch(setLoading(false));
  }
};

// Add machine
export const createMachine = (machineData: Partial<Machine>) => async (dispatch: any) => {
  const res = await csrfFetch('/api/machines', {
    method: 'POST',
    body: JSON.stringify(machineData),
  });

  if (res.ok) {
    const newMachine = await res.json();
    dispatch(addMachine(newMachine));
  }
};

// Update machine
export const editMachine = (id: number, updates: Partial<Machine>) => async (dispatch: any) => {
  const res = await csrfFetch(`/api/machines/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(updates),
  });

  if (res.ok) {
    const updated = await res.json();
    dispatch(updateMachine(updated));
  }
};

// Delete machine (from DB and Cloudinary)
export const removeMachine = (id: number) => async (dispatch: any) => {
  const res = await csrfFetch(`/api/machines/${id}`, {
    method: 'DELETE',
  });

  if (res.ok) {
    dispatch(deleteMachine(id));
  }
};

/******************************* REDUCER *******************************************/

const initialState: MachinesState = {
  all: {},
};

export default function machinesReducer(
  state = initialState,
  action: MachinesActionTypes
): MachinesState {
  switch (action.type) {
    case LOAD_MACHINES: {
      const newAll: Record<number, Machine> = {};
      action.payload.forEach((m) => (newAll[m.id] = m));
      return { ...state, all: newAll };
    }
    case ADD_MACHINE:
    case UPDATE_MACHINE:
      return { ...state, all: { ...state.all, [action.payload.id]: action.payload } };
    case DELETE_MACHINE: {
      const newAll = { ...state.all };
      delete newAll[action.payload];
      return { ...state, all: newAll };
    }
    default:
      return state;
  }
}