from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from extensions import registry

from modules.holehe.extensions import holehe_registry, holehe_set


@holehe_registry.register_transform(display_name="Email to Alias [HOLEHE]", input_entity="maltego.EmailAddress",
                             description='Extracts the alias from an Email Address',
                             settings=[],
                             output_entities=["maltego.Alias"],
                             transform_set = holehe_set)
class EmailToAlias(DiscoverableTransform):
    """
    Extracts the alias from an Email Address
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        email = request.Value
        alias = str(email).split("@", 1)[0]
        response.addEntity("maltego.Alias", alias)
