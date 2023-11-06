import { Box, Typography } from '@mui/material'
import React, { useEffect, useState } from 'react'
import colorConfigs from '../../config/colorConfigs'
import DomainItem from './DomainItem'


const DomainSettingPage = () => {
  // TODO : app 저장소에서 불러오기

  const [domainList, setData] = useState([]);
  useEffect(() => {
    const url = '/app/' + 1 + '/domain-list';
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setData(data['result']);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
    }, []);

  return (
    <Box>
      <Box sx={{
        backgroundColor: colorConfigs.noticeBoxBg,
        padding: "20px",
        marginBottom: "20px",
        borderRadius: "24px",
      }}>
        <Typography sx={{
          fontSize: "16px",
          margin: "4px"
        }}>
          💡 도메인 설정 시 유의 사항
        </Typography>
        <Typography sx={{
          fontSize: "14px",
          marginLeft: "24px"
        }}>
          DNS 서버의 IP를 43.200.213.102:8443로 <br />
          도메인을 wf.awstest.piolink.net로 업데이트해야 합니다.
        </Typography>
      </Box>
      {domainList.map((domain, index) => (
        <DomainItem domain={domain}></DomainItem>
      ))}
    </Box>
  )
}

export default DomainSettingPage