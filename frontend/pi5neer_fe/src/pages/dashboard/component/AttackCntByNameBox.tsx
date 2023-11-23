import { Box, Typography } from '@mui/material'
import React from 'react'
import styleConfigs from '../../../config/styleConfigs'
import { Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis } from 'recharts'
import colorConfigs from '../../../config/colorConfigs'
import { AttackType } from '../../../models/AttackType'


type Props = {
    data: AttackType[]
}

const AttackCntByNameBox = (props: Props) => {

    // TODO : 그래프 값에 따라서 색깔이 달라지도록
    const getChartColor = (value: number): string => {
        // 여기에서 값에 따라 원하는 색상을 동적으로 계산
        if (value >= 75) {
            return colorConfigs.chart.high;
        } else if (value >= 50) {
            return colorConfigs.chart.medium;
        } else {
            return colorConfigs.chart.low;
        }
    };

    return (
        <Box sx={{
            flex: "1",
            borderRadius: "20px",
            padding: "20px",
            margin: "20px",
            boxShadow: styleConfigs.boxShadow
        }}>
            <Typography sx={{ fontWeight: "700" }}>공격 이름</Typography>
            <BarChart
                width={500}
                height={300}
                data={props.data}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                layout='vertical'>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill={colorConfigs.chart.medium} label="공격 시도 횟수" />
            </BarChart>
        </Box>
    )
}

export default AttackCntByNameBox