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
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

import { DataGrid, GridColDef, GridRowParams, GridRowId } from '@mui/x-data-grid';
import { Dictionary } from '@reduxjs/toolkit';

type Props = {}
let rows = [
  {
    id : 0,
    time : '2023.10.17 23:00:01',
    detected_request : '2137',
    ip : '1.3.5.7',
    url : '/watswonBlog',
    threat_level: '높음',
    category:'SQL Injecdtion',
    state :'차단'
  }
];

interface securitylog  {
  time : string,
  detected_request : string,
  ip : string,
  url : string,
  threat_level : string,
  category : string,
  state : string
}


const columns: GridColDef[] = [
  { field: 'time', headerName: '시간', width: 200 , align:'left'},
  { field: 'detected_request', headerName: '감지된 요청 수', width: 170, align:'left' },
  { field: 'ip', headerName: 'IP 주소', width: 200 , align:'left'},
  { field: 'url', headerName: 'URL', width: 250 , align:'left'},
  { field: 'threat_level', headerName: '공격 위험 수준', width: 200, align:'left' },
  { field: 'category', headerName: '분류', width: 150 , align:'left'},
  { field: 'state', headerName: '처리 상태', width: 180 , align:'left'},

];


const text_style = {
  fontSize: '20px',
  fontWeight: 'bold'
};

const text_style2 = {
  fontSize: '20px',
}

const SecurityLogPage = (props: Props) => {
  
  const [age, setAge] = React.useState('');

  const handleChange = (event: SelectChangeEvent) => {
  setAge(event.target.value as string);
  };

  return (
    <Box>
      <Grid container spacing={2} marginBottom={2} alignItems="center">
        
          <Typography variant="body1" style={Object.assign({marginLeft: '20px'}, text_style)}>
           도메인 : 
          </Typography>

          <Grid item>
          <FormControl style={{ width: '200px' }}>
             <InputLabel id="domain-label">Domain</InputLabel>
             <Select
               labelId="domain-label"
               id="domain-select"
               value={age}
               label="Domain"
               onChange={handleChange}
             >
               <MenuItem value={10}>www.watson.com</MenuItem>
               <MenuItem value={20}>www.hacking.co.kr</MenuItem>
               <MenuItem value={30}>www.client.site.com</MenuItem>
             </Select>
             </FormControl>
         </Grid>
         
         <Grid item style = {{marginLeft: 'auto'}}> 
          <Button variant="outlined" style ={{margin: '10px'}}>
            <Typography style={text_style2}>
              Filters 
            </Typography>
          </Button>
          <Button variant="outlined" style ={{margin: '10px'}}>
            <Typography style={text_style2}>
              Export 
            </Typography>
          </Button>
         </Grid>
      </Grid>

      <Box>
        <Grid>
          <div style={{ height: 700, width: '100%' }}>
            <DataGrid
              rows={rows}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 5 },
                },
              }}
              pageSizeOptions={[5, 10]}
            />
          </div>
        </Grid>
      </Box>
    </Box>
  )
}

export default SecurityLogPage