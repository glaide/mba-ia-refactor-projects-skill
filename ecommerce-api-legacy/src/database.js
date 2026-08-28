const sqlite3 = require("sqlite3").verbose();
const { promisify } = require("util");
const bcrypt = require("bcryptjs");

let db = null;

function getDb() {
    if (!db) {
        db = new sqlite3.Database(":memory:");
        promisifyDb(db);
    }
    return db;
}

function promisifyDb(database) {
    database.runAsync = function (sql, params = []) {
        return new Promise((resolve, reject) => {
            database.run(sql, params, function (err) {
                if (err) reject(err);
                else resolve({ lastID: this.lastID, changes: this.changes });
            });
        });
    };
    database.getAsync = promisify(database.get.bind(database));
    database.allAsync = promisify(database.all.bind(database));
}

async function initDb() {
    const database = getDb();
    await database.runAsync(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)"
    );
    await database.runAsync(
        "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)"
    );
    await database.runAsync(
        "CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)"
    );
    await database.runAsync(
        "CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)"
    );
    await database.runAsync(
        "CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)"
    );

    const userCount = await database.getAsync("SELECT COUNT(*) as count FROM users");
    if (userCount.count === 0) {
        const hash = await bcrypt.hash("123", 10);
        await database.runAsync(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            ["Leonan", "leonan@fullcycle.com.br", hash]
        );
        await database.runAsync(
            "INSERT INTO courses (title, price, active) VALUES (?, ?, ?), (?, ?, ?)",
            ["Clean Architecture", 997.0, 1, "Docker", 497.0, 1]
        );
        await database.runAsync(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [1, 1]
        );
        await database.runAsync(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [1, 997.0, "PAID"]
        );
    }
}

module.exports = { getDb, initDb };
