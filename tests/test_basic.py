def test_basic_math():
    """Basic test to verify CI is working"""
    assert 1 + 1 == 2

def test_imports():
    """Test that main modules can be imported"""
    try:
        from src.inventory import Inventory
        from src.product import Product
        assert True
    except ImportError as e:
        assert False, f"Import error: {e}"

def test_inventory_creation():
    """Test Inventory class creation"""
    from src.inventory import Inventory
    # Use a valid file path instead of ":memory:"
    inventory = Inventory("test_inventory.json")
    assert inventory is not None
    # Clean up
    import os
    if os.path.exists("test_inventory.json"):
        os.remove("test_inventory.json")

def test_product_creation():
    """Test Product class creation"""
    from src.product import Product
    product = Product("Test Product", "TEST123", 10.0, 5)
    assert product.name == "Test Product"
    assert product.sku == "TEST123"