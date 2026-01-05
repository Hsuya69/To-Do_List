import { useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api";
import styles from "../styles/login.module.css"
function Loginuser(){
    const [username,setUsername] = useState("");
    const [password,setPassword] = useState("");
    const [message,setMessage] = useState("");
    const navigate=useNavigate();

    const handleLogin = async (e) =>{
        e.preventDefault();
        
        try{
            const res=await api.post("/login",{
                username,
                password,
            });
            setMessage("logged in successfully");
            navigate("/user");
        }
        catch(err){
            if(err && err.response.status==401){
                setMessage("incorrect password or username")
            }
            else{
                setMessage("server error, try again later!!")
            }
        }
    }
    return <div className={styles.login}>
        <form onSubmit={handleLogin} method="POST">
        <input type="text"
         placeholder="username"
          value={username}
           onChange={(e)=>setUsername(e.target.value)} />
        <input type="password"
         placeholder="password"
          value={password}
           onChange={(e)=>setPassword(e.target.value)}/>
           <button type="submit">Login</button>
           <p>{message}</p>
        </form>
    </div>
}

export default Loginuser