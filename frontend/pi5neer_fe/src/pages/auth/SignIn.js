import styles from './Auth.module.css';
import { useState } from "react";
import { useNavigate } from "react-router-dom"
import axios from "axios";

function SignIn() {

    const navigate = useNavigate();

    const [cName, setCName] = useState("");
    const [pw, setPW] = useState("");

    const signInAxios = async (e) => {
        e.preventDefault();
        
        const cn_reg = /^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$/;
        const pw_reg = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,15}$/;
        if( !cn_reg.test(cName) ) {
            alert("회사 이름을 확인해주세요.");
            return;
        }
        if( !pw_reg.test(pw) ) {
            alert("비밀번호를 확인해주세요.");
            return;
        }

        await axios.post("/users/signin", {
            companyName : cName,
            password : pw,
          })
          .then((response) => {
            if (response.status = 200) {
              return navigate("/customers/dashboard");
            } else if (response.status = 401) {
                alert("다시 확인해주세요");
            }
          })
          .catch((err) => {
            alert("에러가 발생했습니다. 관리자에게 문의해주세요\n" + err);
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
                        <h2>Sign in</h2>
                        <form onSubmit={signInAxios}> 
                            <input className={styles.InputField} onChange={(e) => setCName(e.target.value)} placeholder="Input Company Name"></input>
                            <input className={styles.InputField} onChange={(e) => setPW(e.target.value)} placeholder="Input Password" type="password"></input>
                            <button className={styles.LoginBtn} type="submit">Login</button>
                        </form>
                        <div className={styles.NavigateBtn}>
                            <a href="./signup">sign up</a>
                            <div>&nbsp;/&nbsp;</div>
                            <a href="#">forgot my password</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
  export default SignIn;
  