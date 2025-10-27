#!/usr/bin/env python3
import click
import logging
from tabulate import tabulate
from src.inventory import Inventory
from src.product import Product

# Setup logging for deletions (INV-7)
logging.basicConfig(
    filename='logs/deletion.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@click.group()
def cli():
    """Command-line Inventory Management System - Sprint 1"""
    pass

# INV-3: Add product with details
@cli.command()
@click.option('--name', prompt='Product name', help='Name of the product')
@click.option('--sku', prompt='SKU', help='Stock Keeping Unit (unique)')
@click.option('--price', prompt='Price', type=float, help='Product price')
@click.option('--quantity', prompt='Quantity', type=int, help='Initial quantity')
@click.option('--category', prompt='Category', help='Product category')
@click.option('--description', prompt='Description', help='Product description')
def add_product(name, sku, price, quantity, category, description):
    """Add a new product with details (INV-3)"""
    inventory = Inventory()
    product = Product(name, sku, price, quantity, category, description)
    
    if inventory.add_product(product):
        click.echo(f"✅ Product '{name}' added successfully! (INV-21)")
    else:
        click.echo("❌ Failed to add product. SKU might already exist.")

# INV-9: View all products with stock
@cli.command()
def view_products():
    """View all products with stock information (INV-9)"""
    inventory = Inventory()
    products = inventory.get_all_products()
    
    if not products:
        click.echo("📭 No products in inventory.")
        return
    
    table_data = []
    for product in products:
        table_data.append([
            product.sku,
            product.name,
            product.category,
            f"${product.price:.2f}",
            product.quantity,
            product.description[:50] + "..." if len(product.description) > 50 else product.description
        ])
    
    headers = ["SKU", "Name", "Category", "Price", "Stock", "Description"]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    click.echo(f"\n📊 Total products: {len(products)}")

# INV-23: Update stock quantity
@cli.command()
@click.option('--sku', prompt='SKU of product to update', help='Product SKU')
@click.option('--quantity', prompt='New quantity', type=int, help='Updated stock quantity')
def update_stock(sku, quantity):
    """Update stock quantity for a product (INV-23)"""
    inventory = Inventory()
    
    if inventory.update_stock(sku, quantity):
        click.echo(f"📦 Stock for {sku} updated to {quantity}")
    else:
        click.echo(f"❌ Product with SKU {sku} not found")

# INV-6: Confirm before deletion
@cli.command()
@click.option('--sku', prompt='SKU of product to delete', help='Product SKU to delete')
def delete_product(sku):
    """Delete a product with confirmation (INV-6)"""
    inventory = Inventory()
    
    # Get product details for confirmation
    product = inventory.get_product(sku)
    if not product:
        click.echo(f"❌ Product with SKU {sku} not found")
        return
    
    # Display product details for confirmation
    click.echo("\n⚠️  PRODUCT TO DELETE:")
    click.echo(f"   SKU: {sku}")
    click.echo(f"   Name: {product['name']}")
    click.echo(f"   Category: {product['category']}")
    click.echo(f"   Current Stock: {product['quantity']}")
    
    # Confirmation prompt (INV-6)
    if click.confirm('❌ Are you sure you want to delete this product?'):
        if inventory.delete_product(sku):
            # Log the deletion (INV-7)
            logging.info(f"Product deleted - SKU: {sku}, Name: {product['name']}")
            click.echo(f"✅ Product {sku} deleted successfully")
        else:
            click.echo("❌ Failed to delete product")
    else:
        click.echo("✅ Deletion cancelled")

# INV-24: Edit product details
@cli.command()
@click.option('--sku', prompt='SKU of product to edit', help='Product SKU')
def edit_product(sku):
    """Edit product details (INV-24)"""
    inventory = Inventory()
    
    product = inventory.get_product(sku)
    if not product:
        click.echo(f"❌ Product with SKU {sku} not found")
        return
    
    # Display current details
    click.echo("\n📝 Current Product Details:")
    click.echo(f"   SKU: {sku}")
    click.echo(f"   Name: {product['name']}")
    click.echo(f"   Category: {product['category']}")
    click.echo(f"   Price: ${product['price']:.2f}")
    click.echo(f"   Stock: {product['quantity']}")
    click.echo(f"   Description: {product['description']}")
    
    # Edit options
    click.echo("\n📝 Edit Product Details:")
    new_name = click.prompt("New name", default=product['name'])
    new_category = click.prompt("New category", default=product['category'])
    new_price = click.prompt("New price", type=float, default=product['price'])
    new_description = click.prompt("New description", default=product['description'])
    
    if inventory.update_product_details(sku, new_name, new_category, new_price, new_description):
        click.echo(f"✅ Product {sku} updated successfully")
    else:
        click.echo("❌ Failed to update product")

if __name__ == '__main__':
    cli()