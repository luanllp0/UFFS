const pool = require("../db/db");

const ServicoController = {
  async listar(req, res) {
    try {
      const query = `
                SELECT 
                    s.*, 
                    s.placacaminhao as placa,
                    t.nome as nome_tecnico, 
                    c.nome as nome_cliente,
                    col.nome as nome_colaborador
                FROM Servico s
                JOIN Usuario t ON s.idTecnico = t.idUsuario
                JOIN Caminhao cam ON s.placaCaminhao = cam.placa
                JOIN Cliente c ON cam.idCliente = c.idCliente
                LEFT JOIN Usuario col ON s.idColaborador = col.idUsuario
                ORDER BY s.data DESC
            `;
      const resultado = await pool.query(query);
      res.json(resultado.rows);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro ao listar serviços" });
    }
  },

  async criar(req, res) {
    const {
      data,
      hora,
      descricao,
      valor,
      mesFaturamento,
      idTecnico,
      placaCaminhao,
    } = req.body;
    try {
      const query = `
                INSERT INTO Servico (data, hora, descricao, valor, mesFaturamento, idTecnico, placaCaminhao) 
                VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *
            `;
      const values = [
        data,
        hora,
        descricao,
        valor,
        mesFaturamento,
        idTecnico,
        placaCaminhao,
      ];
      const resultado = await pool.query(query, values);
      res.status(201).json(resultado.rows[0]);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro ao criar serviço" });
    }
  },

  async atualizar(req, res) {
    const { id } = req.params;
    const { descricao, valor, statusConciliacao, idColaborador } = req.body;

    try {
      const query = `
                UPDATE Servico 
                SET descricao = $1, valor = $2, statusConciliacao = $3, idColaborador = $4
                WHERE idServico = $5 RETURNING *
            `;
      const values = [descricao, valor, statusConciliacao, idColaborador, id];
      const resultado = await pool.query(query, values);

      if (resultado.rowCount === 0) {
        return res.status(404).json({ error: "Serviço não encontrado" });
      }
      res.json(resultado.rows[0]);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro ao atualizar serviço" });
    }
  },

  async deletar(req, res) {
    const { id } = req.params;
    try {
      await pool.query("DELETE FROM Servico WHERE idServico = $1", [id]);
      res.status(204).send();
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro ao deletar serviço" });
    }
  },
};

module.exports = ServicoController;
