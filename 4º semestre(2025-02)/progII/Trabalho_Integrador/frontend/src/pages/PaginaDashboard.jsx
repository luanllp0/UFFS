import React, { useState, useEffect } from "react";
import api from "../services/api";
import { Grid, Paper, Typography, Box } from "@mui/material";
import PeopleIcon from "@mui/icons-material/People";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import AssignmentIcon from "@mui/icons-material/Assignment";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";

function PaginaDashboard() {
  const [dados, setDados] = useState({
    totalClientes: 0,
    totalCaminhoes: 0,
    servicosPendentes: 0,
    totalFaturado: 0,
  });

  useEffect(() => {
    api
      .get("/dashboard")
      .then((res) => setDados(res.data))
      .catch((err) => console.error(err));
  }, []);

  const CardResumo = ({ titulo, valor, icone, cor, isMoney }) => (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        bgcolor: cor,
        color: "white",
      }}
    >
      <Box>
        <Typography variant="h6">{titulo}</Typography>
        <Typography variant="h4" fontWeight="bold">
          {isMoney
            ? parseFloat(valor).toLocaleString("pt-BR", {
                style: "currency",
                currency: "BRL",
              })
            : valor}
        </Typography>
      </Box>
      {icone}
    </Paper>
  );

  return (
    <Box>
      <Typography
        variant="h4"
        gutterBottom
        sx={{ mb: 4, fontWeight: "bold", color: "#1976d2" }}
      >
        Visão Geral
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={3}>
          <CardResumo
            titulo="Total Clientes"
            valor={dados.totalClientes}
            icone={<PeopleIcon sx={{ fontSize: 50, opacity: 0.8 }} />}
            cor="#1976d2"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <CardResumo
            titulo="Frota Caminhões"
            valor={dados.totalCaminhoes}
            icone={<LocalShippingIcon sx={{ fontSize: 50, opacity: 0.8 }} />}
            cor="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <CardResumo
            titulo="Serviços Pendentes"
            valor={dados.servicosPendentes}
            icone={<AssignmentIcon sx={{ fontSize: 50, opacity: 0.8 }} />}
            cor="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <CardResumo
            titulo="Faturado (Confirmado)"
            valor={dados.totalFaturado || 0}
            icone={<AttachMoneyIcon sx={{ fontSize: 50, opacity: 0.8 }} />}
            cor="#9c27b0"
            isMoney={true}
          />
        </Grid>
      </Grid>

      <Paper sx={{ mt: 5, p: 4, textAlign: "center", bgcolor: "#f5f5f5" }}>
        <Typography variant="h6" color="textSecondary">
          Bem-vindo ao Sistema Rodofrio. Use o menu lateral para navegar.
        </Typography>
      </Paper>
    </Box>
  );
}

export default PaginaDashboard;
