import { Box, Typography, styled } from '@mui/material'
import React, { useState } from 'react'
import { PieChart } from '@mui/x-charts/PieChart';
import styleConfigs from '../../config/styleConfigs';
import { useDrawingArea } from '@mui/x-charts';
type Props = {}

const StyledText = styled('text')(({ theme }) => ({
  fill: theme.palette.text.primary,
  textAnchor: 'middle',
  dominantBaseline: 'central',
  fontSize: 20,
}));

function PieCenterLabel({ children }: { children: React.ReactNode }) {
  const { width, height, left, top } = useDrawingArea();
  return (
    <StyledText x={left + width / 2} y={top + height * 4.5 / 10}>
      {children}
    </StyledText>
  );
}

const AdminDashBoardPage = (props: Props) => {

  
  const [cpuUsage, setCpuUsage] = useState(400);
  const cpuTotal = 1400;
  const cpuPercent = (cpuUsage / cpuTotal * 100).toFixed(2);

  const [memoryUsage, setMemoryUsage] = useState(500);
  const memoryTotal = 1400;
  const MemoryPercent = (memoryUsage / memoryTotal * 100).toFixed(2);;



  const data = [
    { label: '사용량', value: cpuUsage, color : "#3f51b5" },
    { label: '남은 사용량', value: cpuTotal- cpuUsage, color : "#e91e63" },
  ];

  return (
    <Box display="flex">
      <Box sx={{
        boxShadow : styleConfigs.boxShadow,
        padding : "20px",
        borderRadius : "24px", 
        margin : "12px",
        height : "220px"
      }}>
        <Typography variant='h6'>CPU 사용량</Typography>
        <PieChart
          series={[{
              startAngle: -90,
              endAngle: 90,
              innerRadius: 60,
              outerRadius: 80,
              data},
          ]}
          margin={{ right: 5 }}
          width={300}
          height={300}
          slotProps={{
            legend: { hidden: true },
          }}>
           <PieCenterLabel> {cpuPercent}% </PieCenterLabel>
        </PieChart>
      </Box>

      <Box sx={{
        boxShadow : styleConfigs.boxShadow,
        padding : "20px",
        borderRadius : "24px", 
        margin : "12px",
        height : "220px"
      }}>
      <Typography variant='h6'>Memory 사용량</Typography>
        <PieChart
          series={[
            {
              startAngle: -90,
              endAngle: 90,
              innerRadius: 60,
              outerRadius: 80,
              data,
            },
          ]}
          margin={{ right: 5 }}
          width={300}
          height={300}
          slotProps={{
            legend: { hidden: true },
          }}>
          <PieCenterLabel> {cpuPercent}% </PieCenterLabel>
        </PieChart>
      </Box>
    </Box>
  )
}



export default AdminDashBoardPage