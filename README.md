# InventorySystem MCP Server

A Python based **MCP (Model Context Protocol) Server** that connects to an Inventory Management System and provides various tools to handle CRUD operations to it.

This is a simple side project I tried myself for fun to try enable AI compatibility to one of our college miniprojects.

## What this MCP Server does

- Serves as an Interface between InventorySystem Server and MCP Client (eg: Claude)
- Provides 15 MCP tools to conduct CRUD operations on Inventory Management System Database.
    - Create and Read Registered Users.
    - Create, Update and Read Inventory Items.
    - Create, Read, Update and Delete Bills.
- Uses Pydantic to validate data inputs given by LLM before passing to main server.
- Logs server logs for easy debugging.


### Tools

Below are the tools that this MCP server provides.

| S.No | Tool                            | Description                                          |
|------|---------------------------------|------------------------------------------------------|
| 1    | `fetch_users`                   | Reads all the Users Registered to System             |
| 2    | `add_user`                      | Adds a New User to the System                        |
| 3    | `fetch_inventory_items`         | Reads all the Items Stored in the Inventory          |
| 4    | `add_inventory_item`            | Adds a New Item to the Inventory                     |
| 5    | `update_inventory_item`         | Updates Details of an Item in Inventory              |
| 6    | `update_inventory_item_stock`   | Updates only the Stock of an Item in Inventory       |
| 7    | `fetch_bill_records`            | Reads all the Bills Created in the System            |
| 8    | `fetch_bill_records_by_cashier` | Reads the Bills Filtered by Cashier who created them |
| 9    | `open_bill`                     | Reads the Item Entries in a Bill                     |
| 10   | `create_bill`                   | Creates a New Bill by the Product Id and Stock       |
| 11   | `issue_bill`                    | Issues a Bill (Bill is Paid)                         |
| 12   | `discard_bill`                  | Discards a Draft Bill (Unpaid Bill)                  |
| 13   | `add_item_to_bill`              | Adds a new Item to a bill.                           |
| 14   | `edit_bill_item_quantity`       | Changes the Quantity of a Item entry in a Bill       |
| 15   | `delete_bill_item`              | Deletes the Item entry from the bill                 |


## How to Setup this MCP Server

### Prerequisites
- Python 3.8 or higher
- uv (Python package manager for MCP servers)
- XAMPP Apache Server with [InventorySystem](https://github.com/AllanSJoseph/InventorySystem) server set up correctly.
- An MCP client that supports MCP servers eg: Claude Desktop, Cursor, WindSurf, etc.
- [Optional] Node.js (for inspecting the MCP server)

### Setup InventorySystem Main Server
1. Install XAMPP from [XAMPP Official Site](https://www.apachefriends.org/download.html)
2. Make sure Apache and MySQL (MariaDB) services are running
3. Navigate to htdocs folder (Location where XAMPP is installed eg: ```C://xampp/htdocs```)
4. Make a new directory invmgmt (or name of your choice)
```shell
mkdir invmgmt
cd invmgmt
```
5. Clone the ```mcp``` branch from InventorySystem Repository on this folder
```shell
git clone -b mcp --single-branch https://github.com/AllanSJoseph/InventorySystem.git
```

### Setup MCP Server

#### Setup uv

For Windows users:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For Linux/Mac users (Note: This server is ran and tested on Windows):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Install Project Dependencies

1. Clone this repository
2. Open the directory in terminal
3. Install the required dependencies using uv
   ```shell
   uv sync
   ```


1. Open an MCP Client (here I am using Claude Desktop).
2. Go To Claude Settings ```Ctrl + ,```.
3. Go to the Developer tab.
4. Click on ```Edit Config``` under Local MCP Servers.
5. It highlights the ```claude_desktop_config.json``` file, Open it in your favourite text editor.
6. Add the below code to the ```mcp_servers``` list in the JSON file save and close.

```json
"mcpServers": {
        "inventory_mgmt_mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "your_project_directory_path",
                "run",
                "main.py"
            ]
        }
    }
```
7. Restart Claude Desktop
8. Open a new chat and click on tools button on the chat box and you will see the **documentation** tool available.
9. Try a prompt like below:
```plaintext
Could you list the users that are registered to Inventory Management System.
```
10. The LLM will use the `fetch_users` tool to search for the answer and return it in the chat. If it askes for permission click on *Allow always*. 

Please Note that free version of Claude has a limitation of number of tokens or characters, so it may not give results as desired and can sometimes give you an error of exceeding the token limit. You can try with a paid version of Claude or use other MCP clients like Cursor, WindSurf, etc.

Refer the official MCP Documentation from Antropic for more details on how to setup MCP servers in your client [For Server Developers - Model Context Protocol](https://modelcontextprotocol.io/quickstart/server#python)


## Sample Prompts to try with Claude

#### Add a Demo User

```plaintext
Could you add a demo user with a name of your choice and details of your choice, user must be a Cashier.
```

#### Add a Product

```plaintext
Could you add the below product to the Inventory Server.
AMUL MILK with stock 200 and price 20. Add a description of your choice.
```

#### Create a bill and issue it

```plaintext
Could you create a bill with the items 2 units of product id 1, 5 units of product id 21 and 3 units of product id 5, Issue the bill with payment method 'UPI'
```
**Note:** These products should be already in the inventory management main server. The database won't have any items just after setup.


## Checking the logs

In the project root directory find ```serverlogs.log```, which will contain the logs. It is ignored in git but it will be created when server is up.


## Inspect this MCP Server

To inspect the tools and check if tools are working properly, run the below command in terminal on the project directory.

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

[![Verified on MSeeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/a851f18a-ddf2-4c48-b972-b7ffb78bd47b)
