// UserApplications.tsx
import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { DataGrid, GridColDef, GridRowParams } from '@mui/x-data-grid';

interface UserApplication {
  id: string; // Add a unique identifier property
  table_id: number;
  domain: string;
}

interface UserApplicationsProps {
  userApps: UserApplication[];
  loading: boolean;
  selectedUserId: number;
  setSelectedAppId: React.Dispatch<React.SetStateAction<number | null>>;
}

const columns: GridColDef[] = [
  { field: 'table_id', headerName: 'Table ID', width: 120 },
  { field: 'domain', headerName: 'Domain', width: 200 },
];

const UserApplications: React.FC<UserApplicationsProps> = ({
  userApps,
  loading,
  selectedUserId,
  setSelectedAppId,
}) => {
  const columns: GridColDef[] = [
    { field: 'table_id', headerName: 'Table ID', width: 120 },
    { field: 'domain', headerName: 'Domain', width: 200 },
  ];

  return (
    <Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box>
          <Typography variant="h6">User Applications for User ID: {selectedUserId}</Typography>
          <DataGrid
            rows={userApps.map((app) => ({ ...app, id: app.table_id.toString() }))}
            columns={columns}
            checkboxSelection
            onRowClick={(params: GridRowParams) => {
              if (params.id != null) {
                setSelectedAppId(Number(params.id));
              }
            }}
          />
        </Box>
      )}
    </Box>
  );
};

export default UserApplications;
