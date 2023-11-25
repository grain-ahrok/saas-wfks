import { Box, Button } from '@mui/material'
import React, { useEffect, useState } from 'react'
import DomainItem from './DomainItem'
import DomainNoticeBox from './DomainNoticeBox'
import colorConfigs from '../../config/colorConfigs'
import DomainCreateModal from './DomainCreateModal'
import { getCookie } from '../../utils/cookie'


const DomainSettingPage = () => {

  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  const [appList, setData] = useState([]);

  const app_id = getCookie("wf_app_id");
  const token = getCookie("access_token");
  const url = '/app/' + app_id + '/domain-list';
  useEffect(() => {
    
    fetch(url, {
      headers : {"Authorization": `Bearer ${token}`, 
      "Content-Type": "application/json"
    },
    })
      .then((response) => response.json())
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
    }, []);

  return (
    <Box>
        <Box sx={{
          textAlign : "right",
          marginBottom : "8px"
        }}>
          <Button sx={{
            color : colorConfigs.button.blue,
            backgroundColor : colorConfigs.button.white,
            border : 1,
            borderColor : colorConfigs.button.blue,
            borderRadius : "40px",
            paddingX : "32px",
            margin : "4px",
            "&: hover" : {
            }
          }}
          onClick={openModal}
          >
            도메인 추가하기
          </Button>
          <DomainCreateModal isOpen={isModalOpen} closeModal={closeModal}/>
      </Box>
      <DomainNoticeBox></DomainNoticeBox>
      <Box sx={{display : 'flex', flexWrap : 'wrap'}}>
      {appList.map((app) => (
        <DomainItem app={app}/>
      ))}
      </Box>
    </Box>
  )
}

export default DomainSettingPage