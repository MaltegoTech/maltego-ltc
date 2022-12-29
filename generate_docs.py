#!python
from maltego_trx.decorator_registry import TransformMeta

from project import registry as meta_registry

if __name__ == '__main__':
    for module, reg in meta_registry.registries.items():

        header = (
            f"# {module} Module\n"
            f"\n"
            f"**Author:** {reg.author}\n"
            f"<br/>\n"
            f"**Owner:** {reg.owner}"
        )

        txt = header

        txt += "\n\n---\n\n"

        txt += "## Transforms \n\n"

        meta: TransformMeta
        for meta in reg.transform_metas.values():
            txt += f"### {meta.display_name}\n\n"
            txt += meta.description + "\n\n"

            txt += f"`{meta.input_entity} --> {', '.join(meta.output_entities)}`"
            txt += "\n\n---\n\n"

        with open(f"./docs/{module}.md", "w+") as docs_md:
            docs_md.write(txt)
