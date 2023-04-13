from maltego_trx.decorator_registry import TransformRegistry, TransformSet

NERV_registry = TransformRegistry(
    owner="shibasec@gmail.com",
    author="Maltego",
    host_url="https://localhost:8080",
    seed_ids=["NERV"],
)
NERV_set = TransformSet("NERV", "NERV Transforms")
