const { Pool } = require("pg");
const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../../.env") });

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

pool.on("connect", () => {
  console.log("Base de Dados conectada com sucesso!");
});

pool.on("error", (err) => {
  console.error("Erro inesperado no cliente do banco", err);
  process.exit(-1);
});

module.exports = pool;
