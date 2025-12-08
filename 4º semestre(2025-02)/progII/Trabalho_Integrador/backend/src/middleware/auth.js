const jwt = require("jsonwebtoken");

function verificarToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ error: "Acesso negado" });
  }

  try {
    const decoded = jwt.verify(token, "SEGREDO_DO_LUAN");
    req.user = decoded;
    next();
  } catch (error) {
    res.status(403).json({ error: "Token inválido" });
  }
}

module.exports = verificarToken;
