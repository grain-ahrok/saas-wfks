import { activeStatus } from "../enums/StatusEnum"

export type AppType = {
    id: number
    ip: string
    ipVer? : ipVer
    port?: number
    status: activeStatus
    domain: string
    server_name: string
    domain_list: DomainType[]
}

export type DomainType = {
    id: number
    name: string
    desc: string
}

export enum ipVer {
    ipv4 = "ipv4",
    ipv6 = 'ipv6'
};

export enum protocol {
    http = "http",
    https = "https"
};