import json
import os

from app import create_app, db
from app.models import Build, Category, Component, GPU, RAM, User


def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()

        categories = {}
        for name in ["CPU", "GPU", "Motherboard", "RAM", "Storage", "PSU", "Case"]:
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(
                    name=name,
                    slug=name.lower(),
                    description=f"Computer {name} components",
                )
                db.session.add(category)
                db.session.flush()
            categories[name] = category

        json_path = os.path.join(os.path.dirname(__file__), "../data/components.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as handle:
                parts = json.load(handle)
            for part in parts:
                existing_component = Component.query.filter_by(name=part["name"]).first()
                if existing_component:
                    if "image_url" in part:
                        existing_component.image_url = part.get("image_url")
                    continue
                category = categories.get(part["category"])
                if not category:
                    continue
                db.session.add(
                    Component(
                        name=part["name"],
                        brand=part["brand"],
                        price=part["price"],
                        socket=part.get("socket"),
                        image_url=part.get("image_url"),
                        category_id=category.id,
                    )
                )

        gpu_seed_data = [
            {
                "name": "NVIDIA GeForce RTX 4070",
                "brand": "NVIDIA",
                "price": 599.99,
                "specs": {"memory": "12GB", "boost_clock": "2475 MHz"},
                "vram": "12GB",
                "image_url": "/images/rtx-4070.webp",
            },
            {
                "name": "AMD Radeon RX 7800 XT",
                "brand": "AMD",
                "price": 499.99,
                "specs": {"memory": "16GB", "boost_clock": "2430 MHz"},
                "vram": "16GB",
                "image_url": "/images/rx-7800xt.png",
            },
        ]
        for gpu_data in gpu_seed_data:
            gpu = GPU.query.filter_by(name=gpu_data["name"]).first()
            if gpu:
                gpu.image_url = gpu_data["image_url"]
            else:
                db.session.add(GPU(**gpu_data))

        ram_seed_data = [
            {
                "name": "Corsair Vengeance LPX",
                "brand": "Corsair",
                "price": 89.99,
                "specs": {"type": "DDR4", "speed": "3200MHz"},
                "capacity": "16GB",
                "speed": "3200MHz",
                "image_url": "/images/vengeance-lpx.png",
            },
            {
                "name": "G.Skill Trident Z5",
                "brand": "G.Skill",
                "price": 129.99,
                "specs": {"type": "DDR5", "speed": "6000MHz"},
                "capacity": "32GB",
                "speed": "6000MHz",
                "image_url": "/images/trident-z5.webp",
            },
        ]
        for ram_data in ram_seed_data:
            ram = RAM.query.filter_by(name=ram_data["name"]).first()
            if ram:
                ram.image_url = ram_data["image_url"]
            else:
                db.session.add(RAM(**ram_data))

        demo_user = User.query.filter_by(username="demo").first()
        if not demo_user:
            demo_user = User(username="demo", email="demo@pcbuilder.local")
            demo_user.set_password("password123")
            db.session.add(demo_user)
            db.session.flush()
        demo_user.email = "demo@pcbuilder.local"
        demo_user.set_password("password123")

        if not Build.query.filter_by(user_id=demo_user.id, name="Starter Build").first():
            build = Build(user_id=demo_user.id, name="Starter Build", total_price=0.0)
            db.session.add(build)
            db.session.flush()
            starter_component = Component.query.first()
            if starter_component:
                build.components.append(starter_component)
                build.total_price = float(starter_component.price or 0)

        db.session.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
