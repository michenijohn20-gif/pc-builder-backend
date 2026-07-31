def serialize_component(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "brand": obj.brand,
        "price": obj.price,
        "socket": obj.socket,
        "image_url": obj.image_url,
        "category": obj.category.name if getattr(obj, "category", None) else None,
    }


def serialize_gpu(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "brand": obj.brand,
        "price": obj.price,
        "specs": obj.specs or {},
        "vram": obj.vram,
        "image_url": obj.image_url,
    }


def serialize_ram(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "brand": obj.brand,
        "price": obj.price,
        "socket": (obj.specs or {}).get("type"),
        "specs": obj.specs or {},
        "capacity": obj.capacity,
        "speed": obj.speed,
        "image_url": obj.image_url,
    }