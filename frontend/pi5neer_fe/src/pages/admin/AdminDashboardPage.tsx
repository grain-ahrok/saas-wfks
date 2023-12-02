import { Box, Typography, styled } from '@mui/material'
import React, { useEffect, useState } from 'react'
import { PieChart } from '@mui/x-charts/PieChart';
import styleConfigs from '../../config/styleConfigs';
import { useDrawingArea } from '@mui/x-charts';
import { authHeaders } from '../../utils/headers';
import { url } from 'inspector';
import TrafficCtnBox from '../dashboard/component/TrafficCtnBox';
import { AttackType } from '../dashboard/component/AttackCntByNameBox';
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

  const [cpuUsage, setCpuUsage] = useState(0);
  const [cpuPercent, setCpuPercent] = useState('0%')

  const [memoryPercent, setMemoryPercent] = useState('0%')
  const [memoryUsage, setMemoryUsage] = useState<number>(0.0);
  const [memoryFree, setMemoryFree] = useState(100.0);


  const [trafficList, setTrafficList] = useState<AttackType[]>([]);


  useEffect(() => {
    fetch('/kui/api/v1/Pi5neer/dashboard/resource', {
      headers: authHeaders,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data['header']['resultMessage'] === 'ok') {
          const percent = data['result']['cpu_usage']
          setCpuPercent(percent)
          var number = parseFloat(percent.split('%')[0]);
          setCpuUsage(number)

          data = data['result']
          setMemoryPercent(data['management_memory_usage'])
          number = parseFloat(data['management_memory_used'].split(' MB')[0])
          setMemoryUsage(number)
          number = parseFloat(data['management_memory_free'].split(' MB')[0])
          setMemoryFree(number)
        }
      })
      .catch((error) => {
        if (error) {
          alert("문제가 발생했습니다. 다시 시도해 주세요")
        }
      });


    fetch('/kui/api/v1/Pi5neer/dashboard/traffic', {headers: authHeaders})
      .then((response) => response.json())
      .then((data) => {
        if (data['header']['resultMessage'] === 'ok') {
          setTrafficList(data['result']['total']['traffic']);
        }
      })
      .catch((error) => {
        if (error.response === 500) {
          alert("문제가 발생했습니다. 다시 시도해 주세요~~~~")
        }
      })
  }, []);



  const data1 = [
    { label: '사용량', value: cpuUsage, color: "#3f51b5" },
    { label: '남은 사용량', value: 100 - cpuUsage, color: "#F1EFFB" },
  ];


  const data2 = [
    { label: '사용량', value: memoryUsage, color: "#3f51b5" },
    { label: '남은 사용량', value: memoryFree, color: "#F1EFFB" },
  ];

  return (
    <Box>
      <Box display="flex">
        <Box sx={{
          boxShadow: styleConfigs.boxShadow,
          padding: "20px",
          borderRadius: "24px",
          margin: "12px",
          height: "220px"
        }}>
          <Typography variant='h6'>CPU 사용량</Typography>
          <PieChart
            series={[{
              startAngle: -90,
              endAngle: 90,
              innerRadius: 60,
              outerRadius: 80,
              data: data1
            },
            ]}
            margin={{ right: 5 }}
            width={300}
            height={300}
            slotProps={{
              legend: { hidden: true },
            }}>
            <PieCenterLabel> {cpuPercent} </PieCenterLabel>
          </PieChart>
        </Box>

        <Box sx={{
          boxShadow: styleConfigs.boxShadow,
          padding: "20px",
          borderRadius: "24px",
          margin: "12px",
          height: "220px"
        }}>
          <Typography variant='h6'>Memory 사용량</Typography>
          <PieChart
            series={[
              {
                startAngle: -90,
                endAngle: 90,
                innerRadius: 60,
                outerRadius: 80,
                data: data2,
              },
            ]}
            margin={{ right: 5 }}
            width={300}
            height={300}
            slotProps={{
              legend: { hidden: true },
            }}>
            <PieCenterLabel> {memoryPercent} </PieCenterLabel>
          </PieChart>
        </Box>
      </Box>
      <TrafficCtnBox data={trafficList} />
    </Box>
  )
}



export default AdminDashBoardPage