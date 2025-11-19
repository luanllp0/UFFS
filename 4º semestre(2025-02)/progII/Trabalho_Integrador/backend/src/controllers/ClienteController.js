const pool = require('../db/db');

const ClienteController = {
    async listar(req, res) {
        try {
            const resultado = await pool.query('SELECT * FROM Cliente ORDER BY nome');
            res.json(resultado.rows);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao buscar clientes' });
        }
    },

    async criar(req, res) {
        const { nome, telefone, email } = req.body;
        try {
            const query = 'INSERT INTO Cliente (nome, telefone, email) VALUES ($1, $2, $3) RETURNING *';
            const valores = [nome, telefone, email];
            
            const resultado = await pool.query(query, valores);
            res.status(201).json(resultado.rows[0]);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Erro ao criar cliente' });
        }
    }
};

module.exports = ClienteController;