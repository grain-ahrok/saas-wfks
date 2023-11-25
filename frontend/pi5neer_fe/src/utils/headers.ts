import { getCookie } from "./cookie";

const basicHeaders = new Headers();
basicHeaders.append('Content-Type', 'application/json');

const authHeaders = new Headers();
authHeaders.append('Content-Type', 'application/json');
authHeaders.append('Authorization', `Bearer ${getCookie("access_token")}`);

export {authHeaders, basicHeaders}