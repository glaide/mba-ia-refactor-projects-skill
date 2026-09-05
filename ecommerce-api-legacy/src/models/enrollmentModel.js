const { getDb, runInTransaction } = require("../database");

async function enroll(userId, courseId, amount, status) {
    return runInTransaction(async (db) => {
        const enrollment = await db.runAsync(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        await db.runAsync(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollment.lastID, amount, status]
        );
        await db.runAsync(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [`Checkout curso ${courseId} por ${userId}`]
        );
        return enrollment.lastID;
    });
}

async function getFinancialReport() {
    const rows = await getDb().allAsync(`
        SELECT
            c.title AS course_title,
            u.name AS student_name,
            p.amount AS paid_amount,
            p.status AS payment_status
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN users u ON u.id = e.user_id
        LEFT JOIN payments p ON p.enrollment_id = e.id
        ORDER BY c.id, e.id
    `);

    const reportByCourse = new Map();

    for (const row of rows) {
        if (!reportByCourse.has(row.course_title)) {
            reportByCourse.set(row.course_title, {
                course: row.course_title,
                revenue: 0,
                students: [],
            });
        }

        if (!row.student_name) {
            continue;
        }

        const courseData = reportByCourse.get(row.course_title);
        if (row.payment_status === "PAID") {
            courseData.revenue += row.paid_amount || 0;
        }
        courseData.students.push({
            student: row.student_name,
            paid: row.paid_amount || 0,
        });
    }

    return Array.from(reportByCourse.values());
}

module.exports = { enroll, getFinancialReport };
