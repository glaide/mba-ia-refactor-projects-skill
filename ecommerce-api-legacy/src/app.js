const express = require("express");
const { config } = require("./config");
const { initDb } = require("./database");
const apiRoutes = require("./routes/apiRoutes");
const { errorHandler } = require("./middlewares/errorHandler");

const app = express();
app.use(express.json());

async function start() {
    await initDb();
    app.use("/api", apiRoutes);
    app.use(errorHandler);

    app.listen(config.port, () => {
        console.log(`LMS API rodando na porta ${config.port}...`);
    });
}

start().catch((err) => {
    console.error("Falha ao iniciar:", err);
    process.exit(1);
});
