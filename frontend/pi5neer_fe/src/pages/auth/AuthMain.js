import styles from './AuthMain.module.css';

function AuthMain() {
    return (
        <div className={styles.Screen}>
            <div className={styles.LogoWindow}>
                <h1>Pi5neer</h1>
                <p>더 빠르고 안정적이며 안전한 서비스로 고객의 비즈니스 가치를 극대화시킵니다</p>
            </div>
            <div className={styles.InputWindow}>
                <div className={styles.ShadowBox}>
                    <div className={styles.InputPadding}>
                        <h3>Login</h3>
                        <input className={styles.InputField}></input>
                        <input className={styles.InputField}></input>
                        <button className={styles.LoginBtn} type="button">Login</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
  export default AuthMain;
  