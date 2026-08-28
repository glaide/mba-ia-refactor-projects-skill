const { getDb } = require("../database");

async function enroll(userId, courseId, amount) {
    const db = getDb();
    const enrollment = await db.runAsync(
        "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
        [userId, courseId]
    );
    await db.runAsync(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
        [enrollment.lastID, amount, "PAID"]
    );
    await db.runAsync(
        "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
        [`Checkout curso ${courseId} por ${userId}`]
    );
    return enrollment.lastID;
}

async function getFinancialReport() {
    const db = getDb();
    const courses = await db.allAsync("SELECT * FROM courses");
    const report = [];

    for (const course of courses) {
        const courseData = { course: course.title, revenue: 0, students: [] };
        const enrollments = await db.allAsync(
            "SELECT * FROM enrollments WHERE course_id = ?",
            [course.id]
        );

        for (const enrollment of enrollments) {
            const user = await db.getAsync(
                "SELECT name, email FROM users WHERE id = ?",
                [enrollment.user_id]
            );
            const payment = await db.getAsync(
                "SELECT amount, status FROM payments WHERE enrollment_id = ?",
                [enrollment.id]
            );
            if (payment && payment.status === "PAID") {
                courseData.revenue += payment.amount;
            }
            courseData.students.push({
                student: user ? user.name : "Unknown",
                paid: payment ? payment.amount : 0,
            });
        }
        report.push(courseData);
    }
    return report;
}

module.exports = { enroll, getFinancialReport };
