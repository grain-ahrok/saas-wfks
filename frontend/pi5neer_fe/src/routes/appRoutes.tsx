import React from "react"
import { RouteType } from "./config";
import SecuritySettingLayout from "../pages/securitySetting/SecuritySettingLayout"
import ExceptionUrlPage from "../pages/securitySetting/ExceptionUrlPage"
import DashboardOutlinedIcon from "@mui/icons-material/DashboardOutlined"
import ExceptionIpPage from "../pages/securitySetting/ExceptionIpPage";
import DomainSettingPage from "../pages/domainSetting/DomainSettingPage";
import {FormatListBulletedOutlined } from "@mui/icons-material";
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
        path: "/dashboard",
        element: <DashboardPage/>,
        state: "dashboard",
        sidebarProps: {
            displayText: "대시보드",
            icon: <FormatListBulletedOutlined />
        }
    },
    {
        path: "/security-logs",
        element: <SecurityLogPage />,
        state: "security-logs",
        sidebarProps: {
            displayText: "보안로그",
            icon: <FormatListBulletedOutlined />
        }
    },
    {
        path: "/security-settings",
        element: <SecuritySettingLayout />,
        state: "security-settings",
        sidebarProps: {
            displayText: "보안 설정 관리",
            icon: <DashboardOutlinedIcon />
        },
        child: [
            {
                index: true,
                element: <ExceptionUrlPage />,
                state: "security-settings.index",
            },
            {
                path: "/security-settings/exception-urls",
                element: <ExceptionUrlPage />,
                state: "security-settings.exception-urls",
                sidebarProps: {
                    displayText: "예외 URL 관리"
                }
            },
            {
                path: "/security-settings/exception-ips",
                element: <ExceptionIpPage />,
                state: "security-settings.exception-ips",
                sidebarProps: {
                    displayText: "예외 IP 관리"
                }
            },
            {
                path: "/security-settings/blocked-ips",
                element: <BlockedIpPage />,
                state: "security-settings.blocked-ips",
                sidebarProps: {
                    displayText: "차단 IP 관리"
                }
            },
            {
                path: "/security-settings/policy-details",
                element: <DetailPolicyPage />,
                state: "security-settings.policy-details",
                sidebarProps: {
                    displayText: "정책 상세 관리"
                }
            }
        ]
    },
    {
        path: "/domain-settings",
        element: <DomainSettingPage />,
        state: "domain-settings",
        sidebarProps: {
            displayText: "도메인 설정 관리",
            icon: <FormatListBulletedOutlined />
        }
    }
]

export default appRoutes;