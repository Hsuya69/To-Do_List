import { useNavigate } from "react-router-dom";
import styles from "../styles/home.module.css"


function Home(){

    const navigate=useNavigate()
    return <div className={styles.hp}>
        <h1>To Do List</h1>
        <button onClick={()=>navigate("/signup")}>go to Signup</button>
        <button onClick={()=>navigate("/login")}>go to Login</button>
    </div>
}
export default Home