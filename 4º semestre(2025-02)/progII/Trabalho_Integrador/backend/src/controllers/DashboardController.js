const pool = require("../db/db");

const DashboardController = {
  async getResumo(req, res) {
    const { id, tipo } = req.user;

    try {
      const clientes = await pool.query("SELECT COUNT(*) FROM Cliente");
      const caminhoes = await pool.query("SELECT COUNT(*) FROM Caminhao");

      let queryPendentes =
        "SELECT COUNT(*) FROM Servico WHERE statusConciliacao = 'Pendente'";
      let queryFaturamento =
        "SELECT SUM(valor) FROM Servico WHERE statusConciliacao = 'Confirmado'";
      let params = [];

      if (tipo === "Tecnico Terceirizado") {
        queryPendentes += " AND idTecnico = $1";
        queryFaturamento += " AND idTecnico = $1";
        params = [id];
      }

      const pendentes = await pool.query(queryPendentes, params);
      const faturamento = await pool.query(queryFaturamento, params);

      res.json({
        totalClientes: clientes.rows[0].count,
        totalCaminhoes: caminhoes.rows[0].count,
        servicosPendentes: pendentes.rows[0].count,
        totalFaturado: faturamento.rows[0].sum || 0,
      });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro ao buscar dados do dashboard" });
    }
  },
};

module.exports = DashboardController;
