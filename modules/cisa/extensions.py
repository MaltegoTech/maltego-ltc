from maltego_trx.decorator_registry import TransformRegistry, TransformSet

cisa_registry = TransformRegistry(
    owner="Maltego Technologies GmbH",
    author="Carlos Fragoso <cf@maltego.com>",
    host_url="https://localhost:8080",
    seed_ids=["cisa"],
)
cisa_set = TransformSet("CISA", "CISA Transforms")
