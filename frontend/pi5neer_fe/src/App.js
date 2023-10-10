import { BrowserRouter, Route, Routes} from "react-router-dom";
import SignIn from './pages/auth/SignIn.js'
import SignUp from './pages/auth/SignUp.js'
import './App.css'

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<SignIn />}/>
          <Route path="/signup" element={<SignUp />}/>
        </Routes>
        
      </BrowserRouter>
  )
}

export default App;
