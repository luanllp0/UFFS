const express = require('express');
const cors = require('cors');
const pool = require('./db/db');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Servidor Rodofrio rodando!');
});

pool.query('SELECT NOW()')
    .then(() => console.log('✅ Banco de Dados detectado e respondendo!'))
    .catch(err => console.error('❌ Erro ao conectar no banco:', err));

app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando na porta ${PORT}`);
});