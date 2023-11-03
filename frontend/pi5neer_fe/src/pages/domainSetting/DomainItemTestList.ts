import { activeStatus } from "../../enums/StatusEnum";
import { DomainType, ipVer, protocol } from "../../models/DomainType";

export const domainTestList: DomainType[] = [
    {
        id: 1,
        ipVer: ipVer.ipv4,
        ipAddr: "111.222.33.44",
        protocol: protocol.http,
        port: 80,
        status: activeStatus.enable,
        domain: [
            {
                id: 1,
                name: "www.naver.com"
            },
        ],
    },
    {
        id: 2,
        ipVer: ipVer.ipv4,
        ipAddr: "222.33.44.55",
        protocol: protocol.http,
        port: 80,
        status: activeStatus.enable,
        domain: [
            {
                id: 2,
                name: "www.daum.net"
            }, 
            {
                id: 3,
                name: "www.daum.com"
            }
        ],
    }
];
