import { AuthForm } from "@/components/login-form"
import { Header } from "@/components/header"


export function LandingPage() {
    return (
      <div className="min-h-screen flex flex-col">
          <Header />
          <div className="flex items-center justify-center p-6">
              <AuthForm />
          </div>
      </div>
  )
}