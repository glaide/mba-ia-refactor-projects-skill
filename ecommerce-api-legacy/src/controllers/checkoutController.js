const courseModel = require("../models/courseModel");
const userModel = require("../models/userModel");
const enrollmentModel = require("../models/enrollmentModel");
const { processPaymentToken } = require("../services/paymentService");

async function checkout(req, res, next) {
    try {
        const { usr, eml, pwd, c_id, payment_token } = req.body;

        if (!usr || !eml || !c_id || !payment_token) {
            return res.status(400).send("Bad Request");
        }

        const course = await courseModel.findActiveById(c_id);
        if (!course) {
            return res.status(404).send("Curso não encontrado");
        }

        let user = await userModel.findByEmail(eml);

        if (!user) {
            if (!pwd) {
                return res.status(400).send("Bad Request");
            }
            const userId = await userModel.create(usr, eml, pwd);
            user = { id: userId };
        } else {
            if (!pwd) {
                return res.status(401).send("Senha obrigatória");
            }
            const authResult = await userModel.authenticate(eml, pwd);
            if (!authResult) {
                return res.status(401).send("Senha inválida");
            }
        }

        const payment = await processPaymentToken(payment_token);
        if (payment.status === "DENIED") {
            return res.status(400).send("Pagamento recusado");
        }

        const enrollmentId = await enrollmentModel.enroll(user.id, c_id, course.price, payment.status);
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
        const changes = await userModel.remove(req.params.id);
        if (changes === 0) {
            return res.status(404).send("Usuário não encontrado");
        }
        res.send("Usuário deletado com sucesso.");
    } catch (error) {
        next(error);
    }
}

module.exports = { checkout, financialReport, deleteUser };
