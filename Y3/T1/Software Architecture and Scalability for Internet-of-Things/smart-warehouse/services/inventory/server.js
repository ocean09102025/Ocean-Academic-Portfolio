import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import router from "./index.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_KEY;

// middleware
app.use(express.json());
app.use(cors());
app.use(helmet());
app.use(rateLimit({ windowMs: 60 * 1000, max: 100 }));

// simple API key check (skip /health)
app.use((req, res, next) => {
  if (req.path === "/health") return next();
  const key = req.header("x-api-key");
  if (!key || key !== API_KEY) return res.status(401).json({ error: "Invalid or missing API key" });
  next();
});

// health
app.get("/health", (req, res) => res.json({ ok: true, service: "inventory-service" }));

// routes under /api
app.use("/api", router);

// connect DB + start
const start = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("MongoDB connected");
    app.listen(PORT, () => console.log(`API running on http://localhost:${PORT}`));
  } catch (err) {
    console.error("DB connection failed:", err.message);
    process.exit(1);
  }
};
start();
