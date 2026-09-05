const config = {
    port: parseInt(process.env.PORT || "3000", 10),
    adminApiKey: process.env.ADMIN_API_KEY,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    dbUser: process.env.DB_USER,
    dbPass: process.env.DB_PASS,
    smtpUser: process.env.SMTP_USER,
};

const REQUIRED_ENV = [
    ["ADMIN_API_KEY", "adminApiKey"],
    ["PAYMENT_GATEWAY_KEY", "paymentGatewayKey"],
    ["DB_USER", "dbUser"],
    ["DB_PASS", "dbPass"],
    ["SMTP_USER", "smtpUser"],
];

function validateConfig() {
    const missing = REQUIRED_ENV.filter(([, key]) => !config[key]).map(([envName]) => envName);
    if (missing.length > 0) {
        throw new Error(`Missing required environment variables: ${missing.join(", ")}`);
    }
}

module.exports = { config, validateConfig };
