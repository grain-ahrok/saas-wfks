import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { routes } from "./routes";
import SignIn from "./pages/auth/SignIn";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" >
          {routes}
        </Route>
        <Route path="*" element={<SignIn />}></Route>,
      </Routes>
    </BrowserRouter>
  );
}

export default App;
