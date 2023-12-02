// UserManagementPage.tsx
import React, { useState, useEffect } from 'react';
import { Box, Button, CircularProgress, Grid, Typography } from '@mui/material';
import { IoIosRefresh } from 'react-icons/io';
import UserManage from './component/UserManage';
import UserApplicationLogs from './component/UserApplicationLogs';
import UserApplications from './component/UserApplications';
import { authHeaders } from '../../utils/headers';

export type AttackType = {
  name?: string;
  count?: number;
  value?: number;
  interval?: string;
};

const UserManagementPage = () => {
  const [users, setUsers] = useState([]);
  const [userApps, setUserApps] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [selectedAppId, setSelectedAppId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [attackByTimeList, setAttackByTimeList] = useState<AttackType[]>([]);
  const [attackByNameList, setAttackByNameList] = useState<AttackType[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('/kui/api/v1/Pi5neer/management/users', {
        headers: authHeaders,
      });
      const data = await response.json();
      setUsers(data.users);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
      setLoading(false);
    }
  };

  const fetchUserApps = async (userId: number) => {
    try {
      setLoading(true);
      const response = await fetch(`/kui/api/v1/Pi5neer/management/${userId}/user_app`, {
        headers: authHeaders,
      });
      const data = await response.json();
      setUserApps(data.domain_list);
      setSelectedUserId(userId);
      setSelectedAppId(null);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching user apps:', error);
      setLoading(false);
    }
  };

  const handleRefreshLogs = async () => {
    try {
      if (selectedUserId && selectedAppId) {
        setLoading(true);
        const response = await fetch(`management/${selectedAppId}/user_app_log`, {
          headers: authHeaders,
        });
        const data = await response.json();
        setAttackByTimeList(data['detect_attack']);
        setAttackByNameList(
          Object.entries(data['attack_name']).map(([name, value]) => ({
            name,
            value: value as number,
          }))
        );

        setLoading(false);
      } else {
        console.error('Selected user or application is null.');
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
      setLoading(false);
    }
  };

  return (
    <Box>
      <UserManage
        users={users}
        loading={loading}
        fetchUserApps={fetchUserApps}
        selectedUserId={selectedUserId}
        setSelectedAppId={setSelectedAppId}
      />

      {selectedUserId && (
        <Box mt={4}>
          <Typography variant="h5">User Applications</Typography>
          <UserApplications
            userApps={userApps}
            loading={loading}
            selectedUserId={selectedUserId}
            setSelectedAppId={setSelectedAppId}
          />
        </Box>
      )}

      {selectedUserId && selectedAppId && (
        <Box mt={4}>
          <Typography variant="h5">User Application Logs</Typography>
          <UserApplicationLogs time_data={attackByTimeList} name_data={attackByNameList} loading={loading} />
        </Box>
      )}

      <Box mt={4}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<IoIosRefresh />}
          onClick={handleRefreshLogs}
          disabled={loading}
        >
          Refresh Logs
        </Button>
      </Box>
    </Box>
  );
};

export default UserManagementPage;
