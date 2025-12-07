import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Box, TextField, Button, Typography, Paper, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function CadastrarCaminhao() {
    const [placa, setPlaca] = useState('');
    const [modeloDescricao, setModeloDescricao] = useState('');
    const [idCliente, setIdCliente] = useState('');
    const [listaClientes, setListaClientes] = useState([]);

    useEffect(() => {
        api.get('/clientes')
            .then(response => {
                setListaClientes(response.data); 
            })
            .catch(error => console.error("Erro ao buscar donos:", error));
    }, []);

    async function acaoBotao(e) {
        e.preventDefault();

        try {
            await api.post('/caminhoes', { placa, modeloDescricao, idCliente });
            alert('Caminhao cadastrado com sucesso!');
            setPlaca('');
            setModeloDescricao('');
            setIdCliente('');
        } catch (error) {
            alert('Erro ao cadastrar');
        }
    }

    return (
      <Paper elevation={3} sx={{ p: 4, mt: 4, maxWidth: 500, mx: "auto" }}>
        <Typography variant="h5" gutterBottom>
          Novo Caminhao
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
            onChange={(e) => setPlaca(e.target.value)}
            required
          />

          <TextField
            label="Modelo / Descricao"
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
            Salvar Caminhao
          </Button>
        </Box>
      </Paper>
    );
}

export default CadastrarCaminhao;