import React, { ReactNode, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setAppState } from '../../redux/features/appSateSlice'
import appRoutes from '../../routes/appRoutes';
import { Box, Button } from '@mui/material';
import colorConfigs from '../../config/colorConfigs';
import { RootState } from '../../redux/store';
import { Link } from 'react-router-dom';

type Props = {
  state?: string,
  children: ReactNode
};

const DetailPolicyWrapper = (props: Props) => {
  const { appState } = useSelector((state: RootState) => state.appState)
  const dispatch = useDispatch()


  useEffect(() => {
    if (props.state) {
      dispatch(setAppState(props.state));
    }
  }, [dispatch, props]);

  return (
    <Box>
      <Box display="flex" flexWrap="wrap" >
        {
          appRoutes.appPolicyDetailRoutes.map((route, index) => (
            route.path && <Button
              component={Link}
              to={route.path}
              sx={{
                backgroundColor: appState === route.state ? colorConfigs.button.pioBg : colorConfigs.button.white,
                borderColor: colorConfigs.button.pioBg,
                border: "solid",
                borderRadius: "24px",
                minWidth: "180px",
                paddingX: "16px",
                paddingY: "5px",
                margin: "4px",
              }}
            >
              {route.sidebarProps?.displayText}
            </Button>
          ))
        }

      </Box>
      {props.children}
    </Box>
  )
}

export default DetailPolicyWrapper

