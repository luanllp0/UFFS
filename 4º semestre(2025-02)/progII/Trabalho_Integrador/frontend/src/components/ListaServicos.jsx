import React, { useState, useEffect, useContext } from "react";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Container,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  InputAdornment,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import SearchIcon from "@mui/icons-material/Search";

function ListaServicos() {
  const { user } = useContext(AuthContext);
  const [servicos, setServicos] = useState([]);
  const [busca, setBusca] = useState("");
  const [ordem, setOrdem] = useState("status");

  const [openModal, setOpenModal] = useState(false);
  const [servicoEditando, setServicoEditando] = useState(null);
  const [editDescricao, setEditDescricao] = useState("");
  const [editValor, setEditValor] = useState("");

  const isAdmin =
    user?.tipo === "Colaborador Interno" || user?.tipo === "admin";

  useEffect(() => {
    carregarServicos();
  }, []);

  function carregarServicos() {
    api
      .get("/servicos")
      .then((response) => setServicos(response.data))
      .catch((error) => console.error(error));
  }

  const formataData = (dataISO) => {
    if (!dataISO) return "-";
    return new Date(dataISO).toLocaleDateString("pt-BR");
  };

  const formataDinheiro = (valor) => {
    return parseFloat(valor).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  };

  const servicosProcessados = servicos
    .filter((servico) => {
      const termo = busca.toLowerCase();
      return (
        servico.nome_cliente?.toLowerCase().includes(termo) ||
        servico.nome_tecnico?.toLowerCase().includes(termo) ||
        servico.descricao?.toLowerCase().includes(termo) ||
        servico.placa?.toLowerCase().includes(termo)
      );
    })
    .sort((a, b) => {
      if (ordem === "status") {
        if (
          a.statusconciliacao === "Pendente" &&
          b.statusconciliacao !== "Pendente"
        )
          return -1;
        if (
          a.statusconciliacao !== "Pendente" &&
          b.statusconciliacao === "Pendente"
        )
          return 1;
        return new Date(b.data) - new Date(a.data);
      }
      if (ordem === "data") {
        return new Date(b.data) - new Date(a.data);
      }
      if (ordem === "cliente") {
        return a.nome_cliente.localeCompare(b.nome_cliente);
      }
      if (ordem === "valor") {
        return parseFloat(b.valor) - parseFloat(a.valor);
      }
      return 0;
    });

  async function handleConfirmar(servico) {
    if (!confirm("Deseja confirmar e conciliar este serviço?")) return;

    try {
      await api.put(`/servicos/${servico.idservico}`, {
        descricao: servico.descricao,
        valor: servico.valor,
        statusConciliacao: "Confirmado",
        idColaborador: user.id,
      });
      alert("Serviço confirmado!");
      carregarServicos();
    } catch (error) {
      console.error(error);
      alert("Erro ao confirmar.");
    }
  }

  async function handleExcluir(id) {
    if (!confirm("Tem certeza que deseja excluir este lançamento?")) return;

    try {
      await api.delete(`/servicos/${id}`);
      setServicos(servicos.filter((s) => s.idservico !== id));
    } catch (error) {
      alert("Erro ao excluir serviço.");
    }
  }

  function abrirModalEdicao(servico) {
    setServicoEditando(servico);
    setEditDescricao(servico.descricao);
    setEditValor(servico.valor);
    setOpenModal(true);
  }

  async function salvarEdicao() {
    try {
      await api.put(`/servicos/${servicoEditando.idservico}`, {
        descricao: editDescricao,
        valor: editValor,
        statusConciliacao: servicoEditando.statusconciliacao,
        idColaborador: user.id,
      });
      setOpenModal(false);
      carregarServicos();
    } catch (error) {
      alert("Erro ao salvar edição.");
    }
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
          gap: 2,
        }}
      >
        <Typography variant="h5" sx={{ fontWeight: "bold" }}>
          Histórico de Serviços
        </Typography>

        <Box sx={{ display: "flex", gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 180, bgcolor: "white" }}>
            <InputLabel>Ordenar por</InputLabel>
            <Select
              value={ordem}
              label="Ordenar por"
              onChange={(e) => setOrdem(e.target.value)}
            >
              <MenuItem value="status">Status (Pendentes)</MenuItem>
              <MenuItem value="data">Data (Recente)</MenuItem>
              <MenuItem value="cliente">Cliente (A-Z)</MenuItem>
              <MenuItem value="valor">Maior Valor</MenuItem>
            </Select>
          </FormControl>

          <TextField
            placeholder="Buscar..."
            variant="outlined"
            size="small"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            sx={{ width: 250, bgcolor: "white" }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: "#fff3e0" }}>
              <TableCell>
                <b>Data</b>
              </TableCell>
              <TableCell>
                <b>Técnico</b>
              </TableCell>
              <TableCell>
                <b>Cliente</b>
              </TableCell>
              <TableCell>
                <b>Caminhão</b>
              </TableCell>
              <TableCell>
                <b>Descrição</b>
              </TableCell>
              <TableCell>
                <b>Valor</b>
              </TableCell>
              <TableCell align="center">
                <b>Status</b>
              </TableCell>
              {isAdmin && (
                <TableCell align="center">
                  <b>Ações</b>
                </TableCell>
              )}
            </TableRow>
          </TableHead>
          <TableBody>
            {servicosProcessados.map((servico) => (
              <TableRow key={servico.idservico} hover>
                <TableCell>{formataData(servico.data)}</TableCell>
                <TableCell>{servico.nome_tecnico}</TableCell>
                <TableCell>{servico.nome_cliente}</TableCell>
                <TableCell>{servico.placa}</TableCell>
                <TableCell>{servico.descricao}</TableCell>
                <TableCell sx={{ color: "green", fontWeight: "bold" }}>
                  {formataDinheiro(servico.valor)}
                </TableCell>
                <TableCell align="center">
                  <Chip
                    label={servico.statusconciliacao || "Pendente"}
                    color={
                      servico.statusconciliacao === "Confirmado"
                        ? "success"
                        : "warning"
                    }
                    size="small"
                  />
                </TableCell>
                {isAdmin && (
                  <TableCell align="center">
                    {servico.statusconciliacao !== "Confirmado" && (
                      <IconButton
                        color="success"
                        onClick={() => handleConfirmar(servico)}
                        title="Confirmar"
                      >
                        <CheckCircleIcon />
                      </IconButton>
                    )}
                    <IconButton
                      color="primary"
                      onClick={() => abrirModalEdicao(servico)}
                      title="Editar"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleExcluir(servico.idservico)}
                      title="Excluir"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                )}
              </TableRow>
            ))}
            {servicosProcessados.length === 0 && (
              <TableRow>
                <TableCell colSpan={8} align="center" sx={{ py: 3 }}>
                  Nenhum serviço encontrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openModal} onClose={() => setOpenModal(false)}>
        <DialogTitle>Editar Serviço</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Descrição"
            fullWidth
            multiline
            rows={3}
            value={editDescricao}
            onChange={(e) => setEditDescricao(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Valor (R$)"
            type="number"
            fullWidth
            value={editValor}
            onChange={(e) => setEditValor(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenModal(false)}>Cancelar</Button>
          <Button onClick={salvarEdicao} variant="contained" color="primary">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default ListaServicos;
