import { Box, Typography } from '@mui/material'
import colorConfigs from '../../config/colorConfigs'
import ActiveStatusBox from './component/ActiveStatusBox'

type Props = {
  name : string,
}

const SqlInjectionPage = (props: Props) => {
  

  return (
    <Box>
      <ActiveStatusBox name={props.name}></ActiveStatusBox>
    </Box>
  )
}

export default SqlInjectionPage