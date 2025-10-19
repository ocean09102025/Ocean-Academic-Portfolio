import { Router } from "express";
import Item from "./models/Item.js";
import Order from "./models/Order.js";

const router = Router();

// helpers
const toNumber = (val) => (typeof val === "number" ? val : Number(val));
const safeDate = (ts) => {
  const d = ts ? new Date(ts) : new Date();
  return isNaN(d.getTime()) ? new Date() : d;
};

// POST /api/inventory/update
router.post("/inventory/update", async (req, res) => {
  try {
    const { itemId, stockLevel, source, ts } = req.body;

    if (!itemId) return res.status(400).json({ error: "itemId is required" });
    const sl = toNumber(stockLevel);
    if (!Number.isFinite(sl)) {
      return res.status(400).json({ error: "stockLevel must be a number" });
    }

    const update = {
      itemId,
      stockLevel: sl,
      source: source || "api",
      lastUpdated: safeDate(ts)
    };

    const doc = await Item.findOneAndUpdate(
      { itemId },
      { $set: update },
      { upsert: true, new: true, setDefaultsOnInsert: true }
    );
    return res.json({ ok: true, data: doc });
  } catch (err) {
    console.error("UPDATE ERROR:", err);
    return res.status(500).json({ error: err?.message || "server error" });
  }
});

// GET /api/inventory/:itemId
router.get("/inventory/:itemId", async (req, res) => {
  try {
    const doc = await Item.findOne({ itemId: req.params.itemId });
    if (!doc) return res.status(404).json({ error: "not found" });
    return res.json({ ok: true, data: doc });
  } catch (err) {
    console.error("READ INV ERROR:", err);
    return res.status(500).json({ error: err?.message || "server error" });
  }
});

// POST /api/orders
router.post("/orders", async (req, res) => {
  try {
    const { orderId, itemId, qty } = req.body;

    if (!orderId || !itemId) {
      return res.status(400).json({ error: "orderId and itemId are required" });
    }
    const q = toNumber(qty);
    if (!Number.isFinite(q)) {
      return res.status(400).json({ error: "qty must be a number" });
    }

    const order = await Order.create({ orderId, itemId, qty: q });
    return res.status(201).json({ ok: true, data: order });
  } catch (err) {
    if (err?.code === 11000) {
      return res.status(409).json({ error: "orderId already exists" });
    }
    console.error("ORDERS ERROR:", err);
    return res.status(500).json({ error: err?.message || "server error" });
  }
});

// GET /api/orders/:orderId
router.get("/orders/:orderId", async (req, res) => {
  try {
    const order = await Order.findOne({ orderId: req.params.orderId });
    if (!order) return res.status(404).json({ error: "not found" });
    return res.json({ ok: true, data: order });
  } catch (err) {
    console.error("READ ORDER ERROR:", err);
    return res.status(500).json({ error: err?.message || "server error" });
  }
});

export default router;
