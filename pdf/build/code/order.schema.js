import fs from "fs";
import {
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLID,
  GraphQLString,
  GraphQLFloat,
  GraphQLInt,
  GraphQLList,
  GraphQLInputObjectType,
} from "graphql";
import pool from "./db.js";
import axios from "axios";
import dotenv from "dotenv";
dotenv.config();

// --- Version info ---
let VERSION = "v-unknown";
let BUILD_DATE = new Date().toISOString().split("T")[0];
try {
  const data = JSON.parse(fs.readFileSync("/app/version.json", "utf-8"));
  VERSION = data.version;
  BUILD_DATE = data.date;
} catch (err) {
  console.warn("Could not read version.json, using defaults");
}

// --- Input type for order items ---
const OrderItemInputType = new GraphQLInputObjectType({
  name: "OrderItemInput",
  fields: {
    product_id: { type: GraphQLID },
    quantity: { type: GraphQLInt },
  },
});

// --- Product type (for resolver) ---
const ProductType = new GraphQLObjectType({
  name: "Product",
  fields: {
    id: { type: GraphQLID },
    name: { type: GraphQLString },
    description: { type: GraphQLString },
    price: { type: GraphQLFloat },
    stock: { type: GraphQLInt },
  },
});

// --- User type (for resolver) ---
const UserType = new GraphQLObjectType({
  name: "User",
  fields: {
    id: { type: GraphQLID },
    username: { type: GraphQLString },
    email: { type: GraphQLString },
    role: { type: GraphQLString },
  },
});

// --- Order Item Type ---
const OrderItemType = new GraphQLObjectType({
  name: "OrderItem",
  fields: () => ({
    id: { type: GraphQLID },
    product_id: { type: GraphQLID },
    quantity: { type: GraphQLInt },
    unit_price: { type: GraphQLFloat },
    // resolve product info from product-service
    product: {
      type: ProductType,
      resolve: async (parent) => {
        try {
          const query = `
            query($id: ID!) {
              product(id: $id) {
                id
                name
                description
                price
              }
            }
          `;
          const response = await axios.post(process.env.PRODUCT_SERVICE_URL, {
            query,
            variables: { id: parent.product_id },
          });
          return response.data.data.product;
        } catch (err) {
          console.error("Failed to fetch product:", err);
          return null;
        }
      },
    },
  }),
});

// --- Order Type ---
const OrderType = new GraphQLObjectType({
  name: "Order",
  fields: () => ({
    id: { type: GraphQLID },
    user_id: { type: GraphQLID },
    total_amount: { type: GraphQLFloat },
    status: { type: GraphQLString },
    items: {
      type: new GraphQLList(OrderItemType),
      resolve: async (parent) => {
        const [rows] = await pool.query(
          "SELECT * FROM order_items WHERE order_id = ?",
          [parent.id]
        );
        return rows;
      },
    },
    created_at: { type: GraphQLString },
    updated_at: { type: GraphQLString },
    // resolve user from auth-service
    user: {
      type: UserType,
      resolve: async (parent) => {
        try {
          const query = `
            query($id: ID!) {
              user(id: $id) {
                id
                username
                email
                role
              }
            }
          `;
          const response = await axios.post(process.env.AUTH_SERVICE_URL, {
            query,
            variables: { id: parent.user_id },
          });
          return response.data.data.user;
        } catch (err) {
          console.error("Failed to fetch user:", err);
          return null;
        }
      },
    },
  }),
});

// --- Root Query ---
const RootQuery = new GraphQLObjectType({
  name: "RootQueryType",
  fields: {
    myOrders: {
      type: new GraphQLList(OrderType),
      resolve: async (_, __, context) => {
        if (!context.user) throw new Error("Unauthorized");
        const [rows] = await pool.query(
          "SELECT * FROM orders WHERE user_id = ?",
          [context.user.id]
        );
        return rows;
      },
    },
    orders: {
      type: new GraphQLList(OrderType),
      resolve: async (_, __, context) => {
        if (!context.user) throw new Error("Unauthorized");
        const [rows] = await pool.query("SELECT * FROM orders");
        return rows;
      },
    },
    healthz: {
      type: GraphQLString,
      resolve: () =>
        `Order Service is healthy!! ${BUILD_DATE} #${VERSION}`,
    },
  },
});

// --- Mutations ---
const Mutation = new GraphQLObjectType({
  name: "Mutation",
  fields: {
    createOrder: {
      type: OrderType,
      args: {
        items: { type: new GraphQLList(OrderItemInputType) },
      },
      resolve: async (_, { items }, context) => {
        if (!context.user) throw new Error("Unauthorized");
        const conn = await pool.getConnection();
        let totalAmount = 0;

        try {
          await conn.beginTransaction();

          // fetch product info and calculate total
          for (const item of items) {
            const query = `
              query($id: ID!) {
                product(id: $id) {
                  id
                  price
                  stock
                }
              }
            `;
            const response = await axios.post(process.env.PRODUCT_SERVICE_URL, {
              query,
              variables: { id: item.product_id },
            });
            const product = response.data.data.product;
            if (!product) throw new Error(`Product ${item.product_id} not found`);
            if (product.stock < item.quantity)
              throw new Error(`Not enough stock for product ${item.product_id}`);

            item.unit_price = product.price;
            totalAmount += product.price * item.quantity;
          }

          // insert order
          const [orderResult] = await conn.query(
            "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)",
            [context.user.id, totalAmount]
          );
          const orderId = orderResult.insertId;

          // insert order_items
          for (const item of items) {
            await conn.query(
              "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
              [orderId, item.product_id, item.quantity, item.unit_price]
            );
          }

          await conn.commit();
          return {
            id: orderId,
            user_id: context.user.id,
            total_amount: totalAmount,
            status: "pending",
          };
        } catch (err) {
          await conn.rollback();
          throw err;
        } finally {
          conn.release();
        }
      },
    },
    updateOrderStatus: {
      type: OrderType,
      args: {
        orderId: { type: GraphQLID },
        status: { type: GraphQLString },
      },
      resolve: async (_, { orderId, status }, context) => {
        // 1. Authorization check
        if (!context.user) throw new Error("Unauthorized");

        // 2. Validate status
        const validStatuses = ["pending", "paid", "shipped", "cancelled"];
        if (!validStatuses.includes(status)) {
          throw new Error(`Invalid status: ${status}`);
        }

        // 3. Update DB
        const [result] = await pool.query(
          "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
          [status, orderId]
        );

        if (result.affectedRows === 0) {
          throw new Error(`Order with ID ${orderId} not found`);
        }

        // 4. Return updated order
        const [rows] = await pool.query("SELECT * FROM orders WHERE id = ?", [
          orderId,
        ]);

        return rows[0];
      },
    },

  },
});

export default new GraphQLSchema({
  query: RootQuery,
  mutation: Mutation,
});
