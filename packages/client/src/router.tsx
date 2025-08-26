import { createHashRouter } from "react-router-dom";
import HomePage from "./pages/home/page";
import MarketsPage from "./pages/markets/page";
import VipsPage from "./pages/vip/page";
import CustomersPage from "./pages/customers/page";

export const router = createHashRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/markets",
    element: <MarketsPage />,
  },
  {
    path: "/vips",
    element: <VipsPage />,
  },
  {
    path: "/customers",
    element: <CustomersPage />,
  },
]);
