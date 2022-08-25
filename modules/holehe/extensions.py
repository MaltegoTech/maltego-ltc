from maltego_trx.decorator_registry import TransformRegistry, TransformSet

holehe_registry = TransformRegistry(
    owner="dw",
    author="TURROKS",
    host_url="https://localhost:8080",
    seed_ids=["holehe"],
)
holehe_set = TransformSet("holehe", "holehe Transforms")
