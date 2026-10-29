describe("Login functionality", () => {

  beforeEach(() => {
    // Replace with your frontend URL (service exposed via Ingress or localhost)
    cy.visit("/login");
  });

  it("should successfully login with valid credentials", () => {
    cy.get("input[placeholder='Email']").type("ks@ks.ks");
    cy.get("input[placeholder='Password']").type("ks");
    cy.get("button[type='submit']").click();

    // Wait for redirect and verify landing page
    cy.url({timeout: 25000}).should("not.include", "/login");
    cy.url({timeout: 25000}).should("include", "/");
    cy.contains("My Orders", { timeout: 25000 }).should("exist");
  });

  it("should successfully login with valid admin credentials", () => {
    cy.get("input[placeholder='Email']").type("admin@ks.ks");
    cy.get("input[placeholder='Password']").type("admin");
    cy.get("button[type='submit']").click();

    // Wait for redirect and verify landing page
    cy.url({timeout: 25000}).should("not.include", "/login");
    cy.url({timeout: 25000}).should("include", "/");
    cy.contains("Admin Dashboard", { timeout: 25000 }).should("exist");
  });

  it("should show an error for invalid credentials", () => {
    cy.get("input[placeholder='Email']").type("wrong@example.com");
    cy.get("input[placeholder='Password']").type("wrongpass");
    cy.get("button[type='submit']").click();

    cy.contains("Invalid credentials", { timeout: 25000 }).should("be.visible");
    cy.url({ timeout: 25000 }).should("include", "/login");
  });
});
