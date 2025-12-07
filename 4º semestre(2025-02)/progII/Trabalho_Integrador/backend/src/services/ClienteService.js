const pool = require('../db/db');

const ClienteService = {
    async listar() {
        const resultado = await pool.query('SELECT * FROM Cliente ORDER BY nome');
        return resultado.rows;
    },

    async criar(dados) {
        const { nome, telefone, email } = dados;
        const query = 'INSERT INTO Cliente (nome, telefone, email) VALUES ($1, $2, $3) RETURNING *';
        const valores = [nome, telefone, email];
        const resultado = await pool.query(query, valores);
        return resultado.rows[0];
    },

    async deletar(id) {
        const query = 'DELETE FROM Cliente WHERE idcliente = $1';
        await pool.query(query, [id]);
    }
};

module.exports = ClienteService;