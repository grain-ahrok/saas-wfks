import React from "react"
import { RouteType } from "./config";
import SecuritySettingLayout from "../pages/securitySetting/SecuritySettingLayout"
import ExceptionUrlPage from "../pages/securitySetting/ExceptionUrlPage"
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import ExceptionIpPage from "../pages/securitySetting/ExceptionIpPage";
import DomainSettingPage from "../pages/domainSetting/DomainSettingPage";
import SpaceDashboardIcon from '@mui/icons-material/SpaceDashboard';
import SubjectIcon from '@mui/icons-material/Subject';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import DashboardPage from "../pages/dashboard/DashboardPage";
import SecurityLogPage from "../pages/securityLog/SecurityLogPage";
import BlockedIpPage from "../pages/securitySetting/BlockedIpPage";
import SqlInjectionPage from "../pages/securityDetailSetting/SqlInjectionPage";
import UrlRegxPage from "../pages/securityDetailSetting/UrlRegxPage";
import XssPage from "../pages/securityDetailSetting/XssPage";
import UpDownloadPage from "../pages/securityDetailSetting/UpDownloadPage";
import EvasionPage from "../pages/securityDetailSetting/EvasionPage";
import AccessControlPage from "../pages/securityDetailSetting/AccessControlPage";
import RequestFloodPage from "../pages/securityDetailSetting/RequestFloodPage";
import CredentialStuffingPage from "../pages/securityDetailSetting/CredentialStuffingPage";
import CookieProtectionPage from "../pages/securityDetailSetting/CookieProtectionPage";
import BufferOverflowPage from "../pages/securityDetailSetting/BufferOverflowPage";
import DirectoryListingPage from "../pages/securityDetailSetting/DirectoryListingPage";
import ShellCodePage from "../pages/securityDetailSetting/ShellCodePage";
import DetailPolicyWrapper from "../pages/securityDetailSetting/DetailPolicyWrapper";
import SignUp from "../pages/auth/SignUp";
import SignIn from "../pages/auth/SignIn";


const appUserRoutes: RouteType[] = [
    {
        path: "/users/signup",
        state: "signup",
        element: <SignUp />
    },
    {
        path: "/users/signin",
        state: "signin",
        element: <SignIn />
    }
]

const appCustomerRoutes: RouteType[] = [
    {
        index: true,
        element: <DashboardPage />,
        state: "dashboard"
    },
    {
        index: true,
        path: "/customers/dashboard",
        element: <DashboardPage />,
        state: "dashboard",
        sidebarProps: {
            displayText: "대시보드",
            icon: <SpaceDashboardIcon />
        }
    },
    {
        index: true,
        path: "/customers/security-logs",
        element: <SecurityLogPage />,
        state: "security-logs",
        sidebarProps: {
            displayText: "보안로그",
            icon: <SubjectIcon />
        }
    },
    {
        index: false,
        path: "/customers/security-settings",
        element: <SecuritySettingLayout />,
        state: "security-settings",
        sidebarProps: {
            displayText: "보안 설정 관리",
            icon: <AdminPanelSettingsIcon />
        },
        child: [
            {
                path: "/customers/security-settings/exception-urls",
                element: <ExceptionUrlPage />,
                state: "security-settings.exception-urls",
                sidebarProps: {
                    displayText: "예외 URL 관리"
                }
            },
            {
                path: "/customers/security-settings/exception-ips",
                element: <ExceptionIpPage />,
                state: "security-settings.exception-ips",
                sidebarProps: {
                    displayText: "예외 IP 관리"
                }
            },
            {
                path: "/customers/security-settings/blocked-ips",
                element: <BlockedIpPage />,
                state: "security-settings.blocked-ips",
                sidebarProps: {
                    displayText: "차단 IP 관리"
                }
            },
            {
                path: "/customers/security-settings/policy-details",
                element: <DetailPolicyWrapper children={<SqlInjectionPage></SqlInjectionPage>}></DetailPolicyWrapper>,
                state: "security-settings.policy-details.sql-injection",
                sidebarProps: {
                    displayText: "정책 상세 관리"
                },
            }
        ]
    },
    {
        path: "/customers/domain-settings",
        element: <DomainSettingPage />,
        state: "domain-settings",
        sidebarProps: {
            displayText: "도메인 설정 관리",
            icon: <ManageAccountsIcon />
        }
    }
]


const appPolicyDetailRoutes: RouteType[] = [
    {
        path: "/customers/security-settings/policy-details/sql-injection",
        element: <SqlInjectionPage />,
        state: "security-settings.policy-details.sql-injection",
        sidebarProps: {
            displayText: "SQL-Injection"
        }
    },
    {
        path: "/customers/security-settings/policy-details/url_regex",
        element: <UrlRegxPage />,
        state: "security-settings.policy-details.url_regex",
        sidebarProps: {
            displayText: "URL 정규식 검사"
        }
    },
    {
        path: "/customers/security-settings/policy-details/xss",
        element: <XssPage />,
        state: "security-settings.policy-details.xss",
        sidebarProps: {
            displayText: "XSS"
        }
    },
    {
        path: "/customers/security-settings/policy-details/directory_listing",
        element: <DirectoryListingPage />,
        state: "security-settings.policy-details.directory_listing",
        sidebarProps: {
            displayText: "디렉토리 리스팅"
        }
    },
    {
        path: "/customers/security-settings/policy-details/shellcode",
        element: <ShellCodePage />,
        state: "security-settings.policy-details.shellcode",
        sidebarProps: {
            displayText: "쉘코드"
        }
    },
    {
        path: "/customers/security-settings/policy-details/up-download",
        element: <UpDownloadPage />,
        state: "security-settings.policy-details.up-download",
        sidebarProps: {
            displayText: "업/다운로드 검사"
        }
    },
    {
        path: "/customers/security-settings/policy-details/request-flood",
        element: <RequestFloodPage />,
        state: "security-settings.policy-details.request-flood",
        sidebarProps: {
            displayText: "과다 요청 제어"
        }
    },
    {
        path: "/customers/security-settings/policy-details/access-control",
        element: <AccessControlPage />,
        state: "security-settings.policy-details.access-control",
        sidebarProps: {
            displayText: "접근 제어"
        }
    },
    {
        path: "/customers/security-settings/policy-details/evasion",
        element: <EvasionPage />,
        state: "security-settings.policy-details.evasion",
        sidebarProps: {
            displayText: "검사 회피"
        }
    },
    {
        path: "/customers/security-settings/policy-details/credential-stuffing",
        element: <CredentialStuffingPage />,
        state: "security-settings.policy-details.credential-stuffing",
        sidebarProps: {
            displayText: "크리덴셜 스터프"
        }
    },
    {
        path: "/customers/security-settings/policy-details/cookie-protection",
        element: <CookieProtectionPage />,
        state: "security-settings.policy-details.cookie-protection",
        sidebarProps: {
            displayText: "쿠키 보호"
        }
    },
    {
        path: "/customers/security-settings/policy-details/buffer-overflow",
        element: <BufferOverflowPage />,
        state: "security-settings.policy-details.buffer-overflow",
        sidebarProps: {
            displayText: "버퍼 오버 플로우"
        }
    },

]

const appRoutes = {
    appUserRoutes: appUserRoutes,
    appCustomerRoutes: appCustomerRoutes,
    appPolicyDetailRoutes: appPolicyDetailRoutes
}

export default appRoutes;