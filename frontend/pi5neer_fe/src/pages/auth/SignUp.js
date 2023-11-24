import styles from './Auth.module.css';
import { useState } from "react"; 
import { useNavigate } from "react-router-dom"
import axios from "axios";

function SignUp() {

    const navigate = useNavigate();

    const [cName, setCName] = useState("");
    const [email, setEmail] = useState("");
    const [pw, setPW] = useState("");
    const [doAddr, setDoAddr] = useState("");
    const [ipAddr, setIpAddr] = useState("");

    const signUpAxios = async (e) => {
        e.preventDefault();

        const cn_reg = /^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$/;
        const email_reg = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        const pw_reg = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,15}$/;
        const do_reg = /^(((http(s?)):\/\/)?)([0-9a-zA-Z-]+\.)+[a-zA-Z]{2,6}(:[0-9]+)?(\/\S*)?/;
        const ip_reg = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/;

        if( !cn_reg.test(cName) ) {
            alert("회사 이름을 확인해주세요.");
            return false;
        }
        if( !email_reg.test(email) ) {
            alert("이메일 확인해주세요.");
            return false;
        }
        if( !pw_reg.test(pw) ) {
            alert("비밀번호는 영문 숫자 특수기호 조합 8자리 이상입니다.");
            return false;
        }
        if( !do_reg.test(doAddr) ) {
            alert("도메인 주소를 확인해주세요");
            return false;
        }
        if( !ip_reg.test(ipAddr) ) {
            alert("IP 주소를 확인해주세요");
            return false;
        }

        await axios.post("/users/signup", {
            companyName : cName,
            email : email,
            password : pw,
            domain_address : doAddr,
            IP_address : ipAddr,
            membership : 'basic'
          })
          .then((response) => {
            if ((response.status = 201)) {
                alert("회원가입 되셨습니다. 로그인 해 주세요");
              return navigate("/users/signin");
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
                        <h2>Sign up for a free account</h2>
                        <form onSubmit={signUpAxios}> 
                            <input className={styles.InputField} onChange={(e) => setCName(e.target.value)} placeholder="Input Company Name"></input>
                            <input className={styles.InputField} onChange={(e) => setEmail(e.target.value)} id="email" placeholder="Email address"></input>
                            <input className={styles.InputField} onChange={(e) => setPW(e.target.value)}  id="pw" placeholder="Input Password" type="password"></input>
                            <input className={styles.InputField} onChange={(e) => setDoAddr(e.target.value)} id="doAddr" placeholder="Domain address"></input>
                            <input className={styles.InputField} onChange={(e) => setIpAddr(e.target.value)} id="ipAddr"placeholder="IP address"></input>
                            <button className={styles.LoginBtn} type="submit">Register</button>
                        </form>
                        <div className={styles.NavigateBtn} >
                            <a href="/users/signin">sign in</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
  export default SignUp;
  