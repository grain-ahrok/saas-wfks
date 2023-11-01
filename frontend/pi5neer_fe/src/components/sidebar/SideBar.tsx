/* eslint-disable react/jsx-no-undef */
import { Avatar, Box, Drawer, List, Stack, Toolbar, Typography } from "@mui/material";
import sizeConfigs from "../../config/sizeConfigs";
import colorConfigs from "../../config/colorConfigs";
import appRoutes from "../../routes/appRoutes";
import SidebarItem from "./SidebarItem";
import SidebarItemCollapse from "./SidebarItemCollapse";

const SideBar = () => {
     return (
        <Drawer 
            variant="permanent"
            sx = {{
               width: sizeConfigs.sidebar.width,
               flexShrink: 0,
               "& .MuiDrawer-paper" : {
                  width : sizeConfigs.sidebar.width,
                  boxSizing : "border-box",
                  borderRight : "0px",
                  backgroundColor : colorConfigs.sidebar.bg,
                  color : colorConfigs.sidebar.color
               }
            }}>
            <List disablePadding >
               <Toolbar sx={{marginBottom : "20px", marginTop : "12px"}}>
                  <Stack 
                     sx={{width: "100px"}}
                     direction="row"
                     justifyContent="center">
                     <Avatar src="%PUBLIC_URL%/img/test.png"/>
                     <Box sx={{marginLeft : "12px"}}>
                        <Typography variant='h6'>
                           Pi5neer
                        </Typography>
                     </Box>
                  </Stack>
               </Toolbar>
               {appRoutes.map((route, index) => (
                  route.sidebarProps ? (
                     route.child ? (
                        <SidebarItemCollapse item={route} key={index}/>
                     ) : (
                        <SidebarItem item={route} key={index}/>
                     )
                  ) : null
               ))}
            </List>
         </Drawer>
     )
}

export default SideBar; 