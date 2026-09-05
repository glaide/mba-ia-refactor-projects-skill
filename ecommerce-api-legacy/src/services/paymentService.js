const APPROVED_CARD_PREFIX = "4";

function processPayment(cardNumber) {
    if (!cardNumber || typeof cardNumber !== "string") {
        return { status: "DENIED" };
    }

    return {
        status: cardNumber.startsWith(APPROVED_CARD_PREFIX) ? "PAID" : "DENIED",
    };
}

module.exports = { processPayment };
