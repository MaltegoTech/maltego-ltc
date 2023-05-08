from maltego_trx.decorator_registry import TransformRegistry, TransformSet

web2screenshot_registry = TransformRegistry(
    owner="Mario Rojas (aka Turroks)",
    author="Mario Rojas",
    host_url="https://localhost:8080",
    seed_ids=["Web2Screenshot"],
)
web2screenshot_set = TransformSet("Web2Screenshot", "Web2Screenshot Transforms")
