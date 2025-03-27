import { createBrowserRouter } from 'react-router-dom';
import { ProtectedRoute } from "@/components/protected-route.tsx";
import { Homepage } from "@/pages/homepage.tsx";
import {LandingPage} from "@/pages/landingpage.tsx";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <LandingPage />
    },
    {
        path:"/home",
        element:
            <ProtectedRoute>
                <Homepage />
            </ProtectedRoute>
    }]
);