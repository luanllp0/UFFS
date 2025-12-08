import React, { useState } from "react";
import { Grid, Typography } from "@mui/material";
import CadastrarCaminhao from "../components/CadastraCaminhoes";
import ListaCaminhoes from "../components/ListaCaminhoes";

function PaginaCaminhoes() {
  const [atualizacao, setAtualizacao] = useState(0);
  const forcarRecarga = () => setAtualizacao((prev) => prev + 1);

  return (
    <>
      <Typography variant="h4" gutterBottom>
        Gestão de Frota
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <CadastrarCaminhao aoSalvar={forcarRecarga} />
        </Grid>
        <Grid item xs={12} md={8}>
          <ListaCaminhoes key={atualizacao} />
        </Grid>
      </Grid>
    </>
  );
}
export default PaginaCaminhoes;
