const pool = require("../db/db");
const jwt = require("jsonwebtoken");

const AuthController = {
  async login(req, res) {
    const { email, senha } = req.body;

    try {
      const query = "SELECT * FROM Usuario WHERE login = $1";
      const resultado = await pool.query(query, [email]);
      const usuario = resultado.rows[0];

      if (!usuario) {
        return res.status(401).json({ error: "Usuário não encontrado" });
      }

      if (usuario.senha !== senha) {
        return res.status(401).json({ error: "Senha incorreta" });
      }

      const token = jwt.sign(
        { id: usuario.idusuario, nome: usuario.nome, tipo: usuario.tipo },
        "SEGREDO_DO_LUAN",
        { expiresIn: "1d" },
      );

      res.json({
        user: {
          id: usuario.idusuario,
          nome: usuario.nome,
          email: usuario.login,
          tipo: usuario.tipo,
        },
        token,
      });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Erro no servidor" });
    }
  },
};

module.exports = AuthController;
