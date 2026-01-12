import { useState,useEffect} from "react";
import { Navigate } from "react-router-dom";
import api from "../api";
import {DEV_MODE} from '../config/dev'


export default function Potectroute({children}){
    const [authcheck,setAuthcheck]=useState(false)
    const [isauth,setIsauth]=useState(false)

    useEffect(()=>{
        api.get("/user")
        .then( ()=>{
            setIsauth(true);
        })
        .catch((err)=>{
            if(err.response?.status===401){
                setIsauth(false);
            }
        })
        .finally(()=>{
            setAuthcheck(true);
        })
        
    },[]);

     if(DEV_MODE){
        return children;
     }

     if(!authcheck) return <div>checking authentication...</div>
     if(!isauth) return <Navigate to="/login" replace/>;
    
    return children;
}

 