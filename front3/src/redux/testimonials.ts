/******************************* TYPES *******************************************/

interface Testimonial {
  id: number;
  author_name: string;
  stars: string;
  notables?: string;
  content: string;
  created_at: string;
  updated_at: string;
}

interface TestimonialsState {
  all: Record<number, Testimonial>;
}

interface LoadTestimonialsAction {
  type: typeof LOAD_TESTIMONIALS;
  payload: Testimonial[];
}

interface AddTestimonialAction {
  type: typeof ADD_TESTIMONIAL;
  payload: Testimonial;
}

interface UpdateTestimonialAction {
  type: typeof UPDATE_TESTIMONIAL;
  payload: Testimonial;
}

interface DeleteTestimonialAction {
  type: typeof DELETE_TESTIMONIAL;
  payload: number;
}

type TestimonialsActionTypes =
  | LoadTestimonialsAction
  | AddTestimonialAction
  | UpdateTestimonialAction
  | DeleteTestimonialAction;

/******************************* ACTION TYPES *******************************************/

const LOAD_TESTIMONIALS = 'testimonials/load';
const ADD_TESTIMONIAL = 'testimonials/add';
const UPDATE_TESTIMONIAL = 'testimonials/update';
const DELETE_TESTIMONIAL = 'testimonials/delete';

/******************************* ACTION CREATORS *******************************************/

export const loadTestimonials = (
  testimonials: Testimonial[]
): LoadTestimonialsAction => ({
  type: LOAD_TESTIMONIALS,
  payload: testimonials,
});

export const addTestimonial = (
  testimonial: Testimonial
): AddTestimonialAction => ({
  type: ADD_TESTIMONIAL,
  payload: testimonial,
});

export const updateTestimonial = (
  testimonial: Testimonial
): UpdateTestimonialAction => ({
  type: UPDATE_TESTIMONIAL,
  payload: testimonial,
});

export const deleteTestimonial = (id: number): DeleteTestimonialAction => ({
  type: DELETE_TESTIMONIAL,
  payload: id,
});

/******************************* THUNKS *******************************************/

import { csrfFetch } from "./csrf";
import { setLoading } from "./session";

export const getTestimonials = () => async (dispatch: any) => {
  try {
    const res = await csrfFetch("/api/testimonials");
    const data = await res.json();

    console.log("Fetched testimonials:", data);

    dispatch(loadTestimonials(data));
  } catch (err) {
    console.error("Failed to fetch testimonials:", err);
  } finally {
    dispatch(setLoading(false));
  }
};

export const createTestimonial = (
  testimonialData: Partial<Testimonial>
) => async (dispatch: any) => {
  const res = await csrfFetch("/api/testimonials", {
    method: "POST",
    body: JSON.stringify(testimonialData),
  });

  if (res.ok) {
    const newTestimonial = await res.json();
    dispatch(addTestimonial(newTestimonial));
  }
};

export const editTestimonial = (
  id: number,
  updates: Partial<Testimonial>
) => async (dispatch: any) => {
  const res = await csrfFetch(`/api/testimonials/${id}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });

  if (res.ok) {
    const updated = await res.json();
    dispatch(updateTestimonial(updated));
  }
};

export const removeTestimonial = (id: number) => async (dispatch: any) => {
  const res = await csrfFetch(`/api/testimonials/${id}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(deleteTestimonial(id));
  }
};

/******************************* REDUCER *******************************************/

const initialState: TestimonialsState = {
  all: {},
};

export default function testimonialsReducer(
  state = initialState,
  action: TestimonialsActionTypes
): TestimonialsState {
  switch (action.type) {
    case LOAD_TESTIMONIALS: {
      const newAll: Record<number, Testimonial> = {};
      action.payload.forEach((t) => (newAll[t.id] = t));
      return { ...state, all: newAll };
    }
    case ADD_TESTIMONIAL:
    case UPDATE_TESTIMONIAL:
      return {
        ...state,
        all: { ...state.all, [action.payload.id]: action.payload },
      };
    case DELETE_TESTIMONIAL: {
      const newAll = { ...state.all };
      delete newAll[action.payload];
      return { ...state, all: newAll };
    }
    default:
      return state;
  }
}