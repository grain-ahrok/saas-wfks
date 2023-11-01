import React from 'react'
import { RouteType } from '../../routes/config'
import { ListItemButton, ListItemIcon } from '@mui/material';
import { Link } from 'react-router-dom';
import colorConfigs from '../../config/colorConfigs';
import { RootState } from '../../redux/store';
import { useSelector } from 'react-redux';

type Props = {
    item: RouteType;
}

const SidebarItem = ({ item }: Props) => {
    const {appState} = useSelector((state: RootState) => state.appState)
    return (
        item.sidebarProps && item.path ? (
            <ListItemButton
                component={Link}
                to={item.path}
                sx={{
                    "&: hover": {
                        backgroundColor: colorConfigs.sidebar.hoverBg
                    },
                    backgroundColor : appState === item.state ? colorConfigs.sidebar.activeBg : "unset",
                    paddingY: "12px",
                    paddingX: "24px"
                }}>

                <ListItemIcon sx={{
                    color: colorConfigs.sidebar.color
                }}>
                    {item.sidebarProps.icon && item.sidebarProps.icon}
                </ListItemIcon>
                {item.sidebarProps.displayText}
            </ListItemButton>
        ) : null
    )
}

export default SidebarItem