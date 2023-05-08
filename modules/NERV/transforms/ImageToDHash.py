from maltego_trx.entities import Hash, Image
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.NERV.extensions import NERV_registry, NERV_set

from modules.NERV.utils.ImageHasher import ImageHasher, get_url_from_image_entity


@NERV_registry.register_transform(display_name="To dHash (difference)", input_entity=Image,
                                  description="Returns the difference hash of an image (the image will be downloaded if"
                                              " not stored locally).",
                                  output_entities=[Hash],
                                  transform_set=NERV_set)
class ImageToDHash(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        url_image = get_url_from_image_entity(request)
        pHash = ImageHasher(url_image).get_dhash()
        ent = response.addEntity(Hash, pHash)
        ent.addProperty(fieldName="type", displayName="Hash Type", value="difference hash", matchingRule="strict")
