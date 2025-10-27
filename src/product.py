class Product:
    def __init__(self, name: str, sku: str, price: float, quantity: int, 
                 category: str = "General", description: str = "", supplier: str = ""):
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity
        self.category = category
        self.description = description
        self.supplier = supplier
        
        # Validate data
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if not sku.strip():
            raise ValueError("SKU cannot be empty")