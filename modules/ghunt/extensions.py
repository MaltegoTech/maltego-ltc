from maltego_trx.decorator_registry import TransformRegistry, TransformSet

ghunt_registry = TransformRegistry(
    owner="kodamaChameleon",
    author="Kodama <contact@kodamachameleon.com>",
    host_url="https://localhost:8080",
    seed_ids=["ghunt"],
)
ghunt_set = TransformSet("ghunt", "ghunt Transforms")
