import { useState } from "react"
import api from "../api"
import {useNavigate} from 'react-router-dom'
import styles from "../styles/signup.module.css";


function Signup(){
    const [username,setUsername]=useState("");
    const [password,setPassword]=useState("");
    const [message,setMessage]=useState("");
    const navigate=useNavigate();

    const handle_signup = async (e) => {
        e.preventDefault();

        try{
            const res = await api.post('/signup',{
                username,
                password,
            });
            setMessage(res.data.message);
            navigate("/");   
        } catch(err){
            setMessage("signup failed");
        }
    };



    return <div>
            <div className={styles.signup}>
                <form onSubmit={handle_signup} method="POST">
            <input type="text" 
            placeholder="username" 
            value={username}
            onChange={(e)=>setUsername(e.target.value)} />
            <input type="password" 
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)} />
            <button  type="submit">Signup</button>
            <p>{message}</p>
        </form>
        </div>    
    </div>
}
export default Signup