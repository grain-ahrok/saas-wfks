import styles from './Auth.module.css';
import { useState } from 'react'; 
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SignUp() {
    const navigate = useNavigate();

    const [cName, setCName] = useState('');
    const [email, setEmail] = useState('');
    const [pw, setPW] = useState('');
    const [doAddr, setDoAddr] = useState('');
    const [ipAddr, setIpAddr] = useState('');
    const [loading, setLoading] = useState(false);

    const signUpAxios = async (e) => {
        e.preventDefault();

        const cn_reg = /^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$/;
        const email_reg = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        const pw_reg = /^(?=.*[a-zA-Z])(?=.*[0-9]).{8,15}$/;
        const do_reg = /^(http:\/\/|https:\/\/)?([0-9a-zA-Z-]+\.)+[a-zA-Z]+(\/\S*)?/;
        const ip_reg = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

        if (!cn_reg.test(cName) || !email_reg.test(email) || !pw_reg.test(pw) || !do_reg.test(doAddr) || !ip_reg.test(ipAddr)) {
            alert('입력값을 확인해주세요.');
            return false;
        }

        setLoading(true);

        try {
            const response = await axios.post('/users/signup', {
                companyName: cName,
                email: email,
                password: pw,
                domain_address: doAddr,
                IP_address: ipAddr,
                membership: 'basic',
            });

            if (response.status === 201) {
                alert('회원가입 되셨습니다. 로그인 해 주세요');
                navigate('/users/signin');
            }
        } catch (err) {
            if (err.response && err.response.status === 400) {
                alert('기존에 가입된 회사이름, 도메인 또는 이메일이 존재합니다.');
            } else {
                alert('에러가 발생했습니다. 관리자에게 문의해주세요\n');
            }
        } finally {
            setLoading(false);
        }
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
                            <input
                                className={styles.InputField}
                                onChange={(e) => setCName(e.target.value)}
                                placeholder="Input Company Name"
                            />
                            <input
                                className={styles.InputField}
                                onChange={(e) => setEmail(e.target.value)}
                                id="email"
                                placeholder="Email address"
                            />
                            <input
                                className={styles.InputField}
                                onChange={(e) => setPW(e.target.value)}
                                id="pw"
                                placeholder="Input Password"
                                type="password"
                            />
                            <input
                                className={styles.InputField}
                                onChange={(e) => setDoAddr(e.target.value)}
                                id="doAddr"
                                placeholder="Domain address"
                            />
                            <input
                                className={styles.InputField}
                                onChange={(e) => setIpAddr(e.target.value)}
                                id="ipAddr"
                                placeholder="IP address"
                            />
                            <button className={styles.LoginBtn} type="submit" disabled={loading}>
                                {loading ? 'Registering...' : 'Register'}
                            </button>
                        </form>
                        <div className={styles.NavigateBtn}>
                            <a href="/users/signin">sign in</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SignUp;
