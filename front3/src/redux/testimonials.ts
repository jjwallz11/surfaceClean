// redux/testimonials.ts

import { csrfFetch } from './csrf';
import { setLoading } from './session';

/******************************* TYPES *******************************************/

export interface Testimonial {
  id: number;
  author_name: string;
  stars: number;
  notables?: string;
  content: string;
  created_at: string;
  updated_at: string;
}

interface TestimonialsState {
  testimonials: Record<number, Testimonial>;
}

/******************************* ACTION TYPES *******************************************/

const LOAD_ALL = 'testimonials/loadAll';
const ADD_ONE = 'testimonials/addOne';
const UPDATE_ONE = 'testimonials/updateOne';
const DELETE_ONE = 'testimonials/deleteOne';

interface LoadAllAction {
  type: typeof LOAD_ALL;
  payload: Testimonial[];
}

interface AddOneAction {
  type: typeof ADD_ONE;
  payload: Testimonial;
}

interface UpdateOneAction {
  type: typeof UPDATE_ONE;
  payload: Testimonial;
}

interface DeleteOneAction {
  type: typeof DELETE_ONE;
  payload: number;
}

type TestimonialActions =
  | LoadAllAction
  | AddOneAction
  | UpdateOneAction
  | DeleteOneAction;

/******************************* ACTION CREATORS *******************************************/

export const loadAll = (testimonials: Testimonial[]): LoadAllAction => ({
  type: LOAD_ALL,
  payload: testimonials,
});

export const addOne = (testimonial: Testimonial): AddOneAction => ({
  type: ADD_ONE,
  payload: testimonial,
});

export const updateOne = (testimonial: Testimonial): UpdateOneAction => ({
  type: UPDATE_ONE,
  payload: testimonial,
});

export const deleteOne = (id: number): DeleteOneAction => ({
  type: DELETE_ONE,
  payload: id,
});

/******************************* THUNK ACTIONS *******************************************/

// Get all testimonials
export const getAllTestimonials = () => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/testimonials/');
    if (!res.ok) throw Error('Failed to get testimonials');
    const data = await res.json();
    dispatch(loadAll(data.testimonials));
  } catch (e) {
    console.error('Error loading testimonials:', e);
  } finally {
    dispatch(setLoading(false));
  }
};

// Add a new testimonial
export const createTestimonial = (payload: Partial<Testimonial>) => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/testimonials/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw Error('Failed to create testimonial');
    const testimonial = await res.json();
    dispatch(addOne(testimonial));
  } catch (e) {
    console.error('Error creating testimonial:', e);
  }
};

// Update testimonial
export const editTestimonial = (id: number, payload: Partial<Testimonial>) => async (dispatch: any) => {
  try {
    const res = await csrfFetch(`/api/testimonials/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw Error('Failed to update testimonial');
    const testimonial = await res.json();
    dispatch(updateOne(testimonial));
  } catch (e) {
    console.error('Error updating testimonial:', e);
  }
};

// Delete testimonial
export const deleteTestimonial = (id: number) => async (dispatch: any) => {
  try {
    const res = await csrfFetch(`/api/testimonials/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw Error('Failed to delete testimonial');
    await res.json();
    dispatch(deleteOne(id));
  } catch (e) {
    console.error('Error deleting testimonial:', e);
  }
};

/******************************* INITIAL STATE AND REDUCER *******************************************/

const initialState: TestimonialsState = {
  testimonials: {},
};

export default function testimonialsReducer(
  state = initialState,
  action: TestimonialActions
): TestimonialsState {
  switch (action.type) {
    case LOAD_ALL: {
      const all: Record<number, Testimonial> = {};
      action.payload.forEach(t => (all[t.id] = t));
      return { ...state, testimonials: all };
    }
    case ADD_ONE:
    case UPDATE_ONE:
      return {
        ...state,
        testimonials: {
          ...state.testimonials,
          [action.payload.id]: action.payload,
        },
      };
    case DELETE_ONE: {
      const updated = { ...state.testimonials };
      delete updated[action.payload];
      return { ...state, testimonials: updated };
    }
    default:
      return state;
  }
}