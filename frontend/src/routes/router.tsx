import { createBrowserRouter } from 'react-router-dom';
import { ProtectedRoute } from "@/routes/protected-route.tsx";
import { Homepage } from "@/pages/homepage.tsx";
import {LandingPage} from "@/pages/landingpage.tsx";
import {Postingpage} from "@/pages/postingpage.tsx";
import {Followrequestpage} from "@/pages/followrequestpage.tsx";
import {Profilepage} from "@/pages/profilepage.tsx";
import {Adminpage} from "@/pages/adminpage.tsx";
import {AdminProtectedRoute} from "@/routes/admin-protected-route.tsx";

export const router = createBrowserRouter([
    {
        path: "/",
        element:<LandingPage />
    },
    {
        path:"/home",
        element:
            <ProtectedRoute>
                <Homepage />
            </ProtectedRoute>
    },
    {
        path:"/post",
        element:
            <ProtectedRoute>
                <Postingpage />
            </ProtectedRoute>
    },
    {
        path:"/requests",
        element:
            <ProtectedRoute>
                <Followrequestpage />
            </ProtectedRoute>
    },
    {
        path:"/authors/:author_serial",
        element:
            <ProtectedRoute>
                <Profilepage />
            </ProtectedRoute>
    },
    {
        path:"/admin",
        element:
            <ProtectedRoute>
                <AdminProtectedRoute>
                    <Adminpage />
                </AdminProtectedRoute>
            </ProtectedRoute>
    },
    ]
);