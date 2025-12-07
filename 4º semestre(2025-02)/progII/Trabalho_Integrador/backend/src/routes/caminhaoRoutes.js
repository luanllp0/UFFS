const express = require('express');
const router = express.Router();
const CaminhaoController = require('../controllers/CaminhaoController');

router.get('/', CaminhaoController.listar);

router.post('/', CaminhaoController.criar);

router.delete('/:placa', CaminhaoController.deletar);

module.exports = router;