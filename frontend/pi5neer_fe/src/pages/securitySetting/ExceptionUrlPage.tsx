import React, { useState, useEffect, useRef } from 'react'
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material-next/Divider';
import TextField from '@mui/material/TextField';


import { DataGrid, GridColDef, GridRowParams, GridRowId } from '@mui/x-data-grid';
import { Dictionary } from '@reduxjs/toolkit';


type Props = {}
let rows = [
  {id : '0' , URL : '0', reason : 'test' } //line for test
];

interface exceptionip  {
  id : string,
  URL : string,
  reason : string
}


const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 100 },
  { field: 'URL', headerName: '적용 URL', width: 350 },
  { field: 'reason', headerName: '적용사유', width: 500 },
];

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 1000,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  m:'2rem'
};



const ExceptionIpPage = (props: Props) => {

    const [deletebutton, setdeletebutton] = useState(false);

    const urlref = useRef('0');
    const reasonref = useRef('0');

    let now_id = -1;
    const [open, setOpen] = React.useState(false);

    const handleOpen = function(params : GridRowParams) {
      const rowData:exceptionip = params.row as exceptionip;
      now_id = Number(rowData.id);
      console.log(rowData);
      setdeletebutton(true);
      setOpen(true);
    }
    const handleOpenbutton = () => {
      now_id = -1;
      setdeletebutton(false);
      setOpen(true);
    }
    const handleClose = function() {
      now_id = 0;
      setOpen(false);
      console.log(now_id);
    } 

    //get 부분 완료
    const url = '/security_policy/' + 1 + '/exception_url_list';
    fetch(url)
      .then((response) => response.json())
      .then((data) => { 
        rows = data['result'];
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });

    //POST(Add) 부분, PUT(수정) 부분
    const send_button = function() {

      const formdata = new FormData();

      
      formdata.append("URL",urlref.current);
      formdata.append("reason",reasonref.current);

      if(now_id == -1){

        const response = fetch(url,{
          method: 'POST',
          body:formdata
        })
        alert("POST(Add) response is : " + response);
      }
      else {
        formdata.append("request_id",now_id.toString());
        const response = fetch(url,{
          method: 'PUT',
          body:formdata
      })
        alert("PUT(edit) response is : " + response);
      }
    }
    //DELETE(delete) 부분
    const delete_button = function() {
      const response = fetch(url,{
        method: 'DELETE'
      })
      alert(response)
    }
    

  return (
    <Box>
      <Grid>
        <Grid sx={{display: 'flex', justifyContent : "space-between"}}>
          <Box>
            적용 URL 목록
          </Box>
          <Stack direction='row' spacing={3}>
            <Button variant="contained" endIcon={<SendIcon />} onClick={handleOpenbutton}>
              ADD
            </Button>

            
          </Stack>
        </Grid>
        <br></br>
        <div style={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            initialState={{
              pagination: {
                paginationModel: { page: 0, pageSize: 5 },
              },
            }}
            pageSizeOptions={[5, 10]}
            
            onRowClick={handleOpen}
          />
        </div>
      </Grid>
      <br></br>

      <Modal
              open={open}
              onClose={handleClose}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
      >
        <Stack sx={style} spacing = {3}>  
          <Typography id="modal-modal-title" variant="h6" component="h2">
            security INFO
          </Typography>
          <Divider />
            <TextField
              required
              id="outlined-required"
              label="URL"
              defaultValue="/your url/*"
              inputRef={urlref}
            />
            <TextField
              required
              id="outlined-required"
              label="Reason"
              defaultValue="Just"
              inputRef={reasonref}
            />
            <Box display="flex" justifyContent="space-between">
                {deletebutton && <Button variant="contained" endIcon={<DeleteIcon />} onClick={() => delete_button()} >
                Delete this policy
                </Button>
                }
              <Button variant="contained" endIcon={<SendIcon />} onClick={() => send_button()}>
              Send
              </Button>
            </Box>
          </Stack>
        </Modal>

      <Grid>
        <Grid sx={{display: 'flex', justifyContent : "space-between"}}>
          <Box>
            예외 URL 목록
          </Box>
          <Stack direction='row' spacing={3}>
            <Button variant="contained" endIcon={<SendIcon />}>
              ADD
            </Button>
          </Stack>
        </Grid>
        <br></br>
        <div style={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            initialState={{
              pagination: {
                paginationModel: { page: 0, pageSize: 5 },
              },
            }}
            pageSizeOptions={[5, 10]}
            checkboxSelection
          />
        </div>
      </Grid>
    </Box>
  );
}





export default ExceptionIpPage