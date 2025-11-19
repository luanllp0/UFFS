const express = require('express');
const router = express.Router();
const ClienteController = require('../controllers/ClienteController');

router.get('/', ClienteController.listar);

router.post('/', ClienteController.criar);

module.exports = router;