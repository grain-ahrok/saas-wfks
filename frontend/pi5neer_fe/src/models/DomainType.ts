import { activeStatus } from "../enums/StatusEnum"

export type AppType = {
    id: number
    ip: string
    protocol? : protocolEnum
    version? : ipVerEnum
    port?: number
    status: activeStatus
    server_name: string
    domain_list: DomainType[]
}

export type DomainType = {
    id?: number
    table_id? : number
    domain: string
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