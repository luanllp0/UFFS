const express = require('express');
const router = express.Router();
const ClienteController = require('../controllers/ClienteController');

router.get('/', ClienteController.listar);

router.post('/', ClienteController.criar);

router.delete('/:id', ClienteController.deletar);

module.exports = router;