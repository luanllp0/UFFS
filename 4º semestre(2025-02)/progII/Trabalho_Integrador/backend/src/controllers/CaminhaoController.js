const pool = require('../db/db');

const CaminhaoController = {
    async listar(req, res) {
        try{
            const resultado = await pool.query('SELECT * FROM Caminhao ORDER BY modeloDescricao');
            res.json(resultado.rows);   
        } catch (error){
            console.error(error);
            res.status(500).json({ error: 'Erro ao buscar caminhões' });
        }
    },

    async criar(req, res) {
        const {placa, modeloDescricao, idCliente} = req.body;
        try{
            const query = 'INSERT INTO Caminhao (placa, modeloDescricao, idCliente) VALUES ($1, $2, $3) RETURNING *';
            const valores = [placa, modeloDescricao, idCliente]
            const resultado = await pool.query(query, valores);
            res.status(201).json(resultado.rows[0]);
        }catch(error){
            console.error(error);
            res.status(500).json({error: 'Erro ao cadastrar caminhão'})
        }
    }
}

module.exports = CaminhaoController;