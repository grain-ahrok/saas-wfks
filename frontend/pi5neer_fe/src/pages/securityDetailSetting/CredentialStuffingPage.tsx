import React, { useEffect, useState } from 'react'
import ActiveStatusBox from './component/ActiveStatusBox';
import { Box } from '@mui/material';

type Props = {
  name : string,
}

const CredentialStuffingPage = (props: Props) => {

  const security_policy_id = 1;
      const url = `/security_policy/${security_policy_id}/credential_stuffing`;

    const [status, setStatus] = useState('');
  
    useEffect(() => {
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          setStatus(data['status']);
        })
        .catch((error) => {
          console.error('요청 중 오류 발생:', error);
        });
    }, [url]);

    function handleValueChange(value: string) {
      fetch(url, {
        method : 'put', 
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

export default CredentialStuffingPage