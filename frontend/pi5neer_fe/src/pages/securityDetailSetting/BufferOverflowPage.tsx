import { Box } from '@mui/material';
import React, { useEffect, useState } from 'react'
import ActiveStatusBox from './component/ActiveStatusBox';
import { getCookie } from '../../utils/cookie';
import { authHeaders } from '../../utils/headers';

type Props = {
  name : string,
}

const BufferOverflowPage = (props: Props) => {

  const security_policy_id = getCookie("security_policy_id");
  const url = `/security_policy/${security_policy_id}/buffer_overflow`;
  
  const [status, setStatus] = useState('');

  useEffect(() => {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setStatus(data['result']['status']);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  }, [url]);

  function handleValueChange(value: string) {
    fetch(url, {
      method : 'put', 
      headers: authHeaders,
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
    </Box>
  )
}

export default BufferOverflowPage