import { useState,useEffect } from "react"
import api from "../api.js"
import styles from "../styles/user.module.css"

function Todo(){
    const [msg,setMsg]=useState("");
    const [username,setusername]=useState("");
    const [task,settask]=useState([]);
    const [taskname,settaskname]=useState("");

    const handleTodo = async ()=>{
        try{
            const res= await api.get("/user")
            setusername(res.data.name)
            settask(res.data.tasks)
        }
        catch (err){
            if (err && err.response.status===401){
                setMsg("server error!!")
            }  
        }
    }
    
    useEffect(()=>{
    handleTodo();
    },[])
    
    const inserttodo = async (e)=>{
        e.preventDefault()
        try{
            const res=await api.post("/user/add_task",{
                "task_name":taskname
            })
            setMsg(res.data.msg|| "Task added successfully")
            settaskname("")
            handleTodo();
        }
        catch(err){
                if (err && err.response.status===401){
                    setMsg("server error!!")
                }
            }

        }
        const updatetask = async (taskid)=>{
            try{
                const res = await api.post("/user/update_task",{taskid})
                setMsg("task updated successfully")
                handleTodo();
            }
            catch(err){
                if(err?.response?.status===401){
                    setMsg("err occured")
                }
            }
           
        }
        const deletetask =async (taskid)=>{
            try{
                const res=await api.delete("/user/delete_task",{
                    data:{taskid}
                })
                setMsg("deleted!!");
                handleTodo();
            }
            catch(err){
                if(err?.status?.response===401){
                    setMsg("oops")
                }
            }
        }
       
    
    return (<div className={styles.user}>
        <h1>{username}</h1>
        <div className={styles.task}>
            <ul>
            {task.map((t,index)=>(
                <li key={index}>
                    {t.taskid} {t.task} {t.task_status}
                     <button onClick={(e)=>{updatetask(t.taskid)}}>update status</button>
                     <button onClick={(e)=>{deletetask(t.taskid)}}>delete task</button>
                </li>
            ))}
        </ul>
        </div>

        <p>{msg}</p> 
        <div className={styles.newtask}>
            <form onSubmit={inserttodo}>
            <input type="text"
            placeholder="add new task"
            value={taskname}
            onChange={(e)=> settaskname(e.target.value)} />
            <button type="submit">add task</button>
        </form>
        </div>
        
            <a href="/userinfo">settings</a>
    </div>);
}

export default Todo