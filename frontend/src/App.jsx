
import {BrowserRouter,Routes,Route} from 'react-router-dom'
import Home from './pages/home'
import Signup from './pages/signup'
import Loginuser from './pages/login'
import Todo from './pages/user'
import Protectroute from './components/protected.jsx'
import Userinfo from './pages/userinfo'
function App() {
  return (
    <>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home/>}/>
      <Route path="/signup" element={<Signup/>}/>
      <Route path="/login" element={<Loginuser/>}/>
      <Route path="/user" element={<Protectroute><Todo/></Protectroute>}/>
      <Route path="/userinfo" element={<Protectroute><Userinfo/></Protectroute>}/>

    </Routes>
    </BrowserRouter>
    
    
    </>
  )
}

export default App
