import { useState , useEffect} from "react";
import api from "../api";
import {useNavigate} from "react-router-dom";
import styles from "../styles/userinfo.module.css"

function Userinfo(){
    const [username,setusername]=useState("");
    const [userid,setuserid]=useState();
    const[msg,setMsg]=useState("");
    const navigate=useNavigate();

    useEffect(()=>{
        const infopage = async ()=>{
        try{
            const res = await api.get("/user")
            setusername(res.data.name)
            setuserid(res.data.user_id)
        }
        catch(err){
            if(err?.response?.status===401){
                setMsg("oops!!!")
                }
            }    
        }
        infopage();
    },[]);
    
    
    const deleteuser = async()=>{
            try{
                await api.delete("/user")
                navigate("/");
            }
            catch(err){
                if(err?.response?.status===401){
                    setMsg("no such user")
                }
            }
        }
    return <div className={styles.info}>
        <p>userid: {userid}</p> 
        <p>username: {username}</p>
        <button onClick={deleteuser}>delete my account??</button>
        <p className={styles.msg}>{msg}</p>
    </div>
}

export default Userinfo;