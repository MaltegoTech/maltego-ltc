from maltego_trx.decorator_registry import TransformRegistry, TransformSet

nmap_registry = TransformRegistry(
    owner="mg@maltego.com",
    author="Mathieu Gaucheler",
    host_url="https://localhost:8080",
    seed_ids=["nmap"],
)
nmap_set = TransformSet("nmap", "nmap Transforms")
