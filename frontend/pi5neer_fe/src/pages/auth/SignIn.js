import styles from './Auth.module.css';

function SignIn() {
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
                        <input className={styles.InputField} placeholder="Input Company Name"></input>
                        <input className={styles.InputField} placeholder="Input Password" type="password"></input>
                        <button className={styles.LoginBtn} type="button">Login</button>
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
  