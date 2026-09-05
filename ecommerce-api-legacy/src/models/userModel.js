const { getDb, runInTransaction } = require("../database");
const bcrypt = require("bcryptjs");

async function findByEmail(email) {
    return getDb().getAsync("SELECT id, name, email FROM users WHERE email = ?", [email]);
}

async function findById(id) {
    return getDb().getAsync("SELECT id, name, email FROM users WHERE id = ?", [id]);
}

async function authenticate(email, password) {
    const row = await getDb().getAsync("SELECT id, pass FROM users WHERE email = ?", [email]);
    if (!row) {
        return null;
    }
    const valid = await bcrypt.compare(password, row.pass);
    if (!valid) {
        return false;
    }
    return { id: row.id };
}

async function create(name, email, password) {
    if (!password) {
        throw new Error("Password is required");
    }
    const hash = await bcrypt.hash(password, 10);
    const result = await getDb().runAsync(
        "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
        [name, email, hash]
    );
    return result.lastID;
}

async function remove(id) {
    return runInTransaction(async (db) => {
        const enrollments = await db.allAsync(
            "SELECT id FROM enrollments WHERE user_id = ?",
            [id]
        );

        for (const enrollment of enrollments) {
            await db.runAsync("DELETE FROM payments WHERE enrollment_id = ?", [enrollment.id]);
        }

        await db.runAsync("DELETE FROM enrollments WHERE user_id = ?", [id]);
        const result = await db.runAsync("DELETE FROM users WHERE id = ?", [id]);
        return result.changes;
    });
}

module.exports = { findByEmail, findById, authenticate, create, remove };
