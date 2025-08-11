/******************************* TYPES *******************************************/

export interface Image {
  id: number;
  url: string;
  description: string;
  machine_id: number;
  created_at?: string;
  updated_at?: string;
}

export interface ImagesState {
  images: Record<number, Image>;
}

/******************************* ACTION TYPES *******************************************/

const LOAD_IMAGES = 'images/loadImages';
const ADD_IMAGE = 'images/addImage';
const UPDATE_IMAGE = 'images/updateImage';
const DELETE_IMAGE = 'images/deleteImage';

interface LoadImagesAction {
  type: typeof LOAD_IMAGES;
  payload: Image[];
}

interface AddImageAction {
  type: typeof ADD_IMAGE;
  payload: Image;
}

interface UpdateImageAction {
  type: typeof UPDATE_IMAGE;
  payload: Image;
}

interface DeleteImageAction {
  type: typeof DELETE_IMAGE;
  payload: number;
}

export type ImageActionTypes =
  | LoadImagesAction
  | AddImageAction
  | UpdateImageAction
  | DeleteImageAction;

/******************************* ACTION CREATORS *******************************************/

export const loadImages = (images: Image[]): LoadImagesAction => ({
  type: LOAD_IMAGES,
  payload: images,
});

export const addImage = (image: Image): AddImageAction => ({
  type: ADD_IMAGE,
  payload: image,
});

export const updateImage = (image: Image): UpdateImageAction => ({
  type: UPDATE_IMAGE,
  payload: image,
});

export const deleteImage = (imageId: number): DeleteImageAction => ({
  type: DELETE_IMAGE,
  payload: imageId,
});

/******************************* THUNK ACTIONS *******************************************/

import { csrfFetch } from './csrf';
import { setLoading } from './session';

export const getAllImages = () => async (dispatch: any) => {
  try {
    const res = await csrfFetch('/api/images/');
    const data = await res.json();
    dispatch(loadImages(data.images));
  } catch (e) {
    console.error('Error loading images:', e);
  } finally {
    dispatch(setLoading(false));
  }
};

export const createImage = (form: FormData) => async (dispatch: any) => {
  const res = await csrfFetch("/api/images/", {
    method: "POST",
    body: form,           // must be FormData with: file, description, machine_id
    credentials: "include"
  });
  if (!res.ok) throw new Error("Image upload failed");
  const data = await res.json();
  dispatch(addImage(data));
  return data;
};


export const editImage = (imageId: number, payload: Partial<Image>) => async (dispatch: any) => {
  try {
    const res = await csrfFetch(`/api/images/${imageId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    dispatch(updateImage(data));
  } catch (e) {
    console.error('Error updating image:', e);
  }
};

export const removeImage = (imageId: number) => async (dispatch: any) => {
  try {
    await csrfFetch(`/api/images/${imageId}`, {
      method: 'DELETE',
    });
    dispatch(deleteImage(imageId));
  } catch (e) {
    console.error('Error deleting image:', e);
  }
};

/******************************* INITIAL STATE AND REDUCER *******************************************/

const initialState: ImagesState = {
  images: {},
};

export default function imagesReducer(
  state = initialState,
  action: ImageActionTypes
): ImagesState {
  switch (action.type) {
    case LOAD_IMAGES: {
      const newImages: Record<number, Image> = {};
      action.payload.forEach((img) => (newImages[img.id] = img));
      return { ...state, images: newImages };
    }
    case ADD_IMAGE:
    case UPDATE_IMAGE:
      return {
        ...state,
        images: {
          ...state.images,
          [action.payload.id]: action.payload,
        },
      };
    case DELETE_IMAGE: {
      const newState = { ...state.images };
      delete newState[action.payload];
      return { ...state, images: newState };
    }
    default:
      return state;
  }
}