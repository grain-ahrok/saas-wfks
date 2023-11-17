import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import colorConfigs from '../../config/colorConfigs'
import ActiveStatusBox from './component/ActiveStatusBox'

type Props = {
  name: string,
}

interface Column {
  label : "위험도" | "내용";
  minWidth? : number;
}

const columns: readonly Column[] = [
  {label : "위험도", minWidth: 80},
  {label : "내용", minWidth: 160},
]

interface Data {
  id : number;
  warning: string;
  title: string;
  color?: string;
}

function createData (
  id : number, 
  warningLevel : number,
  title : string
) : Data{
  let warning = "";
  let color = "";
  switch(warningLevel) {
    case 1 : warning = "낮음"; color = colorConfigs.warning.low; break;
    case 2 : warning = "보통"; color = colorConfigs.warning.medium; break;
    default : warning = "높음"; color = colorConfigs.warning.high;
  }
  return {id, warning, title, color}
}

const rows = [
  createData(1, 3, 'alter를 이용한 SQL Injection 공격'),
  createData(1, 3, 'SQL Injection을 이용하여 CMD 쉘을 직접 제어 하기 위한 공격문1'),
  createData(1, 3, 'delete from을 이용한 SQL Injection 공격'),
  createData(1, 2, 'SQL Injection을 사용하여 웹 쉘을 생성하려는 방법'),
  createData(1, 1, 'RANDOMBLOB 함수를 이용한 Time-based Blind Injection'),
  createData(1, 3, 'alter를 이용한 SQL Injection 공격'),
  createData(1, 3, 'SQL Injection을 이용하여 CMD 쉘을 직접 제어 하기 위한 공격문1'),
  createData(1, 3, 'delete from을 이용한 SQL Injection 공격'),
  createData(1, 2, 'SQL Injection을 사용하여 웹 쉘을 생성하려는 방법'),
  createData(1, 1, 'RANDOMBLOB 함수를 이용한 Time-based Blind Injection'),
  createData(1, 3, 'alter를 이용한 SQL Injection 공격'),
  createData(1, 3, 'SQL Injection을 이용하여 CMD 쉘을 직접 제어 하기 위한 공격문1'),
  createData(1, 3, 'delete from을 이용한 SQL Injection 공격'),
  createData(1, 2, 'SQL Injection을 사용하여 웹 쉘을 생성하려는 방법'),
  createData(1, 1, 'RANDOMBLOB 함수를 이용한 Time-based Blind Injection'),
];


const SqlInjectionPage = (props: Props) => {


  return (
    <Box>
      <Box>
        <ActiveStatusBox name={props.name}></ActiveStatusBox>
      </Box>  
      <Paper sx={{width : "100%", overflow: "hidden", marginTop : "20px", }}>
        <TableContainer  sx={{maxHeight : "440px",  }}>
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
              {rows.map((row) => (
                <TableRow hover key={row.id}>
                  <TableCell align="center" sx={{
                    color : row.color,
                    fontWeight : "bold"
                  }}>{row.warning}</TableCell>
                  <TableCell sx={{paddingX : "60px", fontSize : "16px", fontWeight : "bold"}} align="left">{row.title}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  )
}

export default SqlInjectionPage