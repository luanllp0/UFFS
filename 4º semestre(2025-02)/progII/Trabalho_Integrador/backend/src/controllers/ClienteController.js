const ClienteService = require('../services/ClienteService');

const ClienteController = {
    async listar(req, res) {
        try {
            const clientes = await ClienteService.listar(); 
            res.json(clientes);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao buscar clientes' });
        }
    },

    async criar(req, res) {
        try {
            const novoCliente = await ClienteService.criar(req.body); 
            res.status(201).json(novoCliente);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao criar cliente' });
        }
    }
};

module.exports = ClienteController;