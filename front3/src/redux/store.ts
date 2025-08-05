// src/redux/store.ts

declare global {
  interface ImportMetaEnv {
    readonly MODE: string;
    readonly VITE_API_BASE_URL: string;
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
}

import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
  Store,
} from "redux";
import thunk from "redux-thunk";

import sessionReducer from "./session";
import faqReducer from "./faqs";
import imageReducer from "./images";
import machineReducer from "./machines";
import testimonialReducer from "./testimonials";

const rootReducer = combineReducers({
  session: sessionReducer,
  faqs: faqReducer,
  images: imageReducer,
  machines: machineReducer,
  testimonials: testimonialReducer,
});

export type RootState = ReturnType<typeof rootReducer>;

let enhancer;
if (import.meta.env.MODE === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    (window && (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__) || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState?: Partial<RootState>): Store => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;