import zipfile
import os
from maltego_trx.decorator_registry import TransformRegistry, TransformSet

class AtopCustomTransformsEntity(TransformRegistry):

    @staticmethod
    def add_entity_to_zip(zip_to_patch: zipfile, entity_dir: str):
        for entity_components in os.listdir(entity_dir):
            for dirpath, dirs, files in os.walk(os.path.join(entity_dir, entity_components)):
                for f in files:
                    fn = os.path.join(dirpath, f)
                    zip_to_patch.write(fn, fn.replace(entity_dir, "").replace(os.path.sep, "/"))

    def write_local_mtz(self,
        mtz_path: str = "./local.mtz",
        working_dir: str = ".",
        command: str = "python3",
        params: str = "project.py",
        debug: bool = True):

        super().write_local_mtz(mtz_path, working_dir, command, params, debug)

        entity_dir = os.path.join(os.path.dirname(mtz_path), "entities")
        if not os.path.exists(entity_dir):
            return False

        ## patch the extension mtz
        with zipfile.ZipFile(mtz_path, "a") as mtz:
            AtopCustomTransformsEntity.add_entity_to_zip(mtz, entity_dir)

        ## update the global mtz
        with zipfile.ZipFile("./local.mtz", "a") as mtz:
            AtopCustomTransformsEntity.add_entity_to_zip(mtz, entity_dir)


atop_registry = AtopCustomTransformsEntity(
    owner="giacomo@udontknow.us",
    author="aaarghhh",
    host_url="https://localhost:8080",
    seed_ids=["atop"],
)

atop_set = TransformSet("atop", "Atop Transforms")

#from modules.atop.settings import api_key_setting
#atop_registry.global_settings = [api_key_setting]
