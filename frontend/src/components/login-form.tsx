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
import {apiCall} from "@/utils/ApiCall.tsx";
import {useNavigate} from "react-router-dom";

export function AuthForm() {
  const navigate = useNavigate();

  const authContext = useContext(AuthContext);
  const [loginUsername, setLoginUsername] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  const [signupUsername, setSignupUsername] = useState("")
  const [signupDisplayName, setSignupDisplayName] = useState("")
  const [signupPassword, setSignupPassword] = useState("")

  async function handleLogin () {
    let response = await authContext?.login(loginUsername, loginPassword);
    if (response?.success) {
      // TODO: Route to home page or show notification error
      console.log("Logged In!");
      setTimeout(() => {navigate('/home')})
    } else {
      console.log("Failed!");
    }
  }

  async function handleSignup () {
    let response = await apiCall(
        "authors/signup",
        "POST",
        {
          username: signupUsername,
          password: signupPassword,
          displayName: signupDisplayName,
          profileImage: `https://robohash.org/${signupDisplayName}.png`
        }
    );

    const data = await response.json()

    if (response.ok) {
      // TODO: Notification
      console.log("Account created! Wait for admin approval before logging in...");
      setSignupUsername("");
      setSignupPassword("");
      setSignupDisplayName("");
    } else if (response.status === 400 && data.username) {
      // TODO: Notification
      console.log("Author with this username already exists");
    } else {
      // TODO: Notification
      console.log("Sign up failed");
    }

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