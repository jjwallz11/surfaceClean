// redux/faqs.ts

import { csrfFetch } from './csrf';
import { setLoading } from './session';

/******************************* TYPES *******************************************/

export interface FAQ {
  id: number;
  question: string;
  answer: string;
  scheduled_post_date: string;
  created_at: string;
  updated_at: string;
}

interface FAQState {
  faqs: Record<number, FAQ>;
}

/******************************* ACTION TYPES *******************************************/

const LOAD_FAQS = 'faqs/loadFaqs';
const ADD_FAQ = 'faqs/addFaq';
const UPDATE_FAQ = 'faqs/updateFaq';
const DELETE_FAQ = 'faqs/deleteFaq';

/******************************* ACTION CREATORS *******************************************/

const loadFaqs = (faqs: FAQ[]) => ({
  type: LOAD_FAQS,
  payload: faqs,
});

const addFaq = (faq: FAQ) => ({
  type: ADD_FAQ,
  payload: faq,
});

const updateFaq = (faq: FAQ) => ({
  type: UPDATE_FAQ,
  payload: faq,
});

const deleteFaq = (faqId: number) => ({
  type: DELETE_FAQ,
  payload: faqId,
});

/******************************* THUNK ACTIONS *******************************************/

// Get all FAQs (admin)
export const getAllFaqs = () => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/faqs');
    if (!res.ok) throw Error('Failed to fetch all FAQs');
    const data = await res.json();
    dispatch(loadFaqs(data.faqs));
  } catch (e) {
    console.error('Error loading all FAQs', e);
  } finally {
    dispatch(setLoading(false));
  }
};

// Get live/public FAQs (home page)
export const getLiveFaqs = () => async (dispatch: any) => {
  try {
    const res = await fetch('/api/faqs/live');
    if (!res.ok) throw Error('Failed to fetch live FAQs');
    const data = await res.json();
    dispatch(loadFaqs(data.faqs));
  } catch (e) {
    console.error('Error loading live FAQs', e);
  }
};

// Create FAQ
export const createFaq = (faqData: Partial<FAQ>) => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/faqs', {
      method: 'POST',
      body: JSON.stringify(faqData),
    });
    const data = await res.json();
    dispatch(addFaq(data));
    return data;
  } catch (e) {
    console.error('Error creating FAQ', e);
  }
};

// Update FAQ
export const editFaq = (id: number, updates: Partial<FAQ>) => async (dispatch: any) => {
  try {
    const res = await csrfFetch(`/api/faqs/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    });
    const data = await res.json();
    dispatch(updateFaq(data));
    return data;
  } catch (e) {
    console.error('Error updating FAQ', e);
  }
};

// Delete FAQ
export const removeFaq = (id: number) => async (dispatch: any) => {
  try {
    const res = await csrfFetch(`/api/faqs/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw Error('Failed to delete FAQ');
    dispatch(deleteFaq(id));
  } catch (e) {
    console.error('Error deleting FAQ', e);
  }
};

/******************************* REDUCER *******************************************/

const initialState: FAQState = {
  faqs: {},
};

export default function faqsReducer(state = initialState, action: any): FAQState {
  switch (action.type) {
    case LOAD_FAQS: {
      const newFaqs: Record<number, FAQ> = {};
      action.payload.forEach((faq: FAQ) => {
        newFaqs[faq.id] = faq;
      });
      return { ...state, faqs: newFaqs };
    }
    case ADD_FAQ:
    case UPDATE_FAQ:
      return {
        ...state,
        faqs: { ...state.faqs, [action.payload.id]: action.payload },
      };
    case DELETE_FAQ: {
      const newState = { ...state.faqs };
      delete newState[action.payload];
      return { ...state, faqs: newState };
    }
    default:
      return state;
  }
}