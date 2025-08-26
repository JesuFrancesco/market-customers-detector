import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import { ThemeProvider } from "@/components/theme-provider";
import Header from "./components/header";
import Footer from "./components/footer";
import "./App.css";

function App() {
  return (
    <ThemeProvider>
      <div className="grid h-screen w-full grid-rows-[auto_1fr_auto]">
        <Header />
        <main className="mx-auto max-w-3xl overflow-scroll">
          <RouterProvider router={router} />
        </main>
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App;
