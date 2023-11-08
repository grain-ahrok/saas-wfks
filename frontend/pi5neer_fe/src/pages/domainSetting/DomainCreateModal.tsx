import { Box, Button, Divider, TextField, Typography } from '@mui/material'
import React from 'react'
import ModalWrapper from '../../components/layout/ModalWrapper'
import colorConfigs from '../../config/colorConfigs'

type Props = {
  isOpen: boolean,
  closeModal: any
}

const DomainCreateModal = ({ isOpen, closeModal }: Props) => {
  return (
    <ModalWrapper isOpen={isOpen} closeModal={closeModal}>
      <Box sx={{
        padding : "20px",
        borderRadius : "24px",
      }}>
        <Typography variant='h6'>추가하기</Typography>
        <Divider sx={{
          marginTop : "8px",
          marginBottom : "16px",
          borderWidth : "1px",
          color : colorConfigs.noticeBoxBg
        }}/>

        <Box display="flex" padding="4px"> 
          <Typography width="20%">IP 주소</Typography>
          <Box width="80%" >
            <TextField fullWidth size='small'></TextField>
          </Box>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">포트 번호</Typography>
          <TextField size='small'></TextField>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">도메인 주소</Typography>
          <Box width="80%">
            <TextField fullWidth size='small'></TextField>
          </Box>
        </Box>

        <Box sx={{
          float : "right",
          paddingBottom : "20px"
        }}>
          <Button sx={{
            color : colorConfigs.button.white,
            backgroundColor : colorConfigs.button.blue,
            border : 1,
            borderColor : colorConfigs.button.blue,
            borderRadius : "40px",
            paddingX : "32px",
            margin : "4px",
            "&: hover" : {
              color : colorConfigs.button.blue
            }
          }}>추가하기</Button>
        </Box>
      </Box>
    </ModalWrapper>
  )
}

export default DomainCreateModal