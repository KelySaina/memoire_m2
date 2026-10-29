import express from "express";
import { graphqlHTTP } from "express-graphql";
import schema from "./schema.js";
import dotenv from "dotenv";
import cors from "cors";

dotenv.config();


const app = express();

app.use(cors());

app.use(
  "/graphql",
  graphqlHTTP({
    schema,
    graphiql: true,
  })
);

const PORT = process.env.PORT || 4001;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Auth service running at ${PORT}/graphql`);
});
