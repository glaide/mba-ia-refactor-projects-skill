async function processPaymentToken(token) {
    if (!token || typeof token !== "string" || !token.startsWith("tok_")) {
        return { status: "DENIED" };
    }

    if (token === "tok_declined") {
        return { status: "DENIED" };
    }

    return { status: "PAID" };
}

module.exports = { processPaymentToken };
