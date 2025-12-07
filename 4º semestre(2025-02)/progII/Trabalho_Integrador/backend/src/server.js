const express = require('express');
const cors = require('cors');
const pool = require('./db/db');

const clienteRoutes = require('./routes/clienteRoutes');
const caminhaoRoutes = require('./routes/caminhaoRoutes');
const servicoRoutes = require('./routes/servicoRoutes');

const AuthController = require('./controllers/AuthController');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

app.post('/login', AuthController.login);

app.use('/clientes', clienteRoutes);
app.use('/caminhoes', caminhaoRoutes);
app.use('/servicos', servicoRoutes);

app.get('/', (req, res) => {
    res.send('Servidor Rodofrio rodando!');
});

pool.query('SELECT NOW()')
    .then(() => console.log('✅ Banco de Dados detectado e respondendo!'))
    .catch(err => console.error('❌ Erro ao conectar no banco:', err));

app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando na porta ${PORT}`);
});