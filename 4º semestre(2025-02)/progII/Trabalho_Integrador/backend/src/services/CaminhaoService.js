const pool = require('../db/db');

const CaminhaoService = {
    async listar() {
        const resultado = await pool.query('SELECT * FROM Caminhao ORDER BY modeloDescricao');
        return resultado.rows;
    },

    async criar(dados) {
        const { placa, modeloDescricao, idCliente } = dados;
        const query = 'INSERT INTO Caminhao (placa, modeloDescricao, idCliente) VALUES ($1, $2, $3) RETURNING *';
        const valores = [placa, modeloDescricao, idCliente];
        const resultado = await pool.query(query, valores);
        return resultado.rows[0];
    }
};

module.exports = CaminhaoService;