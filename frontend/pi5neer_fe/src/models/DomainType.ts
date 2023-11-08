import { activeStatus } from "../enums/StatusEnum"

export type DomainType = {
    id : number,
    ipVer : ipVer,
    ip : string,
    protocol? : protocol, 
    port? : number,
    status : activeStatus,
    domain : {
        id : number,
        name : string
    }[],
}

export enum ipVer {
    ipv4 = "ipv4",
    ipv6 = 'ipv6'
};

export enum protocol {
    http = "http",
    https = "https"
};