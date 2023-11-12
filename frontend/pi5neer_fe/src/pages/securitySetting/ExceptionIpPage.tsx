import React from 'react'
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';

import { FixedSizeList, ListChildComponentProps } from 'react-window';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';


type Props = {}

const ExceptionIpPage = (props: Props) => {
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


const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 100 },
  { field: 'ip', headerName: '적용 네트워크 IP', width: 350 },
  { field: 'subnet_mask', headerName: '서브넷 마스크', width: 350 },
  { field: 'reason', headerName: '적용사유', width: 500 },
];

const rows = [
  { id: 1, ip : '142.167.10.0', subnet_mask: '255.255.255.0', reason : 'test'},
  { id: 2, ip : '114.70.0.0', subnet_mask: '255.0.0.0', reason : 'test'},
  { id: 3, ip : '174.1.0.0', subnet_mask: '255.255.0.0', reason : 'test'},
  { id: 4, ip : '124.3.3.0', subnet_mask: '255.255.255.0', reason : 'test'},
  { id: 5, ip : '4.11.0.0', subnet_mask: '255.255.0.0', reason : 'test'},
  { id: 6, ip : '1.0.0.0', subnet_mask: '255.0.0.0', reason : 'test'},
];


export default ExceptionIpPage