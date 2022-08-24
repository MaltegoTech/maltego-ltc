from maltego_trx.decorator_registry import TransformRegistry, TransformSet

dnstwist_registry = TransformRegistry(
    owner="dw",
    author="TURROKS",
    host_url="https://localhost:8080",
    seed_ids=["dnstwist"],
)
dnstwist_set = TransformSet("dnstwist", "dnstwist Transforms")
