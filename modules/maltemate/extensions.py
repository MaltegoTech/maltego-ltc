from maltego_trx.decorator_registry import TransformRegistry, TransformSet

maltemate_registry = TransformRegistry(
    owner="Maltego Technologies GmbH",
    author="Carlos Fragoso <cf@maltego.com>",
    host_url="https://localhost:8080",
    seed_ids=["maltemate"],
)
maltemate_set = TransformSet("Maltemate", "Maltemate Transforms")
