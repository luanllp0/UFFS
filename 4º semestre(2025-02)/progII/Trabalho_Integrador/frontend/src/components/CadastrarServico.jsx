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
  Grid,
} from "@mui/material";

function CadastrarServico({ aoSalvar }) {
  const [data, setData] = useState("");
  const [hora, setHora] = useState("");
  const [descricao, setDescricao] = useState("");
  const [valor, setValor] = useState("");

  const [idTecnico, setIdTecnico] = useState("");
  const [placaCaminhao, setPlacaCaminhao] = useState("");

  const [listaCaminhoes, setListaCaminhoes] = useState([]);

  useEffect(() => {
    api
      .get("/caminhoes")
      .then((res) => setListaCaminhoes(res.data))
      .catch((err) => console.error(err));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    const valorFormatado = valor.toString().replace(",", ".");

    const dadosPayload = {
      data,
      hora,
      descricao,
      valor: parseFloat(valorFormatado),
      mesFaturamento: data,
      idTecnico: parseInt(idTecnico),
      placaCaminhao,
    };

    try {
      await api.post("/servicos", dadosPayload);
      alert("Sucesso!");
      setDescricao("");
      setValor("");
      setIdTecnico("");
      setPlacaCaminhao("");

      if (aoSalvar) aoSalvar();
    } catch (error) {
      console.error(error);
      alert("Erro!");
    }
  }

  return (
    <Paper elevation={3} sx={{ p: 4, mt: 4, maxWidth: 900, mx: "auto" }}>
      <Typography
        variant="h5"
        gutterBottom
        sx={{ color: "#ed6c02", mb: 3, fontWeight: "bold" }}
      >
        Nova Ordem de Serviço
      </Typography>

      <Box component="form" onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField
              label="Data"
              type="date"
              fullWidth
              required
              InputLabelProps={{ shrink: true }}
              value={data}
              onChange={(e) => setData(e.target.value)}
              sx={{
                "& input::-webkit-calendar-picker-indicator": {
                  cursor: "pointer",
                  filter: "invert(0.5)",
                  fontSize: "1.5rem",
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Hora"
              type="time"
              fullWidth
              required
              InputLabelProps={{ shrink: true }}
              value={hora}
              onChange={(e) => setHora(e.target.value)}
              sx={{
                "& input::-webkit-calendar-picker-indicator": {
                  cursor: "pointer",
                  filter: "invert(0.5)",
                  fontSize: "1.5rem",
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Valor (R$)"
              fullWidth
              required
              placeholder="0.00"
              value={valor}
              onChange={(e) => setValor(e.target.value)}
            />
          </Grid>

          <Grid item xs={12} md={8}>
            <FormControl fullWidth required sx={{ minWidth: 200 }}>
              <InputLabel id="select-cam-label">Caminhão (Placa)</InputLabel>
              <Select
                labelId="select-cam-label"
                value={placaCaminhao}
                label="Caminhão (Placa)"
                onChange={(e) => setPlacaCaminhao(e.target.value)}
              >
                {listaCaminhoes.map((cam) => (
                  <MenuItem key={cam.placa} value={cam.placa}>
                    {cam.placa} - {cam.modelodescricao}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="ID Técnico"
              type="number"
              fullWidth
              required
              placeholder="Ex: 2"
              value={idTecnico}
              onChange={(e) => setIdTecnico(e.target.value)}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              label="Descrição do Serviço"
              multiline
              rows={3}
              fullWidth
              required
              placeholder="Detalhes..."
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="warning"
              fullWidth
              size="large"
            >
              Lançar Serviço
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
}

export default CadastrarServico;
