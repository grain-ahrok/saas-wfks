import styles from './Auth.module.css';
import { useState } from "react";
import axios from "axios";

function SignUp() {

    const [cName, setCName] = useState("");
    const [email, setEmail] = useState("");
    const [pw, setPW] = useState("");
    const [doAddr, setDoAddr] = useState("");
    const [ipAddr, setIpAddr] = useState("");

    const signUpAxios = async (e) => {
        e.preventDefault();

        await axios.post("/users/signup", {
            companyName : cName,
            email : email,
            password : pw,
            domain_address : doAddr,
            IP_address : ipAddr,
            membership : 'Basic'
          })
          .then((response) => {
            if ((response.status = 200)) {
                alert("회원가입 되셨습니다. 로그인 해 주세요");
              return navigate("/signin");
            }
          })
          .catch((err) => {
            alert("에러가 발생했습니다. 관리자에게 문의해주세요" + err);
          });
      };


    return (
        <div className={styles.Screen}>
            <div className={styles.LogoWindow}>
                <h1>Pi5neer</h1>
                <p>더 빠르고 안정적이며 안전한 서비스로 고객의 비즈니스 가치를 극대화시킵니다</p>
            </div>
            <div className={styles.InputWindow}>
                <div className={styles.ShadowBox}>
                    <div className={styles.InputPadding}>
                        <h2>Sign up for a free account</h2>
                        <input className={styles.InputField} onChange={(e) => setCName(e.target.value)} placeholder="Input Company Name"></input>
                        <input className={styles.InputField} onChange={(e) => setEmail(e.target.value)} id="email" placeholder="Email address"></input>
                        <input className={styles.InputField} onChange={(e) => setPW(e.target.value)}  id="pw" placeholder="Input Password" type="password"></input>
                        <input className={styles.InputField} onChange={(e) => setDoAddr(e.target.value)} id="doAddr" placeholder="Domain address"></input>
                        <input className={styles.InputField} onChange={(e) => setIpAddr(e.target.value)} id="ipAddr"placeholder="IP address"></input>
                        <button className={styles.LoginBtn} onClick={signUpAxios} type="button">Register</button>
                        <div className={styles.NavigateBtn} >
                            <a href="./">sign in</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
  export default SignUp;
  