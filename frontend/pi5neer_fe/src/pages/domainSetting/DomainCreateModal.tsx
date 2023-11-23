import { Box, Button, Divider, FormControlLabel, IconButton, Radio, RadioGroup, TextField, Typography } from '@mui/material'
import React, { ChangeEvent, useState } from 'react'
import ModalWrapper from '../../components/layout/ModalWrapper'
import colorConfigs from '../../config/colorConfigs'
import { DomainType } from '../../models/DomainType'
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import { activeStatus } from '../../enums/StatusEnum'
import DomainNoticeBox from './DomainNoticeBox'

type Props = {
  isOpen: boolean,
  closeModal: any
}

const DomainCreateModal = ({ isOpen, closeModal }: Props) => {

  const [serverName, setServerName] = useState('');
  const [ip, setIP] = useState('');
  const [port, setPort] = useState('');
  const [protocol, setProtocol] = useState('');
  const [domainListName, setDomainName] = useState<DomainType[]>([{name : ''}]);

  function createDomain() {
    const url = '/app/' + 1 + '/domain-list';

    let jsonData = {
      ip: ip,
      port: port,
      protocol : protocol,
      status: activeStatus.enable,
      domain_list: domainListName,
      server_name: serverName
    }

  fetch(url, { method: 'post', body: JSON.stringify(jsonData) })
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


  const handleChange = (event : ChangeEvent<HTMLInputElement>) => {
    setProtocol(event.target.value);
  };


  const addInput = () => {
    if(domainListName.every((item) => item.name !== '') && domainListName.length <= 5 ) {
      const newDomain = {
        name : "",
        desc : ""
      }
      setDomainName([...domainListName, newDomain]);
    }
  };

  const removeInput = (index : number) => {
    if(domainListName.length === 1) return;
    const newInputValues = [...domainListName, ];
    newInputValues.splice(index, 1);
    setDomainName(newInputValues);
  };

  const handleInputChange = (index : number, value : string) => {
    const newInputValues = [...domainListName];
    newInputValues[index].name = value
    setDomainName(newInputValues);
  };

  const renderInputs = () => {
    return domainListName.map((item, index) => (
      <Box display="flex">
      <TextField
        fullWidth
        size='small'
        key={index}
        value={item.name}
        onChange={(e) => handleInputChange(index, e.target.value)}
      />
      <IconButton
          color="secondary"
          onClick={() => removeInput(index)}
          aria-label="delete">
          <RemoveCircleOutlineIcon />
        </IconButton>
      </Box>
    ));
  };

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
        <DomainNoticeBox />

        <Box display="flex" padding="4px">
          <Typography width="20%">서버 이름</Typography>
          <Box width="80%" >
            <TextField fullWidth size='small' value={serverName} onChange={(e) => setServerName(e.target.value)}></TextField>
          </Box>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">프로토콜</Typography>
          <Box width="80%" >
            <RadioGroup
              row
              aria-label="protocol"
              name="protocol"
              value={protocol}
              onChange={handleChange}>
              <FormControlLabel value="http" control={<Radio />} label="HTTP" />
              <FormControlLabel value="https" control={<Radio />} label="HTTPS" />
            </RadioGroup>
          </Box>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">IP 주소</Typography>
          <Box width="80%" >
            <TextField fullWidth size='small' value={ip} onChange={(e) => setIP(e.target.value)}></TextField>
          </Box>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">포트 번호</Typography>
          <TextField size='small' value={port} onChange={(e) => setPort(e.target.value)}></TextField>
        </Box>

        <Box display="flex" padding="4px">
          <Typography width="20%">도메인 주소</Typography>
          <Box width="80%">
            {renderInputs()}
            <Button onClick={addInput} >추가하기</Button>
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
          }}
          onClick={createDomain}
          >추가하기</Button>
        </Box>
      </Box>
    </ModalWrapper>
  )
}

export default DomainCreateModal