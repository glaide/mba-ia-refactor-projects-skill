const express = require("express");
const checkoutController = require("../controllers/checkoutController");

const router = express.Router();

router.post("/checkout", checkoutController.checkout);
router.get("/admin/financial-report", checkoutController.financialReport);
router.delete("/users/:id", checkoutController.deleteUser);

module.exports = router;
