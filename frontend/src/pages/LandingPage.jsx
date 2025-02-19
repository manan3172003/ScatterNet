
import HeaderLogo from "../components/HeaderLogo"
import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import "../assets/styles/landing-page.css"
export default function LandingPage(){


    return <div className="landing-container">
            <header className="landing-header">
                <HeaderLogo/>
            </header>
            <main className="landing-main">
                <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="signup">Sign Up</TabsTrigger>
            </TabsList>
            <TabsContent value="login" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" placeholder="Enter your email" type="email" className="bg-gray-800 border-gray-700" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input id="password" type="password" className="bg-gray-800 border-gray-700" />
              </div>
              <Button className="w-full bg-primary hover:bg-primary/90">Log In</Button>
              <div className="text-center">
                <Link href="#" className="text-sm text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>
            </TabsContent>
            <TabsContent value="signup" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signup-email">Email</Label>
                <Input
                  id="signup-email"
                  placeholder="Enter your email"
                  type="email"
                  className="bg-gray-800 border-gray-700"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="signup-password">Password</Label>
                <Input id="signup-password" type="password" className="bg-gray-800 border-gray-700" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirm-password">Confirm Password</Label>
                <Input id="confirm-password" type="password" className="bg-gray-800 border-gray-700" />
              </div>
              <Button className="w-full bg-primary hover:bg-primary/90">Sign Up</Button>
            </TabsContent>
          </Tabs>

            </main>


    </div>

}