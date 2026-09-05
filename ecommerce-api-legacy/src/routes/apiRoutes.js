const express = require("express");
const checkoutController = require("../controllers/checkoutController");
const { requireAdmin } = require("../middlewares/auth");

const router = express.Router();

router.post("/checkout", checkoutController.checkout);
router.get("/admin/financial-report", requireAdmin, checkoutController.financialReport);
router.delete("/users/:id", requireAdmin, checkoutController.deleteUser);

module.exports = router;
