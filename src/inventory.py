import json
import os
import logging
from typing import List, Optional, Dict

class Inventory:
    def __init__(self, data_file: str = "data/inventory.json"):
        self.data_file = data_file
        self._ensure_data_dir()
        self.products = self._load_data()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    
    def _load_data(self) -> Dict:
        """Load inventory data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_data(self):
        """Save inventory data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.products, f, indent=2)
            return True
        except IOError:
            return False
    
    def add_product(self, product) -> bool:
        """Add a new product to inventory"""
        if product.sku in self.products:
            return False
        
        self.products[product.sku] = {
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'category': product.category,
            'description': product.description,
            'supplier': getattr(product, 'supplier', '')
        }
        return self._save_data()
    
    def get_product(self, sku: str) -> Optional[Dict]:
        """Get product by SKU"""
        return self.products.get(sku)
    
    def get_all_products(self) -> List:
        """Get all products with stock"""
        from .product import Product
        products = []
        for sku, product_data in self.products.items():
            products.append(Product(
                name=product_data['name'],
                sku=sku,
                price=product_data['price'],
                quantity=product_data['quantity'],
                category=product_data.get('category', ''),
                description=product_data.get('description', ''),
                supplier=product_data.get('supplier', '')
            ))
        return products
    
    def update_stock(self, sku: str, quantity: int) -> bool:
        """Update product stock quantity"""
        if sku in self.products:
            self.products[sku]['quantity'] = quantity
            return self._save_data()
        return False
    
    def delete_product(self, sku: str) -> bool:
        """Delete a product from inventory"""
        if sku in self.products:
            del self.products[sku]
            # Log deletion
            logging.info(f"Product deleted - SKU: {sku}")
            return self._save_data()
        return False
    
    def update_product_details(self, sku: str, name: str, category: str, price: float, description: str) -> bool:
        """Update product details"""
        if sku in self.products:
            self.products[sku]['name'] = name
            self.products[sku]['category'] = category
            self.products[sku]['price'] = price
            self.products[sku]['description'] = description
            return self._save_data()
        return False