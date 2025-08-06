// front3/src/main.tsx

import React from "react";
import ReactDOM from "react-dom/client";
import { Provider as ReduxProvider } from "react-redux";
import { RouterProvider } from "react-router-dom";
import configureStore from "./redux/store";
import { router } from "./router";
import { ModalProvider } from "./context/Modal";
import * as sessionActions from "./redux/session";
import * as faqActions from "./redux/faqs";
import * as machineActions from "./redux/machines";
import * as imageActions from "./redux/images";
import * as testimonialActions from "./redux/testimonials";
import type { Store } from "redux";
import type { RootState } from "./redux/store";

// Extend window type for dev tools
declare global {
  interface Window {
    store: Store<RootState>;
    sessionActions: typeof sessionActions;
    faqActions: typeof faqActions;
    machineActions: typeof machineActions;
    imageActions: typeof imageActions;
    testimonialActions: typeof testimonialActions;
  }
}

const store = configureStore();

if (import.meta.env.MODE !== "production") {
  window.store = store;
  window.sessionActions = sessionActions;
  window.faqActions = faqActions;
  window.machineActions = machineActions;
  window.imageActions = imageActions;
  window.testimonialActions = testimonialActions;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ReduxProvider store={store}>
      <ModalProvider>
        <RouterProvider router={router} />
      </ModalProvider>
    </ReduxProvider>
  </React.StrictMode>
);