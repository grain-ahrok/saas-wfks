import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import { AttackType } from '../../../models/AttackType'
import { Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis } from 'recharts'
import colorConfigs from '../../../config/colorConfigs'
export type AttackType2 = {
    name?: string;
    count?: number;
    interval?: string;
  };


  interface UserApplicationLogsProps {
    time_data: AttackType[];
    name_data: AttackType2[];
    loading: boolean;
  }
  
  const UserApplicationLogs: React.FC<UserApplicationLogsProps> = ({ time_data, name_data, loading }) => {
  return (
    <Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box>
          <Typography variant="h6">User Application Logs</Typography>
          <BarChart
            width={500}
            height={300}
            data={name_data}
            margin={{ top: 20, right: 30, left: 50, bottom: 5 }} // Adjust left margin to make space for y-axis labels
            layout='vertical'
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" width={100} /> {/* Rotate and adjust width */}
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill={colorConfigs.chart.medium} label="공격 시도 횟수" />
        </BarChart>

        <BarChart
            width={500}
            height={300}
            data={time_data}
            margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="interval"  tick={false} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          
        </Box>
      )}
    </Box>
  );
};

export default UserApplicationLogs;
