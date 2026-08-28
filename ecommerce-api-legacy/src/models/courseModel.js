const { getDb } = require("../database");

async function findActiveById(id) {
    return getDb().getAsync("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
}

async function getAll() {
    return getDb().allAsync("SELECT * FROM courses");
}

module.exports = { findActiveById, getAll };
