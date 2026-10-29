import express from "express";
import { graphqlHTTP } from "express-graphql";
import schema from "./schema.js";
import { authenticate } from "./auth.js";
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();

const app = express();

app.use(cors());

app.use(
  "/graphql",
  graphqlHTTP((req) => ({
    schema,
    graphiql: true,
    context: { user: authenticate(req) },
  }))
);

const PORT = process.env.PORT || 4002;
app.listen(PORT, () => {
  console.log(`Order service running at ${PORT}/graphql`);
});
