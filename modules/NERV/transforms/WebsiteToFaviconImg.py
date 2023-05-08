from maltego_trx.entities import Website, Image
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_FATAL

from maltego_trx.transform import DiscoverableTransform

from modules.NERV.extensions import NERV_registry, NERV_set

import bs4
import requests
from urllib.parse import urlparse

from modules.NERV.utils.InternetInteraction import Downloader


@NERV_registry.register_transform(display_name="To Favicon", input_entity=Website,
                                  description='Outputs the favicon of this website as an Image Entity.',
                                  output_entities=[Image],
                                  transform_set=NERV_set)
class WebsiteToFaviconImg(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        try:
            link_favicon = cls.get_favicon_url(website)
        except Exception as e:
            response.addUIMessage("Error getting the favicon hash, see logs.{}".format(e), messageType=UIM_FATAL)
            raise e
        ent = response.addEntity(Image, "favicon")
        ent.addProperty(displayName="URL", fieldName="url", matchingRule="strict", value=link_favicon)

    @classmethod
    def get_favicon_url(cls, website):
        # <link rel="shortcut icon" href="http://www.example.com/myicon.ico" />
        soup = Downloader.get_page_source(f"http://{website}")
        icons_link_list = list()
        icons_link_list.append(soup.find("link", rel="shortcut icon"))
        icons_link_list.append(soup.find("link", rel="icon"))
        for link in icons_link_list:
            if link is not None:
                # check the link is not relative
                link_to_favicon = link.attrs["href"]
                if urlparse(link_to_favicon).netloc == '':
                    link_to_favicon = f"http://{website}/{link_to_favicon}"
                return link_to_favicon

        google_favicon = f"http://www.google.com/s2/favicons?domain={website}"
        resp = requests.get(google_favicon)
        if resp.status_code == 200:
            return google_favicon

        github_favicon = f"https://favicons.githubusercontent.com/{website}"
        resp = requests.get(github_favicon)
        if resp.status_code == 200:
            return github_favicon

        # if we couldn't find it, we do it the old fashioned way
        return f"http://{website}/favicon.ico"

if __name__ == '__main__':
    ee = WebsiteToFaviconImg.get_favicon_url('www.github.com')
    print(ee)