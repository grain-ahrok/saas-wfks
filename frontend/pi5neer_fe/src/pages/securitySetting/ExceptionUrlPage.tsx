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


import { DataGrid, GridColDef, GridRowParams } from '@mui/x-data-grid';
import { getCookie } from '../../utils/cookie';
import { URLType } from '../../models/URLType';
import colorConfigs from '../../config/colorConfigs';
import ExcepUrlCreateModal from './component/ExcepUrlCreateModal';
import ExcepUrlUpdateModal from './component/ExcepUrlUpdateModal';


type Props = {}

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 100 },
  { field: 'url', headerName: '적용 URL', width: 350 },
  { field: 'desc', headerName: '적용사유', width: 500 },
];



const ExceptionUrlPage = (props: Props) => {

  const [exceptionUrlList, setExceptionUrlList] = useState<URLType[]>([]);

  const [selectedExpItem, setSelectedExpItem] = useState<URLType | undefined>();

  const [isExpCreateModalOpen, setIsExpCreateModalOpen] = useState(false);
  const openExpCreateModal = () => setIsExpCreateModalOpen(true);
  const closeCreateModal = () => setIsExpCreateModalOpen(false);

  const [isExpUpdateModalOpen, setIsExpUpdateModalOpen] = useState(false);
  const openExpUpdateModal = () => setIsExpUpdateModalOpen(true);
  const closeUpdateModal = () => setIsExpUpdateModalOpen(false);

  

  const security_policy_id = getCookie("security_policy_id");
  const url = '/security_policy/' + security_policy_id + '/exception_url_list';

  const handleSelectionModelChange = (selectionModel: number[]) => {
    const selectedId = selectionModel.length > 0 ? selectionModel[0] : null;
    const selectedRowData = selectedId
      ? exceptionUrlList.find((row) => row.id === selectedId) || null
      : undefined;
      selectedRowData && setSelectedExpItem(selectedRowData);
      openExpUpdateModal()
  };

  useEffect(() => {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if (data['header']['isSuccessful'] === true) {
          setExceptionUrlList(data['result'])
        }
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  }, [url]);


  return (
    <Box paddingRight="50px" paddingLeft="10px" >
      {/* <Box sx={{ display: 'flex', justifyContent: "space-between" }}>
        <Typography fontSize="18px" fontWeight="bold">적용 URL 목록 : 보안 정책이 적용되는 URL을 나타냅니다.</Typography>
        <Button sx={{
            color: colorConfigs.button.blue,
            backgroundColor: colorConfigs.button.white,
            border: 1,
            borderColor: colorConfigs.button.blue,
            borderRadius: "40px",
            paddingX: "32px",
            margin: "4px",
          }}>
            차단IP 추가하기
          </Button>
      </Box>
      <br></br>
      <div style={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSizeOptions={[5, 10]}

          onRowClick={handleOpen}
        />
      </div>
      <br></br> */}

        <Box sx={{ display: 'flex', justifyContent: "space-between" }}>
          <Typography fontSize="18px" fontWeight="bold">예외 URL 목록 </Typography>
          <Button sx={{
            color: colorConfigs.button.blue,
            backgroundColor: colorConfigs.button.white,
            border: 1,
            borderColor: colorConfigs.button.blue,
            borderRadius: "40px",
            paddingX: "32px",
            margin: "4px",
          }}
            onClick={openExpCreateModal}>
            차단IP 추가하기
          </Button>
        </Box>

        <Box style={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={exceptionUrlList}
            columns={columns}
            pageSizeOptions={[5, 10]}
            onRowSelectionModelChange={(selectionModel) => handleSelectionModelChange(selectionModel.map(Number))}
            />
        </Box>
      <ExcepUrlCreateModal isOpen={isExpCreateModalOpen} closeModal={closeCreateModal}></ExcepUrlCreateModal>
      <ExcepUrlUpdateModal isOpen={isExpUpdateModalOpen} closeModal={closeUpdateModal} excepUrl={selectedExpItem}></ExcepUrlUpdateModal>
    </Box>
    
  );
}





export default ExceptionUrlPage