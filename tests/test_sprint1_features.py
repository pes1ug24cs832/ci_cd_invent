import pytest
import json
import os
import tempfile
import logging
from src.inventory import Inventory
from src.product import Product


class TestSprint1Features:
    @pytest.fixture
    def inventory(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump({}, f)
            temp_file = f.name

        inventory = Inventory(temp_file)
        yield inventory
        os.unlink(temp_file)

    def test_inv_3_add_product_with_details(self, inventory):
        """Test INV-3: Add product with complete details"""
        product = Product(
            name="Test Product",
            sku="TEST001",
            price=29.99,
            quantity=100,
            category="Electronics",
            description="A test product for testing purposes",
        )

        result = inventory.add_product(product)
        assert result is True

        # Verify all details are saved
        saved_product = inventory.get_product("TEST001")
        assert saved_product["name"] == "Test Product"
        assert saved_product["category"] == "Electronics"
        assert saved_product["description"] == "A test product for testing purposes"
        assert saved_product["price"] == 29.99
        assert saved_product["quantity"] == 100

    def test_inv_9_view_all_products_with_stock(self, inventory):
        """Test INV-9: View all products with stock information"""
        # Add multiple products
        product1 = Product("Product 1", "P1", 10.0, 5, "Category A", "Desc 1")
        product2 = Product("Product 2", "P2", 20.0, 10, "Category B", "Desc 2")

        inventory.add_product(product1)
        inventory.add_product(product2)

        all_products = inventory.get_all_products()

        assert len(all_products) == 2
        assert all(isinstance(p, Product) for p in all_products)

        # Verify stock quantities are correct
        stock_quantities = [p.quantity for p in all_products]
        assert 5 in stock_quantities
        assert 10 in stock_quantities

    def test_inv_23_update_stock_quantity(self, inventory):
        """Test INV-23: Update stock quantity"""
        product = Product("Test Product", "TEST123", 15.0, 50, "Test")
        inventory.add_product(product)

        # Update stock
        result = inventory.update_stock("TEST123", 25)
        assert result is True

        # Verify update
        updated_product = inventory.get_product("TEST123")
        assert updated_product["quantity"] == 25

    def test_inv_23_update_stock_nonexistent_product(self, inventory):
        """Test INV-23: Update stock for non-existent product"""
        result = inventory.update_stock("NONEXISTENT", 100)
        assert result is False

    def test_inv_6_delete_product_with_confirmation(self, inventory):
        """Test INV-6: Delete product functionality"""
        product = Product("To Delete", "DEL001", 10.0, 5, "Test")
        inventory.add_product(product)

        # Verify product exists
        assert inventory.get_product("DEL001") is not None

        # Delete product
        result = inventory.delete_product("DEL001")
        assert result is True

        # Verify product is deleted
        assert inventory.get_product("DEL001") is None

    def test_inv_7_log_deletions(self, inventory, caplog):
        """Test INV-7: Log deletion actions"""
        # Setup logging capture
        with caplog.at_level(logging.INFO):
            product = Product("Log Test", "LOG001", 10.0, 5, "Test")
            inventory.add_product(product)
            inventory.delete_product("LOG001")

            # Check if deletion was logged
            assert "deleted" in caplog.text.lower()

    def test_inv_24_edit_product_details(self, inventory):
        """Test INV-24: Edit product details"""
        product = Product("Original", "EDIT001", 10.0, 5, "Old Category", "Old Desc")
        inventory.add_product(product)

        # Edit product details
        result = inventory.update_product_details(
            "EDIT001", "Updated Name", "New Category", 15.0, "New Description"
        )
        assert result is True

        # Verify updates
        updated = inventory.get_product("EDIT001")
        assert updated["name"] == "Updated Name"
        assert updated["category"] == "New Category"
        assert updated["price"] == 15.0
        assert updated["description"] == "New Description"
