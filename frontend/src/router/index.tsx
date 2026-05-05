import { Navigate, Outlet, createBrowserRouter } from "react-router-dom";
import AppLayout from "../layouts/AppLayout";
import { useAuth } from "../hooks/useAuth";
import ActivitiesPage from "../pages/ActivitiesPage";
import AssignmentsPage from "../pages/AssignmentsPage";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";
import NotFoundPage from "../pages/NotFoundPage";
import RegisterPage from "../pages/RegisterPage";
import UsersPage from "../pages/UsersPage";

function RequireAuth() {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <Outlet />;
}

function PublicOnly() {
  const { token } = useAuth();
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }
  return <Outlet />;
}

export const router = createBrowserRouter([
  {
    element: <PublicOnly />,
    children: [
      { path: "/login", element: <LoginPage /> },
      { path: "/register", element: <RegisterPage /> }
    ]
  },
  {
    element: <RequireAuth />,
    children: [
      {
        path: "/",
        element: <AppLayout />,
        children: [
          { index: true, element: <Navigate to="/dashboard" replace /> },
          { path: "/dashboard", element: <DashboardPage /> },
          { path: "/users", element: <UsersPage /> },
          { path: "/activities", element: <ActivitiesPage /> },
          { path: "/assignments", element: <AssignmentsPage /> }
        ]
      }
    ]
  },
  { path: "*", element: <NotFoundPage /> }
]);

