from fpdf import FPDF
from datetime import datetime
import mysql.connector


class InvoiceGenerator:
    def __init__(self, db_config, invoice_id):
        """
        Initializes the InvoiceGenerator with database configuration and invoice ID.
        """
        self.db_config = db_config
        self.invoice_id = invoice_id
        self.invoice_data = self.fetch_invoice_data()

    def fetch_invoice_data(self):
        """
        Fetches customer, seller, and item details for the invoice from the database.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch customer data
        cursor.execute(
            """
            SELECT name, contact_number, email, address FROM customers
            WHERE id = (SELECT customer_id FROM invoices WHERE id = %s)
            """,
            (self.invoice_id,)
        )
        customer = cursor.fetchone()

        # Fetch seller data
        cursor.execute("SELECT name, contact_number, email, address FROM sellers LIMIT 1")
        seller = cursor.fetchone()

        # Fetch item data
        cursor.execute(
            """
            SELECT i.name AS item_name, li.quantity, li.price
            FROM line_items li
            JOIN items i ON li.item_id = i.id
            WHERE li.invoice_id = %s
            """,
            (self.invoice_id,)
        )
        items = cursor.fetchall()

        conn.close()

        return {"customer": customer, "seller": seller, "items": items}

    def generate_invoice(self, file_name="invoice.pdf"):
        """
        Generates a PDF invoice and saves it with the given file name.
        """
        pdf = FPDF()
        pdf.add_page()

        # Title and Invoice Date
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "INVOICE", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

        pdf.cell(0, 10, "", ln=True)  # Spacer

        # Seller Information
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Seller Information:", ln=True, align="L")
        pdf.set_font("Arial", "", 10)
        seller = self.invoice_data.get("seller", {})
        pdf.cell(200, 10, f"Name: {seller.get('name', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Contact: {seller.get('contact_number', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Email: {seller.get('email', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Address: {seller.get('address', 'N/A')}", ln=True, align="L")

        pdf.cell(0, 10, "", ln=True)  # Spacer

        # Customer Information
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Customer Information:", ln=True, align="L")
        pdf.set_font("Arial", "", 10)
        customer = self.invoice_data.get("customer", {})
        pdf.cell(200, 10, f"Name: {customer.get('name', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Contact: {customer.get('contact_number', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Email: {customer.get('email', 'N/A')}", ln=True, align="L")
        pdf.cell(200, 10, f"Address: {customer.get('address', 'N/A')}", ln=True, align="L")

        pdf.cell(0, 10, "", ln=True)  # Spacer

        # Table Header
        pdf.set_font("Arial", "B", 10)
        pdf.cell(80, 10, "Item", border=1, align="C")
        pdf.cell(30, 10, "Quantity", border=1, align="C")
        pdf.cell(40, 10, "Price", border=1, align="C")
        pdf.cell(40, 10, "Total", border=1, align="C")
        pdf.ln()

        # Table Rows
        pdf.set_font("Arial", "", 10)
        items = self.invoice_data.get("items", [])
        net_total = 0
        for item in items:
            pdf.cell(80, 10, item["item_name"], border=1)
            pdf.cell(30, 10, str(item["quantity"]), border=1, align="C")
            pdf.cell(40, 10, f"=N={item['price']:.2f}", border=1, align="R")
            total = item["quantity"] * item["price"]
            pdf.cell(40, 10, f"=N={total:.2f}", border=1, align="R")
            pdf.ln()
            net_total += total

        # Net Total
        pdf.cell(0, 10, "", ln=True)  # Spacer
        pdf.cell(150, 10, "Net Total:", align="R")
        pdf.cell(40, 10, f"=N={net_total:.2f}", border=1, align="R")

        # Save PDF
        pdf.output(file_name)
        print(f"Invoice saved as {file_name}")


# Usage example
if __name__ == "__main__":
    # Database configuration (adjust to match your MySQL credentials and database)
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "pos",
        "port": "1207"
    }

    # Specify the invoice ID you want to generate
    invoice_id = 1  # Replace with the appropriate invoice ID

    # Generate and save invoice
    generator = InvoiceGenerator(db_config, invoice_id)
    generator.generate_invoice("customer_invoice.pdf")
