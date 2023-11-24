import React, { useEffect, useState } from 'react'
import ActiveStatusBox from './component/ActiveStatusBox';
import { Box } from '@mui/material';
import SignatureListBox from './component/SignatureListBox';
import { getCookie } from '../../utils/cookie';

type Props = {
  name : string,
}

const DirectoryListingPage = (props: Props) => {

  const security_policy_id = getCookie("security_policy_id");
  const url = `/security_policy/${security_policy_id}/directory_listing`;
  const token = getCookie("access_token");
  const [status, setStatus] = useState('');
  const [sigList, setData] = useState([]);

  useEffect(() => {
    fetch(url, {
      headers : {"Authorization": `Bearer ${token}`},
    })
      .then((response) => response.json())
      .then((data) => {
        setStatus(data['result']['status']);
        setData(data['result']['sig_list']);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  }, [url]);

  
  function handleValueChange(value: string) {
    fetch(url, {
      method : 'put', 
      headers: {'Content-Type': 'application/json', "Authorization": `Bearer ${token}`},
      body : JSON.stringify({status : value})})
      .then((response) => response.json())
      .then((data) => {
        if(data['header']['resultMessage'] === 'ok')
        setStatus(value);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  };


  return (
    <Box>
      <Box>
        <ActiveStatusBox name={props.name} status={status} onValueChange={handleValueChange} />
      </Box>
      <SignatureListBox sigList={sigList} />
    </Box>
  )
}

export default DirectoryListingPage