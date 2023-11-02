import { AppBar, Toolbar, Typography } from '@mui/material';
import React from 'react';
import sizeConfigs from '../../config/sizeConfigs';
import colorConfigs from '../../config/colorConfigs';

type Props = {};

const TopBar = (props: Props) => {
    return(
        <AppBar position='fixed' sx={{
            width : `calc(100% - ${sizeConfigs.sidebar.width})`,
            ml: sizeConfigs.sidebar.width,
            boxShadow: 'unset',
            backgroundColor : colorConfigs.topbar.bg,
            color : colorConfigs.topbar.color,
        }}>
            <Toolbar>
                <Typography variant='h6'>
                    Hello👋
                </Typography>
            </Toolbar>
        </AppBar>
    )    
};
 
export default TopBar; 