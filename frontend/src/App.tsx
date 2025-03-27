import { ThemeProvider } from "@/components/theme-provider"
import { RouterProvider } from "react-router-dom";
import {router} from "@/components/router.tsx";

function App() {
  return (
      <ThemeProvider>
        <RouterProvider router={router} />
      </ThemeProvider>
  )
}

export default App
