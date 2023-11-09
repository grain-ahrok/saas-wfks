import { BrowserRouter, Route, Routes } from "react-router-dom";
import { routes } from "./routes";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/">
          {routes}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
