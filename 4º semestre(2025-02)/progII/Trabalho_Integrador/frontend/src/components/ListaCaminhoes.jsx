import React, { useState, useEffect } from "react";
import api from "../services/api";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  IconButton,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Container,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";

function ListaCaminhoes() {
  const [caminhoes, setCaminhoes] = useState([]);

  useEffect(() => {
    api
      .get("/caminhoes")
      .then((response) => {
        console.log(response.data);
        setCaminhoes(response.data);
      })
      .catch((error) => {
        console.error("Erro:", error);
        alert("Erro ao buscar caminhoes. O Back-end está rodando?");
      });
  }, []);

  async function handleDelete(id) {
    if (!confirm("Tem certeza que deseja excluir este caminhão?")) return;

    try {
      await api.delete(`/caminhoes/${id}`);

      setCaminhoes(caminhoes.filter((caminhoes) => caminhoes.placa !== id));
    } catch (error) {
      alert(
        "Erro ao excluir. Verifique se há serviços vinculados ao caminhão.",
      );
    }
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h2" gutterBottom>
        Caminhoes Rodofrio
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#f5f5f5" }}>
              <TableCell>
                <b>Placa</b>
              </TableCell>
              <TableCell>
                <b>Modelo</b>
              </TableCell>
              <TableCell>
                <b>ID do cliente</b>
              </TableCell>
              <TableCell align="center">
                <b>Ações</b>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {caminhoes.map((caminhao) => (
              <TableRow key={caminhao.placa}>
                <TableCell>{caminhao.placa}</TableCell>
                <TableCell>{caminhao.modelodescricao}</TableCell>
                <TableCell>{caminhao.idcliente}</TableCell>
                <TableCell align="center">
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(caminhao.placa)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default ListaCaminhoes;
