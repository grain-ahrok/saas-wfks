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