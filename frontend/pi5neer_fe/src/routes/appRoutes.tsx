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
import DetailPolicyPage from "../pages/securitySetting/DetailPolicyPage";


const appRoutes: RouteType[] = [
    {
        index: true,
        element: <DashboardPage />,
        state: "dashboard"
    },
    {
        path: "/customers/dashboard",
        element: <DashboardPage/>,
        state: "dashboard",
        sidebarProps: {
            displayText: "대시보드",
            icon: <SpaceDashboardIcon />
        }
    },
    {
        path: "/customers/security-logs",
        element: <SecurityLogPage />,
        state: "security-logs",
        sidebarProps: {
            displayText: "보안로그",
            icon: <SubjectIcon />
        }
    },
    {
        path: "/customers/security-settings",
        element: <SecuritySettingLayout />,
        state: "security-settings",
        sidebarProps: {
            displayText: "보안 설정 관리",
            icon: <AdminPanelSettingsIcon />
        },
        child: [
            {
                index: true,
                element: <ExceptionUrlPage />,
                state: "security-settings.index",
            },
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
                element: <DetailPolicyPage />,
                state: "security-settings.policy-details",
                sidebarProps: {
                    displayText: "정책 상세 관리"
                }
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

export default appRoutes;