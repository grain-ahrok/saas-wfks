import { activeStatus } from "../enums/StatusEnum"

export type AppType = {
    id: number
    ip: string
    protocol? : protocolEnum
    ip_ver? : ipVerEnum
    port?: number
    status: activeStatus
    server_name: string
    domain_list: DomainType[]
}

export type DomainType = {
    id?: number
    name: string
    desc?: string
}

export enum ipVerEnum {
    ipv4 = "ipv4",
    ipv6 = 'ipv6'
};

export enum protocolEnum {
    http = "http",
    https = "https"
};