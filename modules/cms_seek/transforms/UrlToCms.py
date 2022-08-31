from maltego_trx.entities import Phrase, URL, Alias
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
# from parser import ParserError

from ..utils.cmseek_service import CMSeekService, CMSeekResult, WordPressCMSeekResult

from modules.cms_seek.extensions import cms_seek_registry, cms_seek_set


@cms_seek_registry.register_transform(display_name="UrlToCms", input_entity="maltego.URL",
                                      description='Runs CMSeeK for a given URL and returns CMS name and url',
                                      output_entities=["maltego.Phrase"],
                                      transform_set=cms_seek_set)
class UrlToCms(DiscoverableTransform):
    """
    Runs CMSeeK for a given URL and returns CMS name and url
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        url = request.Value

        try:
            cmseek_result: CMSeekResult = CMSeekService.run(url)
        except ValueError as e:
            response.addException(str(e))
            return

        if not cmseek_result:
            response.addException(f"Unexpected error processing url '{url}'")
            return

        if cmseek_result['cms_name'] == '':
            response.addUIMessage(f"No CMS found for url {url}")
            return

        name_entity = response.addEntity(Phrase, cmseek_result['cms_name'])
        name_entity.setLinkLabel(cmseek_result['detection_param'])

        response.addEntity(URL, cmseek_result['cms_url'])

        if cmseek_result['cms_id'] == 'wp':
            # CMSeeK has deep scanner for WordPress with additional properties
            cmseek_result: WordPressCMSeekResult

            for user in cmseek_result.get('wp_users', []):
                response.addEntity(Alias, user)

            if 'wp_version' in cmseek_result:
                name_entity.addProperty('wp_version', 'WordPress Version',
                                        value=cmseek_result['wp_version'])

            for plugin in cmseek_result.get('wp_plugins', []):
                plugin_entity = response.addEntity(Phrase, plugin)
                plugin_entity.setLinkLabel("uses plugin")

            if 'wp_uploads_directory' in cmseek_result:
                response.addEntity(URL, cmseek_result['wp_uploads_directory'])

            if 'wpvulndb_url' in cmseek_result:
                db_entity = response.addEntity(Phrase, cmseek_result['wpvulndb_url'])
                db_entity.setLinkLabel("database")
