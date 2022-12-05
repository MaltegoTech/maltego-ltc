from maltego_trx.decorator_registry import TransformRegistry, TransformSet

punycode_registry = TransformRegistry(
    owner="fm@maltego.com",
    author="Maltego",
    host_url="https://localhost:8080",
    seed_ids=["punycode"],
)
punycode_set = TransformSet("punycode", "punycode Transforms")
