from datetime import datetime as dt
import os
from urllib import parse

from dotenv import load_dotenv
import requests

from extensions import registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.overlays import OverlayType, OverlayPosition

from modules.Web2Screenshot.extensions import web2screenshot_registry, web2screenshot_set

# Load Environment Variables
load_dotenv()


def api_handler(api_url, target_url, api, custom_agent):

    data = requests.get(api_url+f"?access_key={api}&url={target_url}&user_agent={custom_agent}")

    if data.status_code == 200:
        return data.url
    else:
        return


def api_info(api):

    data = requests.get(f"https://api.apiflash.com/v1/urltoimage/quota?access_key={api}")
    parsed = data.json()

    if data.status_code == 200:
        return parsed


@web2screenshot_registry.register_transform(display_name="To Screenshot - Cache [API Flash]",
                                            input_entity="maltego.URL",
                                            description='Take a cache screenshot from an URL, will consume 1 credit if'
                                                        ' not available in cache.',
                                            output_entities=["maltego.Image"],
                                            transform_set=web2screenshot_set)
class URLtoScreenshotCache(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        # Access Environment Variables
        api_key = os.getenv("API_KEY")
        user_agent = os.getenv("USER_AGENT")
        api_baseurl = os.getenv("API_URL")

        input_url = request.getProperty(key='theurl')
        clean_url = parse.quote_plus(input_url)

        screenshot = api_handler(api_url=api_baseurl, target_url=clean_url, api=api_key, custom_agent=user_agent)
        api_check = api_info(api=api_key)

        if screenshot:
            ent = response.addEntity("maltego.Image", str(input_url).lower())
            ent.addProperty("url", "URL", "strict", screenshot)
            ent.addProperty(fieldName="captureType", displayName="Capture Type", matchingRule='strict', value="Cache")
            ent.addProperty(fieldName="captureSize", displayName="Capture Size", matchingRule='strict', value="Standard")
            ent.addOverlay("#fcba03", OverlayPosition.NORTH_WEST, OverlayType.COLOUR)
            ent.addDisplayInformation(content=f'<a href="{screenshot}">Open in Browser</a>', title="Screenshot")
            response.addUIMessage(f"API Flash Transform runs: {api_check.get('remaining')} of {api_check.get('limit')} "
                                  f"credits remaining. Current quota period ends at "
                                  f"{dt.fromtimestamp(api_check.get('reset'))}")
