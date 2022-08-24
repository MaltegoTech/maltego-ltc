from meta_registry import MetaRegistry
from modules.IOCparser.extensions import iocparser_registry
from modules.cisa.extensions import cisa_registry
from modules.cms_seek.extensions import cms_seek_registry

from modules.dnstwist.extensions import dnstwist_registry

registry = MetaRegistry()
registry.include_registry("cisa", cisa_registry)
registry.include_registry("iocparser", iocparser_registry)
registry.include_registry("cms_seek", cms_seek_registry)

registry.include_registry("dnstwist", dnstwist_registry)


# The rest of these attributes are optional

# metadata
registry.version = "0.1"

# global settings
# from maltego_trx.template_dir.settings import api_key_setting
# registry.global_settings = [api_key_setting]

# transform suffix to indicate datasource
# registry.display_name_suffix = " [ACME]"

# reference OAuth settings
# registry.oauth_settings_id = ['github-oauth']
