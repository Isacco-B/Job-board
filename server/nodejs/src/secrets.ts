import dotenv from "dotenv";

dotenv.config({ path: ".env" });

// Server
export const PORT = process.env.PORT || 4000;
export const NODE_ENV = process.env.NODE_ENV;

// Tokens
export const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET!;
export const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET!;
export const PASSWORD_TOKEN_SECRET = process.env.PASSWORD_TOKEN_SECRET!;

// Email
export const EMAIL_HOST = process.env.EMAIL_HOST;
export const EMAIL_PORT = process.env.EMAIL_PORT;
export const EMAIL_ADDRESS = process.env.EMAIL_ADDRESS;
export const EMAIL_PASSWORD = process.env.EMAIL_PASSWORD;
