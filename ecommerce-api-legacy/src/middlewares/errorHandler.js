function errorHandler(err, _req, res, _next) {
    console.error("[ERROR]", err.message);
    res.status(500).send("Erro interno do servidor");
}

module.exports = { errorHandler };
