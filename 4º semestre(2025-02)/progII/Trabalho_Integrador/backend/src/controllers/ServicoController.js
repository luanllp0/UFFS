const pool = require('../db/db');

const ServicoController = {
    async listar(req,res){
        try{
            const query = `
            SELECT 
                s.IdServico, s.Data, s.hora, s.descricao, s.valor, s.statusConciliacao,
                u.nome AS nome_tecnico,
                c.nome AS nome_cliente, 
                cam.placa
            FROM Servico s
            JOIN Tecnico_Terceirizado t ON s.idTecnico = t.IdUsuario
            JOIN Usuario u ON t.IdUsuario = u.IdUsuario
            JOIN Caminhao cam ON s.placaCaminhao = cam.placa
            JOIN Cliente c ON cam.idCliente = c.IdCliente
            ORDER BY s.Data DESC
            `;
            const resultado = await pool.query(query);
            res.json(resultado.rows);
        }catch(error){
            console.error(error);
            res.status (500).json({ error: 'Erro ao buscar serviços'})
        }
    },

    async criar(req,res){
        const {data, hora, descricao, valor, mesFaturamento, idTecnico, placaCaminhao} = req.body;

        try{
            const query = `
                INSERT INTO Servico 
                (Data, hora, descricao, valor, MesFaturamento, idTecnico, placaCaminhao) 
                VALUES ($1, $2, $3, $4, $5, $6, $7) 
                RETURNING *
            `;
            const valores = [data, hora, descricao, valor, mesFaturamento, idTecnico, placaCaminhao];
            const resultado = await pool.query(query, valores);
            res.status(201).json(resultado.rows[0]);
        }catch(error){
            console.error(error);
            res.status(500).json({ error: 'Erro ao lançar serviço' });
        }
    }
};

module.exports = ServicoController;