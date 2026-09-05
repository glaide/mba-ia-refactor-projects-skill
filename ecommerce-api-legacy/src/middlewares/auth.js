const { config } = require("../config");

function requireAdmin(req, res, next) {
    const headerKey = req.headers["x-api-key"];
    const bearerKey = (req.headers.authorization || "").replace(/^Bearer\s+/i, "");
    const providedKey = headerKey || bearerKey;

    if (!providedKey || providedKey !== config.adminApiKey) {
        return res.status(401).send("Unauthorized");
    }

    next();
}

module.exports = { requireAdmin };
