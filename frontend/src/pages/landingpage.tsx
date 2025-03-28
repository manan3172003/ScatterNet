import { AuthForm } from "@/components/login-form"
import { Header } from "@/components/header"
import {useContext} from "react";
import {AuthContext} from "@/context/AuthContext.tsx";
import {useNavigate} from "react-router-dom";


export function LandingPage() {
      const { user } = useContext(AuthContext);
      const navigate = useNavigate();

      if (user !== null) {
          navigate('/home');
      }

    return (
      <div className="min-h-screen flex flex-col">
          <Header />
          <div className="flex items-center justify-center p-6">
              <AuthForm />
          </div>
      </div>
  )
}