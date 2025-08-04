from mcp.server.fastmcp import FastMCP
import json
from pydantic import ValidationError


import logging

from utils import logging_config
from schemas import models
from services import users, bills, inventory

# Initialize Logging
logging_config.setup_logging()
logger = logging.getLogger("inventorymcp")

mcp = FastMCP("inventorymcp", version="0.1.0", timeout=300)



# User management tools
@mcp.tool()
async def fetch_users():
    """
        Gets the list of all users from the inventory management system server in json format.
        There are three types of users: Admin, Stocker and Cashier.

        Returns:
            A list of users in json format, or an error message if the request fails.
    """

    return await users.fetchUsers()


@mcp.tool()
async def add_user(username: str, password: str, email: str, phone: str, address: str, type: str):
    """
        Adds a new user to the inventory management system.
        
        Args:
            username: The username of the new user.
            password: The password for the new user.
            email: The email address of the new user.
            phone: The phone number of the new user.
            address: The address of the new user.
            type: The type of user (e.g., Admin, Stocker, Cashier).
        
        Returns:
            A confirmation message or an error message in json format if the request fails.
    """

    try:
        user = models.User(username=username, password=password, email=email, phone=phone, address=address, type=type)
        return await users.addUser(user)

    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})



# Inventory Management Tools
@mcp.tool()
async def fetch_inventory_items():
    """
        Fetches the list of all inventory items from the inventory management system server in json format.
        
        Returns:
            A list of inventory items in json format, or an error message if the request fails.
    """
    return await inventory.fetchInventoryItems()


@mcp.tool()
async def add_inventory_item(name: str, price: int, stock: int, description: str):
    """
        Adds a new inventory item to the inventory management system.
        
        Args:
            name: The name of the inventory item.
            price: The price of the inventory item.
            stock: The new_stock quantity of the inventory item.
            description: A description of the inventory item.
        
        Returns:
            A confirmation message or an error message in json format if the request fails.
    """

    try:
        item = models.InventoryItemInsert(name=name, price=price, stock=stock, description=description)
        return await inventory.addInventoryItem(item)

    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})

@mcp.tool()
async def update_inventory_item(prod_id: int, name: str, price: int, stock: int, description: str):
    """
        Updates an existing inventory item in the inventory management system.
        
        Args:
            prod_id: The ID of the inventory item to update.
            name: The new name of the inventory item.
            price: The new price of the inventory item.
            stock: The new new_stock quantity of the inventory item.
            description: The new description of the inventory item.
        
        Returns:
            A confirmation message or an error message in json format if the request fails.
    """

    try:
        item = models.InventoryItemUpdate(prod_id=prod_id, name=name, stock=stock, description=description)
        return await inventory.updateInventoryItem(item)
    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})

@mcp.tool()
async def update_inventory_item_stock(prod_id: int, stock: int):
    """
        Updates the new_stock quantity of an existing inventory item in the inventory management system.
        
        Args:
            prod_id: The ID of the inventory item to update.
            stock: The new new_stock quantity of the inventory item.
        
        Returns:
            A confirmation message or an error message in json format if the request fails.
    """

    try:
        item = models.InventoryItemUpdateStock(prod_id=prod_id, new_stock=stock)
        return await inventory.updateInventoryItemStock(item)

    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})


# Billing Tools
@mcp.tool()
async def fetch_bill_records():
    """
    Fetches the list of all bill records from the inventory management system server in json format.
    Each bill record contains it invoice_no, Date, total_price and paymethod.
    If total_price and paymethod are NULL then that bill is not issued (Products inside the bill are not sold).


    Returns:
        A list of bill records in json format, or an error message if the request fails.

    """

    return await bills.fetchBillRecords()

@mcp.tool()
async def fetch_bill_records_by_cashier(cashier_id: int):
    """
    Fetches the list of all bill records from the inventory management system server in json format.

    Args:
        cashier_id: Unique id of the cashier.

    Returns:
        A list of bill records created by this cashier in json format, or an error message if the request fails.

    """
    return await bills.fetchBillRecordsByCashier(cashier_id)

@mcp.tool()
async def open_bill(invoice_no: int):
    """
    Reads the products inside a bill with the provided invoice_no.

    Args:
        invoice_no: The Invoice No of the bill

    Returns:
        A list of products inside a bill with the provided invoice_no in a json format.

    """

    return await bills.openBill(invoice_no)

@mcp.tool()
async def create_draft_bill(products: list[dict[str, int]]):
    """
    Creates a draft bill and adds the provided products to it.

    Args:
        products: A list of products, each element of this list should be a python dictionary of the format:
                - prod_id: int, a unique identifier for the product (must be a positive value)
                - quantity: int, quantity of the product (must be a positive value and cannot be zero)

    Example Usage for LLM:
    User: "Create a bill for 2 units of product 101 and 5 units of product 102"
    LLM Input:
    {
        "products": [
            {"prod_id": 101, "quantity": 2},
            {"prod_id": 102, "quantity": 5}
        ]
    }

    Returns:
        A confirmation message or an error message in json format if the request fails.
    """

    try:
        draft_bill = models.DraftBill(**{"products": products})
        return await bills.createDraftBill(draft_bill)

    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})

@mcp.tool()
async def add_item_to_bill(invoice_no: int, prod_id: int, quantity: int):
    """
    Adds an item to the bill with the provided invoice_no.

    Args:
        invoice_no:
        prod_id:
        quantity:

    Returns:
        A confirmation message or an error message in json format if the request fails.

    """

    try:
        entry = models.BillItemAddOrUpdate(invoice_no=invoice_no, prod_id=prod_id, quantity=quantity)
        return await bills.addToExistingBill(entry)

    except ValidationError as e:
        logging.error(f"ValidationError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})


@mcp.tool()
async def edit_bill_item_quantity(invoice_no: int, prod_id: int, quantity: int):
    """
    Updates the quantity of an existing unpaid/unissued bill item in the inventory management system.
    Args:
        invoice_no: Invoice Number of the bill
        prod_id: int, a unique identifier for the product (must be a positive value)
        quantity: int, quantity of the product (must be a positive value and cannot be zero)

    Returns:
        A confirmation message or an error message in json format if the request fails.
    """

    try:
        entry = models.BillItemAddOrUpdate(invoice_no=invoice_no, prod_id=prod_id, quantity=quantity)
        return await bills.editProductQty(entry)

    except ValidationError as e:
        logging.error(f"ValidationError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})


@mcp.tool()
async def delete_bill_item(invoice_no: int, prod_id: int):
    """
    Deletes an existing item from an unpaid/unissued bill.

    Args:
        invoice_no: Invoice Number of the bill
        prod_id: Id of the product (must be a positive value)

    Returns:
        A confirmation message or an error message in json format if the request fails.

    """

    try:
        entry = models.BillItemDelete(invoice_no=invoice_no, prod_id=prod_id)
        return await bills.deleteBillItem(entry)

    except ValidationError as e:
        logging.error(f"ValidationError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})

@mcp.tool()
async def issue_bill(invoice_no: int, pay_method: str):
    """
    Issues a draft bill i.e. The bill is finalised and considered paid.
    After calling this tool, the bill cannot be edited or deleted.

    Args:
        invoice_no: Invoice Number of the bill
        pay_method: Payment Method in uppercase letters (e.g. Cash, Card, UPI)

    Returns:
        A confirmation message or an error message in json format if the request fails.

    """

    try:
        bill = models.IssueBill(invoice_no=invoice_no, pay_method=pay_method)
        return await bills.issueBill(bill)

    except ValidationError as e:
        logging.error(f"ValidationError occurred: {e}")
        return json.dumps({"error": f"ValueError occurred: {e}"})

@mcp.tool()
async def discard_bill(invoice_no: int):
    """
    Discards a draft Bill.

    Args:
        invoice_no: Invoice Number of the bill

    Returns:
        A confirmation message or an error message in json format if the request fails.
    """

    return await bills.discardBill(invoice_no)


if __name__ == "__main__":
    mcp.run(transport="stdio")