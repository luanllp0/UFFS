const express = require('express');
const router = express.Router();
const ServicoController = require('../controllers/ServicoController');

router.get('/', ServicoController.listar);
router.post('/', ServicoController.criar);

module.exports = router;