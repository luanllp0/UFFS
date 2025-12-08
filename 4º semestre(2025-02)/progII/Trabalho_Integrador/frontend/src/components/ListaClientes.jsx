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

function ListaClientes() {
  const [clientes, setClientes] = useState([]);

  useEffect(() => {
    api
      .get("/clientes")
      .then((response) => {
        console.log(response.data);
        setClientes(response.data);
      })
      .catch((error) => {
        console.error("Erro:", error);
        alert("Erro ao buscar clientes. O Back-end está rodando?");
      });
  }, []);

  async function handleDelete(id) {
    if (!confirm("Tem certeza que deseja excluir este cliente?")) return;

    try {
      await api.delete(`/clientes/${id}`);

      setClientes(clientes.filter((cliente) => cliente.idcliente !== id));
    } catch (error) {
      alert(
        "Erro ao excluir. Verifique se o cliente possui caminhões vinculados!",
      );
    }
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h2" gutterBottom>
        Clientes Rodofrio
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#f5f5f5" }}>
              <TableCell>
                <b>ID</b>
              </TableCell>
              <TableCell>
                <b>Nome</b>
              </TableCell>
              <TableCell>
                <b>Telefone</b>
              </TableCell>
              <TableCell>
                <b>Email</b>
              </TableCell>
              <TableCell align="center">
                <b>Ações</b>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {clientes.map((cliente) => (
              <TableRow key={cliente.idcliente}>
                <TableCell>{cliente.idcliente}</TableCell>
                <TableCell>{cliente.nome}</TableCell>
                <TableCell>{cliente.telefone}</TableCell>
                <TableCell>{cliente.email}</TableCell>
                <TableCell align="center">
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(cliente.idcliente)}
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

export default ListaClientes;
