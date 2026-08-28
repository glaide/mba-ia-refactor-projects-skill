const courseModel = require("../models/courseModel");
const userModel = require("../models/userModel");
const enrollmentModel = require("../models/enrollmentModel");
const bcrypt = require("bcryptjs");

async function checkout(req, res, next) {
    try {
        const { usr, eml, pwd, c_id, card } = req.body;

        if (!usr || !eml || !c_id || !card) {
            return res.status(400).send("Bad Request");
        }

        const course = await courseModel.findActiveById(c_id);
        if (!course) {
            return res.status(404).send("Curso não encontrado");
        }

        let user = await userModel.findByEmail(eml);

        if (!user) {
            const userId = await userModel.create(usr, eml, pwd);
            user = { id: userId };
        } else if (pwd) {
            const valid = await bcrypt.compare(pwd, user.pass);
            if (!valid) {
                return res.status(401).send("Senha inválida");
            }
        }

        const status = card.startsWith("4") ? "PAID" : "DENIED";
        if (status === "DENIED") {
            return res.status(400).send("Pagamento recusado");
        }

        const enrollmentId = await enrollmentModel.enroll(user.id, c_id, course.price);
        res.status(200).json({ msg: "Sucesso", enrollment_id: enrollmentId });
    } catch (error) {
        next(error);
    }
}

async function financialReport(_req, res, next) {
    try {
        const report = await enrollmentModel.getFinancialReport();
        res.json(report);
    } catch (error) {
        next(error);
    }
}

async function deleteUser(req, res, next) {
    try {
        await userModel.remove(req.params.id);
        res.send("Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.");
    } catch (error) {
        next(error);
    }
}

module.exports = { checkout, financialReport, deleteUser };
