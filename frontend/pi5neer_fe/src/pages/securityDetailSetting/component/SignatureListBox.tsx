import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import React from 'react'
import { SignatureType } from '../../../models/SignatureType'
import colorConfigs from '../../../config/colorConfigs'

type Props = {
    sigList: SignatureType[]
}

interface Column {
    label: "위험도" | "내용";
    minWidth?: number;
}

const columns: readonly Column[] = [
    { label: "위험도", minWidth: 80 },
    { label: "내용", minWidth: 160 },
]

const SignatureListBox = (props: Props) => {

    function warningToColor(warning : Number) {
        switch(warning) {
            case 1 : return colorConfigs.warning.low;
            case 2 : return colorConfigs.warning.medium;
            case 3 : return colorConfigs.warning.high;
        }
    }

    function warningToStr(warning : Number) {
        switch(warning) {
            case 1 : return "낮음";
            case 2 : return "보통";
            case 3 : return "높음";
        }
    }

    return (
        <Paper sx={{ width: "100%", overflow: "hidden", marginTop: "20px", }}>
            <TableContainer sx={{ maxHeight: "440px", }}>
                <Table stickyHeader arial-label="sticky table">
                    <TableHead>
                        <TableRow>
                            {
                                columns.map((column) => (
                                    <TableCell key={column.label} align='center' sx={{
                                      minWidth: column.minWidth
                                    }}>
                                      {column.label}
                                    </TableCell>
                                  ))
                            }
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {props.sigList.map((row) => (
                            <TableRow hover key={row.id.toString()}>
                                <TableCell align="center" sx={{
                                    color: warningToColor(row.warning),
                                    fontWeight: "bold"
                                }}>{warningToStr(row.warning)}</TableCell>
                                <TableCell sx={{ paddingX: "60px", fontSize: "16px", fontWeight: "bold" }} align="left">{row.title}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Paper>
    )
}

export default SignatureListBox