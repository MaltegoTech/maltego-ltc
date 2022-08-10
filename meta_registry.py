import zipfile
from itertools import chain

from maltego_trx.decorator_registry import (
    TransformRegistry,
    TRANSFORMS_CSV_HEADER,
    SETTINGS_CSV_HEADER,
)
from maltego_trx.protocol.mtz import create_local_server_xml
from maltego_trx.utils import export_as_csv, serialize_xml


class MetaRegistry:
    registries: dict[str, TransformRegistry]

    def __init__(self):
        self.registries = {}

    def include_registry(self, namespace: str, registry: TransformRegistry):
        self.registries[namespace] = registry

    def write_transforms_config(
        self, config_path: str = "./transforms.csv", csv_line_limit: int = 100
    ):
        csv_lines = chain.from_iterable(
            registry._create_transforms_config()
            for registry in self.registries.values()
        )

        export_as_csv(
            TRANSFORMS_CSV_HEADER, tuple(csv_lines), config_path, csv_line_limit
        )

    def write_settings_config(
        self, config_path: str = "./settings.csv", csv_line_limit: int = 100
    ):
        """Exports the collected settings metadata as a csv-file to config_path"""

        csv_lines = chain.from_iterable(
            registry._create_settings_config() for registry in self.registries.values()
        )

        export_as_csv(
            SETTINGS_CSV_HEADER, tuple(csv_lines), config_path, csv_line_limit
        )

    def write_local_mtz(
        self,
        mtz_path: str = "./local.mtz",
        working_dir: str = ".",
        command: str = "python3",
        params: str = "project.py",
        debug: bool = True,
    ):
        transform_meta_names = chain.from_iterable(
            registry.transform_metas.keys() for registry in self.registries.values()
        )
        server_xml = create_local_server_xml(transform_meta_names)
        server_xml_str = serialize_xml(server_xml)

        with zipfile.ZipFile(mtz_path, "w") as mtz:
            mtz.writestr("Servers/Local.tas", server_xml_str)

            mtz_content = chain.from_iterable(
                registry._create_local_mtz(working_dir, command, params, debug)
                for registry in self.registries.values()
            )

            for path, content in mtz_content:
                if path == "Servers/Local.tas":
                    continue

                mtz.writestr(path, content)
