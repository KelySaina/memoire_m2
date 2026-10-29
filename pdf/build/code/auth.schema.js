import fs from "fs";

// Try reading version.json
let VERSION = "v-unknown";
let BUILD_DATE = new Date().toISOString().split("T")[0];

try {
  const data = JSON.parse(fs.readFileSync("/app/version.json", "utf-8"));
  VERSION = data.version;
  BUILD_DATE = data.date;
} catch (err) {
  console.warn("Could not read version.json, using defaults");
}

import {
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLString,
  GraphQLID,
  GraphQLList,
} from "graphql";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import pool from "./db.js";
import dotenv from "dotenv";

dotenv.config();

// User type
const UserType = new GraphQLObjectType({
  name: "User",
  fields: () => ({
    id: { type: GraphQLID },
    username: { type: GraphQLString },
    email: { type: GraphQLString },
    role: { type: GraphQLString },
    created_at: { type: GraphQLString },
    updated_at: { type: GraphQLString },
  }),
});

const AuthPayloadType = new GraphQLObjectType({
  name: "AuthPayload",
  fields: () => ({
    token: { type: GraphQLString },
    user: { type: UserType },
  }),
});

// Root Query
const RootQuery = new GraphQLObjectType({
  name: "RootQueryType",
  fields: {
    user: {
      type: UserType,
      args: { id: { type: GraphQLID } },
      resolve: async (_, { id }) => {
        const [rows] = await pool.query("SELECT * FROM users WHERE id = ?", [
          id,
        ]);
        return rows[0];
      },
    },
    users: {
      type: new GraphQLList(UserType),
      resolve: async () => {
        const [rows] = await pool.query("SELECT * FROM users");
        return rows;
      },
    },
    healthz: {
      type: GraphQLString,
      resolve: () =>
        `Auth Service is healthy! ${BUILD_DATE} #${VERSION}`,
    },
  },
});

// Mutations
const Mutation = new GraphQLObjectType({
  name: "Mutation",
  fields: {
    register: {
      type: UserType,
      args: {
        username: { type: GraphQLString },
        email: { type: GraphQLString },
        password: { type: GraphQLString },
        role: { type: GraphQLString },
      },
      resolve: async (_, { username, email, password, role }) => {
        const hashedPassword = await bcrypt.hash(password, 10);
        const [result] = await pool.query(
          "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
          [username, email, hashedPassword, role || "customer"]
        );
        return {
          id: result.insertId,
          username,
          email,
          role: role || "customer",
        };
      },
    },
    login: {
      type: AuthPayloadType,
      args: {
        email: { type: GraphQLString },
        password: { type: GraphQLString },
      },
      resolve: async (_, { email, password }) => {
        const [rows] = await pool.query("SELECT * FROM users WHERE email = ?", [email]);
        const user = rows[0];
        if (!user) throw new Error("User not found");

        const valid = await bcrypt.compare(password, user.password_hash);
        if (!valid) throw new Error("Invalid password");

        const token = jwt.sign(
          { id: user.id, email: user.email, role: user.role },
          process.env.JWT_SECRET,
          { expiresIn: "24h" }
        );

        return {
          token,
          user: {
            id: user.id,
            username: user.username,
            email: user.email,
            role: user.role,
          },
        };
      },
    },
  },
});

// ✅ Export default for ES module
export default new GraphQLSchema({
  query: RootQuery,
  mutation: Mutation,
});
