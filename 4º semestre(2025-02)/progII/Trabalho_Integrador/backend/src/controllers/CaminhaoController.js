const CaminhaoService = require('../services/CaminhaoService');

const CaminhaoController = {
    async listar(req, res) {
        try {
            const caminhoes = await CaminhaoService.listar();
            res.json(caminhoes);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao buscar caminhões' });
        }
    },

    async criar(req, res) {
        try {
            const novoCaminhao = await CaminhaoService.criar(req.body);
            res.status(201).json(novoCaminhao);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao cadastrar caminhão' });
        }
    }
};

module.exports = CaminhaoController;