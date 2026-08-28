const { getDb } = require("../database");
const bcrypt = require("bcryptjs");

async function findByEmail(email) {
    return getDb().getAsync("SELECT * FROM users WHERE email = ?", [email]);
}

async function findById(id) {
    return getDb().getAsync("SELECT id, name, email FROM users WHERE id = ?", [id]);
}

async function create(name, email, password) {
    const hash = await bcrypt.hash(password || "123456", 10);
    const result = await getDb().runAsync(
        "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
        [name, email, hash]
    );
    return result.lastID;
}

async function remove(id) {
    await getDb().runAsync("DELETE FROM users WHERE id = ?", [id]);
}

module.exports = { findByEmail, findById, create, remove };
