const express = require('express');
const router = express.Router();
const CaminhaoController = require('../controllers/CaminhaoController');

router.get('/', CaminhaoController.listar);

router.post('/', CaminhaoController.criar);

module.exports = router;