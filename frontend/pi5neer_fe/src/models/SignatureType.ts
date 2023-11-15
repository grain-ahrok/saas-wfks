import { securityStatus } from "../enums/StatusEnum"

export type SignatureType = {
    id: Number
    status?: securityStatus
    warning: Number
    title: String
    poc_example: String
    impact: String
}