import React from 'react'
import { DomainType } from '../../models/DomainType'
import { Box, IconButton, Typography } from '@mui/material'
import styleConfigs from '../../config/styleConfigs'
import colorConfigs from '../../config/colorConfigs'
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';
import { activeStatus } from '../../enums/StatusEnum'

type Props = {
    domain: DomainType
}

const DomainItem = ({ domain }: Props) => {
    return (
        <Box 
            sx={{
                justifyContent: 'space-between',
                display: "flex",
                padding: "25px 40px",
                borderRadius: "24px",
                marginTop: "18px",
                marginBottom: "18px",
                boxShadow: styleConfigs.boxShadow
            }}>
            <Box>
                <Box display="flex">
                    <Typography sx={{
                        width: "130px",
                    }}>
                        IP 주소
                    </Typography>
                    <Typography>
                        {domain.ipAddr}
                    </Typography>
                </Box>
                {domain.domain.map((item, index) => (
                    <Box display="flex">
                        {index === 0
                            ? <Typography sx={{ width: "130px" }}>
                                도메인 주소
                            </Typography>
                            : <Typography sx={{ width: "130px" }} />}
                        <Typography>
                            도메인 주소 {item.name}
                        </Typography>
                    </Box>
                ))}
                <Box display="flex">
                    <Typography sx={{
                        width: "130px",
                    }}>
                        상태
                    </Typography>
                    {domain.status === activeStatus.enable
                        ? <Typography color={colorConfigs.stauts.enable} >활성화</Typography>
                        : <Typography color={colorConfigs.stauts.disable}>비활성화</Typography>
                    }
                </Box>
                
            </Box>
            <IconButton sx={{
                width : "45px",
                height : "45px"
            }}>
                <DriveFileRenameOutlineIcon/>
            </IconButton>
        </Box>
    )
}

export default DomainItem