from maltego_trx.decorator_registry import TransformRegistry, TransformSet

wigle_registry = TransformRegistry(
    owner="Maltego Technologies GmbH",
    author="Carlos Fragoso <cf@maltego.com>",
    host_url="https://localhost:8080",
    seed_ids=["wigle"],
)
wigle_set = TransformSet("WIGLE", "WIGLE Transforms")
