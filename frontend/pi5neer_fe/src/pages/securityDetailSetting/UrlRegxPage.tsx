import { Box } from '@mui/material';
import React, { useEffect, useState } from 'react'
import ActiveStatusBox from './component/ActiveStatusBox';
import SignatureListBox from './component/SignatureListBox';

type Props = {
  name: string,
}

const UrlRegxPage = (props: Props) => {
  const [sigList, setData] = useState([]);

  useEffect(() => {
    const security_policy_id = 1;
    const url = `/security_policy/${security_policy_id}/url_regex/sig_list`;
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
      <Box>
        <ActiveStatusBox name={props.name}></ActiveStatusBox>
      </Box>
      <SignatureListBox sigList={sigList} />
    </Box>
  )
}

export default UrlRegxPage