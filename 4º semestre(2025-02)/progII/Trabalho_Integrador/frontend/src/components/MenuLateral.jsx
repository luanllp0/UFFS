import React, { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Divider,
  Box,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import BuildIcon from "@mui/icons-material/Build";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";

const drawerWidth = 240;

function MenuLateral({ children }) {
  const { logout, user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const todosMenus = [
    { text: "Dashboard", icon: <DashboardIcon />, path: "/", publico: true },
    { text: "Serviços", icon: <BuildIcon />, path: "/servicos", publico: true },
    {
      text: "Clientes",
      icon: <PeopleIcon />,
      path: "/clientes",
      publico: false,
    },
    {
      text: "Caminhões",
      icon: <LocalShippingIcon />,
      path: "/caminhoes",
      publico: false,
    },
  ];

  const menusFiltrados = todosMenus.filter((item) => {
    if (item.publico) return true;
    if (user?.tipo === "Colaborador Interno" || user?.tipo === "admin")
      return true;
    return false;
  });

  return (
    <Box sx={{ display: "flex" }}>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto" }}>
          <List>
            {menusFiltrados.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton
                  selected={location.pathname === item.path}
                  onClick={() => navigate(item.path)}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          <Divider />
          <List>
            <ListItem disablePadding>
              <ListItemButton onClick={logout}>
                <ListItemIcon>
                  <ExitToAppIcon color="error" />
                </ListItemIcon>
                <ListItemText primary="Sair" sx={{ color: "error.main" }} />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}

export default MenuLateral;
