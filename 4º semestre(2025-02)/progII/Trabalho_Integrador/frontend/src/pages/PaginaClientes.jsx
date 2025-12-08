import React, { useState } from "react";
import { Grid, Typography } from "@mui/material";
import CadastrarCliente from "../components/CadastraClientes";
import ListaClientes from "../components/ListaClientes";

function PaginaClientes() {
  const [atualizacao, setAtualizacao] = useState(0);

  const forcarRecarga = () => {
    setAtualizacao((prev) => prev + 1);
  };

  return (
    <>
      <Typography variant="h4" gutterBottom>
        Gestão de Clientes
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <CadastrarCliente aoSalvar={forcarRecarga} />
        </Grid>
        <Grid item xs={12} md={8}>
          <ListaClientes key={atualizacao} />
        </Grid>
      </Grid>
    </>
  );
}
export default PaginaClientes;
