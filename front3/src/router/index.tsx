// src/router/index.tsx
import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import MachinesPage from "../pages/Machines/MachinesPage";
import MachineDetailsPage from "../pages/MachineDetailsPage";
import HomePage from "../pages/Home/HomePage";
import FaqsPage from "../pages/Faqs/FaqsPage";
import TestimonialsPage from "../pages/Testimonials/TestimonialsPage";
import AboutPage from "../pages/About/AboutPage";
import ContactPage from "../pages/Contact/ContactPage";
import AdminHomePage from "../pages/AdminHomePage/AdminHomePage";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />, // public landing page
      },
      {
        path: "/admin",
        element: <AdminHomePage />, // Dave-only admin access
      },
      {
        path: "/faqs",
        element: <FaqsPage />,
      },
      {
        path: "/machines",
        element: <MachinesPage />,
      },
      {
        path: "/machines/:machineId",
        element: <MachineDetailsPage />,
      },
      {
        path: "/testimonials",
        element: <TestimonialsPage />,
      },
      {
        path: "/about",
        element: <AboutPage />,
      },
      {
        path: "/contact",
        element: <ContactPage />,
      },
    ],
  },
]);
