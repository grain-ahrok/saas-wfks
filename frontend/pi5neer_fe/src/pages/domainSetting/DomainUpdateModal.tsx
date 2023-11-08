import { Box, Button, Divider, Switch, TextField, Typography } from '@mui/material'
import React, { useState } from 'react'
import ModalWrapper from '../../components/layout/ModalWrapper'
import colorConfigs from '../../config/colorConfigs'
import DomainNoticeBox from './DomainNoticeBox'
import { DomainType } from '../../models/DomainType'
import { activeStatus } from '../../enums/StatusEnum'

type Props = {
  isOpen: boolean,
  closeModal: any,
  domain: DomainType
}

const DomainUpdateModal = (props: Props) => {

  const [ip, setIP] = useState(props.domain.ip);
  const [port, setPort] = useState(props.domain.port);
  const [domainName, setDomainName] = useState(props.domain.domain[0].name);
  const [status, setStatus] = useState(props.domain.status === activeStatus.enable ? true : false)


  function updateDomain() {
    const url = '/app/' + 1 + '/domain-list';

    let jsonData = {
      id: props.domain.id,
      ip: ip,
      port: port,
      status: status ? activeStatus.enable : activeStatus.disable,
      domain: {
        id: props.domain.domain[0].id,
        name: props.domain.domain[0].name
      }
    }

    fetch(url, { method: 'put', body: JSON.stringify(jsonData) })
      .then((response) => response.json())
      .then((data) => {
        if (data.header.isSuccessful !== 'true') {
          alert("다시 시도해주세요");
        }
        window.location.reload();
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  }

  function deleteDomain() {
    const url = '/app/' + 1 + '/domain-list';
    fetch(url, {method : 'delete', body : JSON.stringify(props.domain)})
      .then((response) => response.json())
      .then((data) => {
        if(data.header.isSuccessful !== 'true') {
          alert("다시 시도해주세요");
        }
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
    });
  }

  return (
    <ModalWrapper isOpen={props.isOpen} closeModal={props.closeModal}>
      <Box sx={{
        padding : "20px",
        borderRadius : "24px",
      }}>
        <Typography variant='h6'>수정하기</Typography>
        <Divider sx={{
          marginTop : "8px",
          marginBottom : "16px",
          borderWidth : "1px",
          color : colorConfigs.noticeBoxBg
        }}/>
        <DomainNoticeBox/>
        <Box display="flex" padding="4px"> 
          <Typography width="20%">IP 주소</Typography>
          <Box width="80%" >
            <TextField fullWidth size='small' value={ip} onChange={(e) => setIP(e.target.value)}></TextField>
          </Box>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">포트 번호</Typography>
          <TextField size='small' value={port} onChange={(e) => setPort(Number(e.target.value))}></TextField>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">도메인 주소</Typography>
          <Box width="80%">
            <TextField fullWidth size='small' value={domainName} onChange={(e) => setDomainName(e.target.value)}></TextField>
          </Box>
        </Box>

        <Box display="flex" padding="4px" >
          <Typography width="20%">상태</Typography>
          <Switch defaultChecked checked={status} onChange={(e) => setStatus(e.target.checked)}/>
        </Box>

        <Box sx={{
          float : "right",
          paddingBottom : "20px"
        }}>
          <Button sx={{
            color : colorConfigs.button.red,
            border : 1,
            borderColor : colorConfigs.button.red,
            borderRadius : "40px",
            paddingX : "32px",
            margin : "4px"
          }}
            onClick={deleteDomain}
          >삭제하기</Button>
          
          <Button
            sx={{
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
          }}
            onClick={updateDomain}
          >수정하기</Button>
        </Box>
      </Box>
    </ModalWrapper>
  )
}

export default DomainUpdateModal