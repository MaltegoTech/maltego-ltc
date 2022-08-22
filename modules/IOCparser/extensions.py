from maltego_trx.decorator_registry import TransformRegistry, TransformSet

iocparser_registry = TransformRegistry(
    owner="Maltego Technologies GmbH",
    author="Florian Murschetz <fm@maltego.com>",
    host_url="https://localhost:8080",
    seed_ids=["iocparser"],
)
iocparser_set = TransformSet("IOC", "IoC Parser Transforms")
