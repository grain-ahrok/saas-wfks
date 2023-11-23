import { Box, Typography, colors } from '@mui/material'
import React, { useEffect, useState } from 'react'
import styleConfigs from '../../config/styleConfigs'
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts'
import AttackCntByNameBox from './component/AttackCntByNameBox'
import AttackCntByTimeBox from './component/AttackCntByTimeBox'
import { AttackType } from '../../models/AttackType'
import TrafficCtnBox from './component/TrafficCtnBox'

type Props = {}

const DashboardPage = (props: Props) => {

  const app_id = 1;
  const url = `/app/${app_id}/dashboard`;

  const [tarfficList, setTrafficList] = useState<AttackType[]>([{
    "count": 249,
    "interval": "2023-11-18 04:25:15 - 2023-11-18 04:40:15"
  },
  {
    "count": 0,
    "interval": "2023-11-18 04:40:15 - 2023-11-18 04:55:15"
  },
  {
    "count": 0,
    "interval": "2023-11-18 04:55:15 - 2023-11-18 05:10:15"
  },
  {
    "count": 0,
    "interval": "2023-11-18 05:10:15 - 2023-11-18 05:25:15"
  }]);
  const [attackByNameList, setAttackByNameList] = useState<AttackType[]>([{ name: 'URL정규식', value: 61 },
  { name: '다운로드', value: 24 },
  { name: '업로드', value: 124 },
  { name: '웹공격프로그램', value: 40 },
  { name: '웹공격프로그램', value: 40 },
  { name: '웹공격프로그램', value: 40 }]);

  const [attackByTimeList, setAttackByTimeList] = useState<AttackType[]>([
    {
      "count": 249,
      "interval": "2023-11-18 04:25:15 - 2023-11-18 04:40:15"
    },
    {
      "count": 0,
      "interval": "2023-11-18 04:40:15 - 2023-11-18 04:55:15"
    },
    {
      "count": 0,
      "interval": "2023-11-18 04:55:15 - 2023-11-18 05:10:15"
    },
    {
      "count": 0,
      "interval": "2023-11-18 05:10:15 - 2023-11-18 05:25:15"
    }
  ]);

  useEffect(() => {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setTrafficList(data['tarffic']);
        setAttackByTimeList(data['detect_attack']);
        setAttackByNameList(data['attack_name']);
      })
      .catch((error) => {
        console.error('요청 중 오류 발생:', error);
      });
  }, [url]);


  return (
    <Box>
      {/* 트래픽 통계 */}
      <TrafficCtnBox data={tarfficList}></TrafficCtnBox>
      <Box display="flex">
        <AttackCntByTimeBox data={attackByTimeList}></AttackCntByTimeBox>
        <AttackCntByNameBox data={attackByNameList}></AttackCntByNameBox>
      </Box>
    </Box>
  )
}

export default DashboardPage