import { ThemeProvider } from "@/components/theme-provider"
import { Page } from "@/pages/loginpage.tsx"

function App() {
  return (
      <ThemeProvider>
        <Page/>
      </ThemeProvider>
  )
}

export default App
