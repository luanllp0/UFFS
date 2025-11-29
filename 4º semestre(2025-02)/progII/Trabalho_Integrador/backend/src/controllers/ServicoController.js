const ServicoService = require('../services/ServicoService');

const ServicoController = {
    async listar(req, res) {
        try {
            const servicos = await ServicoService.listar();
            res.json(servicos);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao buscar serviços' });
        }
    },

    async criar(req, res) {
        try {
            const novoServico = await ServicoService.criar(req.body);
            res.status(201).json(novoServico);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao lançar serviço' });
        }
    }
};

module.exports = ServicoController;