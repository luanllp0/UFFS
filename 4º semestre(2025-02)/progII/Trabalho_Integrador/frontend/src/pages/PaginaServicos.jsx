import React, { useState } from "react";
import { Box, Typography } from "@mui/material";
import CadastrarServico from "../components/CadastrarServico";
import ListaServicos from "../components/ListaServicos";

function PaginaServicos() {
  const [atualizacao, setAtualizacao] = useState(0);
  const forcarRecarga = () => setAtualizacao((prev) => prev + 1);

  return (
    <>
      <Typography variant="h4" gutterBottom>
        Ordens de Serviço
      </Typography>
      <Box sx={{ mt: 4 }}>
        <CadastrarServico aoSalvar={forcarRecarga} />
        <Box sx={{ mt: 6 }}>
          <ListaServicos key={atualizacao} />
        </Box>
      </Box>
    </>
  );
}
export default PaginaServicos;
