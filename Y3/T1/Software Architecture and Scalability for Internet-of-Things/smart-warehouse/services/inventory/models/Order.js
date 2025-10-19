import mongoose from "mongoose";

const OrderSchema = new mongoose.Schema(
  {
    orderId: { type: String, required: true, unique: true },
    itemId: { type: String, required: true },
    qty: { type: Number, required: true },
    status: { type: String, default: "PENDING" },
    createdAt: { type: Date, default: Date.now }
  },
  { collection: "orders" }
);

export default mongoose.model("Order", OrderSchema);
