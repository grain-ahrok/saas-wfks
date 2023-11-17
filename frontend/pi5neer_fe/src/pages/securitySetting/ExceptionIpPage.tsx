import React, { useState, useEffect } from 'react'
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material-next/Divider';
import TextField from '@mui/material/TextField';


import { FixedSizeList, ListChildComponentProps } from 'react-window';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';


type Props = {}
let rows = [
  {id : 0 , ip : '0', subnet_mast : '0', reason : 'test' } //line for test
];

type exceptionip = {
  id : number,
  ip : string,
  subnet_mask : string,
  reason : string
}

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 100 },
  { field: 'ip', headerName: '적용 네트워크 IP', width: 350 },
  { field: 'subnet_mask', headerName: '서브넷 마스크', width: 350 },
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

    const [open, setOpen] = React.useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const url = '/security_policy/' + 1 + '/exception_ip_list';
    fetch(url)
      .then((response) => response.json())
      .then((data) => { rows = data;
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });

  return (
    <Box>
      <Grid>
        <Grid sx={{display: 'flex', justifyContent : "space-between"}}>
          <Box>
            적용 IP 목록
          </Box>

          <Stack direction='row' spacing={3}>
            <Button variant="outlined" startIcon={<DeleteIcon />}>
              Delete
            </Button>
            <Button variant="contained" endIcon={<SendIcon />} onClick={handleOpen}>
              Edit
            </Button>
            <Modal
              open={open}
              onClose={handleClose}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
            >
              <Stack sx={style} spacing = {3}>  
                <Typography id="modal-modal-title" variant="h6" component="h2">
                  수정하기
                </Typography>
                <Divider />
                
                <TextField
                  required
                  id="outlined-required"
                  label="Required"
                  defaultValue="Hello World"
                />
                <TextField
                  required
                  id="outlined-required"
                  label="Required"
                  defaultValue="Hello World"
                />

                <TextField
                  required
                  id="outlined-required"
                  label="Required"
                  defaultValue="Hello World"
                />
                
                <Box>

                <Button variant="contained" endIcon={<SendIcon />}>
                Send
                </Button>

                </Box>


                </Stack>
            </Modal>
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
      <br></br>
      <Grid>
        <Grid sx={{display: 'flex', justifyContent : "space-between"}}>
          <Box>
            예외 IP 목록
          </Box>
          <Stack direction='row' spacing={3}>
            <Button variant="outlined" startIcon={<DeleteIcon />}>
              Delete
            </Button>
            <Button variant="contained" endIcon={<SendIcon />}>
              Edit
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