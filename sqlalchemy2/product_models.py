# 1. Set up SQLAlchemy engin connecting to product_catalog.db (with echo=True)
from sqlalchemy import create_engine, String
from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Boolean
from typing import Optional
from sqlalchemy import inspect

engine = create_engine(
    "sqlite:///product_catalog.db",
    echo=True
)

class Base(DeclarativeBase):
    pass

# 2. Define two models:
    # Category: id (primary key), name (string, not null, unique), description (optional string)
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"
        
    # Product: id (primary key), name (string, not null), price (float, not null), in_stock (boolean, default True), category_name (string — just store the category name as text for now; we'll use proper foreign keys in the Relationships lesson)
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean,default=True)
    category_name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price}, "
            f"in_stock={self.in_stock}, "
            f"category_name='{self.category_name}')"
            )
    
# 3. Create the tables using Base.metadata.create_all(engine)
Base.metadata.create_all(engine)
print("\nTables created succesfully")

# 4. Use a session:
with Session(engine) as session:
    # Insert at least 3 categories 6 products across those categories
    category1 = Category(name="Electronics")
    category2 = Category(name="Apparel", description="Clothing, hats, shoes, and/or jewelry")
    category3 = Category(name="Travel")
    
    session.add_all([category1, category2, category3])

    # Insert at least 6 products across those categories
    product1 = Product(name="Computer", price=1500.00, in_stock=True, category_name="Electronics")
    product2 = Product(name="Coffee Maker", price=40.00, in_stock=True, category_name="Electronics")    
    product3 = Product(name="Dunks", price=200.00, in_stock=True, category_name="Apparel")
    product4 = Product(name="Melin Headwear", price=80.00, in_stock=True, category_name="Apparel")
    product5 = Product(name="Suitcase", price=200.00, in_stock=False, category_name="Travel")
    product6 = Product(name="Weekender", price=65.00, in_stock=True, category_name="Travel")

    session.add_all([product1, product2, product3, product4, product5, product6])
    
    session.commit()
    print(f"\nCreated: {category1}, {category2} and {category3}")
    print(f"\nCreated: {product1}, {product2}, {product3}, {product4}, {product5}, and {product6}")

# Query
with Session(engine) as session:
    # Query and print all categories
    print("\n=== All Categories ===")
    categories = session.query(Category).all()
    for category in categories:
        print(f"  {category}")

    # Query and print all products that are in stock
    print("\n=== All Products in Stock ===")
    products = session.query(Product).filter(Product.in_stock == True).all()
    for product in products:
        print(f"  {product}")

    # Query and print all products with a price under $50
    print("\n=== Products Under $50 ===")
    products = session.query(Product).filter(Product.price < 50).all()

    for product in products:
        print(f"  {product}")

inspector = inspect(engine)
print("Tables:", inspector.get_table_names())
for column in inspector.get_columns("products"):
    print(f"  {column['name']}: {column['type']} (nullable={column['nullable']})")