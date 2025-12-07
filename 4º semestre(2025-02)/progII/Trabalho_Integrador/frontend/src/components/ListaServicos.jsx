import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { 
    Table, TableBody, TableCell, TableContainer, 
    TableHead, TableRow, Paper, Typography, Box, Container, Chip 
} from '@mui/material';

function ListaServicos() {
    const [servicos, setServicos] = useState([]);

    useEffect(() => {
        api.get('/servicos')
            .then(response => {
                console.log("Serviços:", response.data);
                setServicos(response.data);
            })
            .catch(error => console.error("Erro ao buscar serviços:", error));
    }, []);

    const formataData = (dataISO) => {
        if (!dataISO) return '-';
        return new Date(dataISO).toLocaleDateString('pt-BR');
    };

    const formataDinheiro = (valor) => {
        return parseFloat(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Histórico de Serviços
            </Typography>
            
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow sx={{ backgroundColor: '#fff3e0' }}> 
                            <TableCell><b>Data</b></TableCell>
                            <TableCell><b>Técnico</b></TableCell>
                            <TableCell><b>Cliente</b></TableCell>
                            <TableCell><b>Caminhão</b></TableCell>
                            <TableCell><b>Descrição</b></TableCell>
                            <TableCell><b>Valor</b></TableCell>
                            <TableCell><b>Status</b></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {servicos.map((servico) => (
                            <TableRow key={servico.idservico}>
                                <TableCell>{formataData(servico.data)}</TableCell>
                                <TableCell>{servico.nome_tecnico}</TableCell>
                                <TableCell>{servico.nome_cliente}</TableCell>
                                <TableCell>{servico.placa}</TableCell>
                                <TableCell>{servico.descricao}</TableCell>
                                <TableCell style={{ color: 'green', fontWeight: 'bold' }}>
                                    {formataDinheiro(servico.valor)}
                                </TableCell>
                                <TableCell>
                                    <Chip 
                                        label={servico.statusconciliacao || 'Pendente'} 
                                        color={servico.statusconciliacao === 'Pago' ? 'success' : 'warning'} 
                                        size="small"
                                    />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

export default ListaServicos;