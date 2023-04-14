from maltego_trx.entities import Image, URL
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_PARTIAL, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.NERV.extensions import NERV_registry, NERV_set
from modules.NERV.utils.InternetInteraction import Downloader

from urllib.parse import urlparse


@NERV_registry.register_transform(display_name="To images", input_entity=URL,
                                  description="Returns the images on a webpage.",
                                  output_entities=[Image],
                                  transform_set=NERV_set)
class URLtoImages(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        page_url = request.Value
        for link in cls.get_images(page_url):
            try:
                path_img = urlparse(link).path
                filename = path_img.rsplit("/", maxsplit=1)[-1]
                ent = response.addEntity(Image, filename)
                ent.addProperty(fieldName="url", displayName="URL", matchingRule="strict", value=link)
            except Exception:
                response.addUIMessage(message=f"We detected a URL that we thought was an image but coulnd't parse it: {link}", messageType=UIM_PARTIAL)

    @classmethod
    def get_images(cls, page_url):
        img_list = set()
        netloc = urlparse(page_url).netloc
        soup = Downloader.get_page_source(page_url)
        for elem in soup.findAll("img"):
            img_url = elem.attrs["src"]
            if not img_url:
                continue
            else:
                img_url = urlparse(img_url)
                if img_url.netloc == "":
                    img_url = img_url._replace(netloc="github.com")
                if img_url.scheme == "":
                    img_url = img_url._replace(scheme="http")

            img_list.add(img_url.geturl())
        return img_list


if __name__ == '__main__':
    TEST_URL = "https://www.liberation.fr/international/moyen-orient/ou-en-est-la-revolte-en-iran-un-feu-qui-couve-sous-les-cendres-20230330_Q67IT67AYJG4FMF3N5WD2ATK6E/"
    TEST_URL = "https://therecord.media/3cx-attack-north-korea-lazarus-group"
    TEST_URL = "https://github.com/MaltegoTech/maltego-ltc/blob/main/docs/nmap.md"
    print(URLtoImages.get_images(TEST_URL))