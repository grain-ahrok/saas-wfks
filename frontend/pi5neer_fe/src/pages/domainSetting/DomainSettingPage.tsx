import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import DomainItem from './DomainItem'
import DomainNoticeBox from './DomainNoticeBox'


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
      <DomainNoticeBox/>
      {domainList.map((domain, index) => (
        <DomainItem domain={domain}/>
      ))}
    </Box>
  )
}

export default DomainSettingPage