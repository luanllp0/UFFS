import React, { useState, useEffect } from "react";
import api from "../services/api";
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

function CadastrarCaminhao({ aoSalvar }) {
  const [placa, setPlaca] = useState("");
  const [modeloDescricao, setModeloDescricao] = useState("");
  const [idCliente, setIdCliente] = useState("");

  const [listaClientes, setListaClientes] = useState([]);

  useEffect(() => {
    api
      .get("/clientes")
      .then((response) => setListaClientes(response.data))
      .catch((error) => console.error(error));
  }, []);

  async function acaoBotao(e) {
    e.preventDefault();
    try {
      await api.post("/caminhoes", { placa, modeloDescricao, idCliente });
      alert("Caminhão cadastrado com sucesso!");
      setPlaca("");
      setModeloDescricao("");
      setIdCliente("");

      if (aoSalvar) aoSalvar();
    } catch (error) {
      console.error(error);
      alert("Erro ao cadastrar.");
    }
  }

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Novo Caminhão
      </Typography>
      <Box
        component="form"
        onSubmit={acaoBotao}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          label="Placa"
          variant="outlined"
          value={placa}
          onChange={(e) => setPlaca(e.target.value.toUpperCase())}
          required
        />
        <TextField
          label="Modelo / Descrição"
          variant="outlined"
          value={modeloDescricao}
          onChange={(e) => setModeloDescricao(e.target.value)}
          required
        />
        <FormControl fullWidth required>
          <InputLabel id="select-dono-label">Dono do Caminhão</InputLabel>
          <Select
            labelId="select-dono-label"
            value={idCliente}
            label="Dono do Caminhão"
            onChange={(e) => setIdCliente(e.target.value)}
          >
            {listaClientes.map((cliente) => (
              <MenuItem key={cliente.idcliente} value={cliente.idcliente}>
                {cliente.nome}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button type="submit" variant="contained" size="large">
          Salvar Caminhão
        </Button>
      </Box>
    </Paper>
  );
}

export default CadastrarCaminhao;
