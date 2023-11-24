import { useState } from "react";
import { useNavigate } from "react-router-dom"
import axios from "axios";
import { Box, Button, TextField, Typography } from "@mui/material";
import styleConfigs from "../../config/styleConfigs";
import { setCookie } from "../../utils/cookie";

function SignIn() {

    const navigate = useNavigate();

    const [cName, setCName] = useState("");
    const [pw, setPW] = useState("");

    const signInAxios = async (e: any) => {
        e.preventDefault();

        const cn_reg = /^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$/;
        const pw_reg = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,15}$/;
        if (!cn_reg.test(cName)) {
            alert("회사 이름을 확인해주세요.");
            return;
        }
        if (!pw_reg.test(pw)) {
            alert("비밀번호를 확인해주세요.");
            return;
        }

        await axios.post("/users/signin", {
            companyName: cName,
            password: pw
            })
            .then((response) => {
                if (response.status === 200) {
                    const acessToken = response.data['access_token']
                    setCookie("acessToken", acessToken);
                    return navigate("/customers/dashboard");
                }
            })
            .catch((err) => {
                if (err.response.status === 401) {
                    alert("회사이름과 비밀번호를 다시 확인 해주세요");
                    return;
                }
                alert("에러가 발생했습니다. 관리자에게 문의해주세요\n" + err);
            });
    };


    return (
        <Box sx={{ display: "flex", height: "100vh" }}>
            <Box sx={{ width: "50%", margin: "auto", padding: "80px" }}>
                <h1>Pi5neer</h1>
                <p>더 빠르고 안정적이며 안전한 서비스로 고객의 비즈니스 가치를 극대화시킵니다</p>
            </Box>

            <Box sx={{ width: "50%", margin: "auto", padding: "80px", minWidth: "460px" }}>
                <Box sx={{ padding: "30px", background: "white", boxShadow: styleConfigs.boxShadow, borderRadius: "30px" }}>
                    <Box sx={{ paddingTop: "30px", paddingBottom: "60px" }}>
                        <Typography variant="h4" paddingBottom="16px" fontWeight="700">Sign in</Typography>

                        <TextField
                            fullWidth
                            size='small'
                            placeholder="Input Company Name"
                            sx={{ height: "42px", padding: "4px" }}
                            onChange={(e) => setCName(e.target.value)} />
                        <TextField
                            fullWidth
                            size='small'
                            placeholder="Input Password"
                            sx={{ height: "42px", padding: "4px" }}
                            type="password"
                            onChange={(e) => setPW(e.target.value)} />

                        <Button
                            onClick={signInAxios}
                            sx={{
                                marginTop: "4px",
                                width: "100%",
                                height: "42px",
                                borderRadius: "8px",
                                background: "#18A0FB",
                                color: "white",
                                border: "1px solid #18A0FB"
                            }}>
                            Login</Button>
                        <Box sx={{ marginTop: "6px", display: "flex", justifyContent: "center", color: "rgba(17, 67, 101, 0.50)" }}>
                            <a href="/users/signup">sign up</a>
                            <Box>&nbsp;/&nbsp;</Box>
                            <a href="#">forgot my password</a>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </Box>
    );
}
export default SignIn;
