from ariadne import QueryType, MutationType, make_executable_schema, gql
from db import get_connection
import json

# --- Load version info safely ---
try:
    with open("/app/version.json") as f:
        VERSION_INFO = json.load(f)
except FileNotFoundError:
    VERSION_INFO = {"version": "v-unknown", "date": "unknown"}

# --- GraphQL Schema Definition ---
type_defs = gql("""
type Product {
  id: ID!
  name: String!
  description: String
  price: Float!
  stock: Int!
}

type Query {
  products: [Product!]!
  product(id: ID!): Product
  healthz: String!
}

type Mutation {
  addProduct(name: String!, description: String, price: Float!, stock: Int): Product
  updateStock(id: ID!, stock: Int!): Product
}
""")

query = QueryType()
mutation = MutationType()

# --- Query Resolvers ---
@query.field("products")
def resolve_products(*_):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@query.field("product")
def resolve_product(*_, id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


@query.field("healthz")
def resolve_healthz(*_):
    return f"Product Service is healthy!! {VERSION_INFO['date']} #{VERSION_INFO['version']}"

# --- Mutation Resolvers ---
@mutation.field("addProduct")
def resolve_add_product(*_, name, description=None, price=0.0, stock=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
        (name, description, price, stock)
    )
    conn.commit()
    product_id = cursor.lastrowid

    # Fetch the inserted product for full response
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row


@mutation.field("updateStock")
def resolve_update_stock(*_, id, stock):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE products SET stock=%s WHERE id=%s", (stock, id))
    conn.commit()

    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row


# --- Executable Schema ---
schema = make_executable_schema(type_defs, query, mutation)
