import { Box, Button, Divider, Modal, Stack, TextField, Typography } from '@mui/material'
import React, { useState } from 'react'
import colorConfigs from '../../../config/colorConfigs'
import { getCookie } from '../../../utils/cookie'
import { authHeaders } from '../../../utils/headers'
import { useNavigate } from 'react-router-dom'

type Props = {
    isOpen : boolean,
    closeModal : any
}


const style = {
    position: 'absolute' as 'absolute',
    top: '45%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 500,
    bgcolor: 'background.paper',
    borderRadius: "12px",
    boxShadow: 24,
    p: 4,
    m: '2rem'
  };

const ExcepUrlCreateModal = (props: Props) => {

    const security_policy_id = getCookie("security_policy_id");
    const url = '/security_policy/' + security_policy_id + '/exception_url_list';

    const navigate = useNavigate();
    const [expUrl, setUrl] = useState('');
    const [desc, setDesc] = useState('');

    const send_button = function () {
        fetch(url, {
          method: 'post',
          headers : authHeaders,
          body: JSON.stringify({
            url : expUrl,
            desc : desc
          })
        }).then((response) => response.json())
          .then((data) => {
            if (data['header']['isSuccessful'] !== true) {
              alert("다시 시도해주세요");
            } else {
              navigate('/customers/security-settings/exception-urls')
              props.closeModal();
            }
          })
          .catch((error) => {
            console.error('요청 중 오류 발생:', error);
          });
      }

    return (
        <Modal
            open={props.isOpen}
            onClose={props.closeModal}>
            <Stack sx={style} spacing={3}>
                <Typography id="modal-modal-title" variant="h6" component="h2">
                    추가하기
                </Typography>
                <Divider />
                <TextField
                    required
                    label="예외 URL"
                    placeholder='예외 URL ex) /test/*'
                    onChange={(e) => setUrl(e.target.value)}
                />
                <TextField
                    label="설명"
                    placeholder='설명'
                    onChange={(e) => setDesc(e.target.value)}
                />
                <Box display="flex" justifyContent="flex-end">
                    <Button sx={{
                        color: colorConfigs.button.white,
                        backgroundColor: colorConfigs.button.blue,
                        border: 1,
                        borderColor: colorConfigs.button.blue,
                        borderRadius: "40px",
                        paddingX: "32px",
                        margin: "4px",
                        width: "130px",
                        "&: hover": {
                            color: colorConfigs.button.blue
                        }
                    }}
                        onClick={() => {send_button()}}
                    >추가하기</Button>
                </Box>
            </Stack>
        </Modal>
    )
}

export default ExcepUrlCreateModal