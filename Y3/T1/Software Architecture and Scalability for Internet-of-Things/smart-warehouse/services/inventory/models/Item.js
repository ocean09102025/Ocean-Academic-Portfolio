import mongoose from "mongoose";

const ItemSchema = new mongoose.Schema(
  {
    itemId: { type: String, required: true, unique: true },
    stockLevel: { type: Number, required: true },
    source: { type: String, default: "unknown" },
    lastUpdated: { type: Date, default: Date.now }
  },
  { collection: "inventory" }
);

export default mongoose.model("Item", ItemSchema);
