from maltego_trx.decorator_registry import TransformRegistry, TransformSet

cms_seek_registry = TransformRegistry(
    owner="fhe@maltego.com",
    author="Maltego Technologies GmbH",
    host_url="https://localhost:8080",
    seed_ids=["cms_seek"],
)
cms_seek_set = TransformSet("cms_seek", "cms_seek Transforms")
