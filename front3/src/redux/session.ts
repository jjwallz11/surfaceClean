// redux/session.ts

import { csrfFetch } from "./csrf";

/******************************* TYPES *******************************************/

interface User {
  id: number;
  email: string;
  // Add any other fields needed
}

interface SessionState {
  user: User | null;
  loading: boolean;
}

/******************************* ACTION TYPES *******************************************/

const SET_USER = 'session/setUser';
const REMOVE_USER = 'session/removeUser';
const SET_LOADING = 'session/setLoading';

interface SetUserAction {
  type: typeof SET_USER;
  payload: User;
}

interface RemoveUserAction {
  type: typeof REMOVE_USER;
}

interface SetLoadingAction {
  type: typeof SET_LOADING;
  payload: boolean;
}

type SessionActionTypes = SetUserAction | RemoveUserAction | SetLoadingAction;

/******************************* ACTION CREATORS *******************************************/

export const setUser = (user: User): SetUserAction => ({
  type: SET_USER,
  payload: user,
});

export const removeUser = (): RemoveUserAction => ({
  type: REMOVE_USER,
});

export const setLoading = (loading: boolean): SetLoadingAction => ({
  type: SET_LOADING,
  payload: loading,
});

/******************************* THUNK ACTIONS *******************************************/

// Get current user from session
export const getCurrentUser = () => async (dispatch: any) => {
  try {
    dispatch(setLoading(true));
    const res = await csrfFetch("/api/session/current");
    if (!res.ok) throw Error("Failed to get current user");
    const user = await res.json();
    dispatch(setUser(user));
  } catch (e) {
    console.error("Error loading user:", e);
  } finally {
    dispatch(setLoading(false));
  }
};

// Login
export const thunkLogin = (credentials: { email: string; password: string }) => async (dispatch: any) => {
  dispatch(setLoading(true));
  const response = await fetch('/api/session/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    dispatch(setLoading(false));
    return errorMessages;
  } else {
    dispatch(setLoading(false));
    return { server: 'Something went wrong. Please try again' };
  }

  dispatch(setLoading(false));
};

// Logout
export const thunkLogout = () => async (dispatch: any) => {
  dispatch(setLoading(true));

  await fetch("/api/session/logout", {
    method: "POST",
    credentials: "include", // include cookies in request
  });

  // Frontend can only remove non-httpOnly cookies like csrf_token
  document.cookie = "csrf_token=; Max-Age=0; path=/";

  dispatch(removeUser());
  dispatch(setLoading(false));
};

/******************************* REDUCER *******************************************/

const initialState: SessionState = {
  user: null,
  loading: false,
};

export default function sessionReducer(state = initialState, action: SessionActionTypes): SessionState {
  switch (action.type) {
    case SET_USER:
      return { ...state, user: action.payload };
    case REMOVE_USER:
      return { ...state, user: null };
    case SET_LOADING:
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}