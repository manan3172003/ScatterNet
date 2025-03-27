import {useContext, useState} from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import {AuthContext} from "@/context/AuthContext.tsx";

export function AuthForm() {
  // Login state
  const authContext = useContext(AuthContext);
  const [loginUsername, setLoginUsername] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  // Signup state
  const [signupUsername, setSignupUsername] = useState("")
  const [signupDisplayName, setSignupDisplayName] = useState("")
  const [signupPassword, setSignupPassword] = useState("")

  // Login handler
  const handleLogin = () => {
    let response = authContext?.login(loginUsername, loginPassword);
    response?.then((loginresponse) => {
      if (loginresponse.success) {
        // TODO: Route to home page or show notification error
        console.log("Logged In!");
      } else {
        console.log("Failed!");
      }
    })
  }

  // Signup handler
  const handleSignup = () => {

  }

  return (
    <Tabs defaultValue="login" className="w-[400px]">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login">Login</TabsTrigger>
        <TabsTrigger value="signup">Signup</TabsTrigger>
      </TabsList>
      <TabsContent value="login">
        <Card>
          <CardHeader>
            <CardTitle>Login</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="space-y-1">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                placeholder="Username"
                value={loginUsername}
                onChange={(e) => setLoginUsername(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={handleLogin}>Login</Button>
          </CardFooter>
        </Card>
      </TabsContent>
      <TabsContent value="signup">
        <Card>
          <CardHeader>
            <CardTitle>Signup</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="space-y-1">
              <Label htmlFor="new-username">Username</Label>
              <Input
                id="new-username"
                placeholder="Username"
                value={signupUsername}
                onChange={(e) => setSignupUsername(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="new-displayname">Display Name</Label>
              <Input
                id="new-displayname"
                placeholder="Display Name"
                value={signupDisplayName}
                onChange={(e) => setSignupDisplayName(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="new-password">Password</Label>
              <Input
                id="new-password"
                type="password"
                placeholder="Password"
                value={signupPassword}
                onChange={(e) => setSignupPassword(e.target.value)}
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={handleSignup}>Signup</Button>
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  )
}