import { Box, Drawer, List, Stack, Toolbar, Typography } from "@mui/material";
import sizeConfigs from "../../config/sizeConfigs";
import colorConfigs from "../../config/colorConfigs";
import appRoutes from "../../routes/appRoutes";
import SidebarItem from "./SidebarItem";
import SidebarItemCollapse from "./SidebarItemCollapse";
import AcUnitIcon from '@mui/icons-material/AcUnit';
import styleConfigs from "../../config/styleConfigs";

const SideBar = () => {
     return (
        <Drawer 
            variant="permanent"
            sx = {{
               width: sizeConfigs.sidebar.width,
               flexShrink: 0,
               "& .MuiDrawer-paper" : {
                  width : sizeConfigs.sidebar.width,
                  padding : "12px",
                  boxSizing : "border-box",
                  borderRight : "0px",
                  backgroundColor : colorConfigs.sidebar.bg,
                  color : colorConfigs.sidebar.unselectedColor,
                  borderRadius: "24px",
                  boxShadow: styleConfigs.boxShadow
               }
            }}>
            <List disablePadding>
               <Toolbar sx={{marginBottom : "8px", marginTop : "8px"}}>
                  <Stack 
                     sx={{width: "100px", color: colorConfigs.logo.color}}
                     direction="row"
                     justifyContent="center">
                     <AcUnitIcon/>
                     <Box sx={{marginLeft : "12px"}}>
                        <Typography variant='h5'>
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