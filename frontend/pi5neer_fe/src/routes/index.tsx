import { ReactNode } from "react";
import { RouteType } from "./config";
import appRoutes from "./appRoutes";
import { Route } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper";
import DetailPolicyWrapper from "../pages/securityDetailSetting/DetailPolicyWrapper";
import MainLayout from "../components/layout/MainLayout";

const generateRoute = (): ReactNode => {

    const users: RouteType[] = appRoutes.appUserRoutes;
    const customers: RouteType[] = appRoutes.appCustomerRoutes;
    const policyDetails: RouteType[] = appRoutes.appPolicyDetailRoutes;

    return [
        users.map((route, index) => (
            <Route path={route.path} element={route.element} />
        )),
        <Route path="/" element={<MainLayout />}>
            {customers.map((route, index) => (
                route.index ? (
                    <Route index path={route.path} element={
                        <PageWrapper state={route.state}>
                            {route.element}
                        </PageWrapper>} />
                ) : (
                    <Route path={route.path} element={
                        <PageWrapper state={route.child ? undefined : route.state}>
                            {route.element}
                        </PageWrapper>
                    } key={index}>
                        {
                            route.child && route.child.map((route, index) => (
                                <Route index path={route.path} element={
                                    <PageWrapper state={route.state}>
                                        {route.element}
                                    </PageWrapper>} />
                            )
                            )
                        }
                    </Route>
                )
            ))}</Route>,
        <Route path="/" element={<MainLayout />}>
            {policyDetails.map((route, index) => (
                <Route path={route.path} element={
                    <PageWrapper>
                        <DetailPolicyWrapper state={route.state}>
                            {route.element}
                        </DetailPolicyWrapper>
                    </PageWrapper>
                }></Route>
            ))}
        </Route>

    ]
}
export const routes: ReactNode = generateRoute(); 