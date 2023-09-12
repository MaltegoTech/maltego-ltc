import httpx, trio
from ghunt.apis.drive import DriveHttp
from ghunt.objects.base import GHuntCreds
from ghunt.helpers.drive import get_comments_from_file, get_users_from_file
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg, UIM_TYPES
from maltego_trx.transform import DiscoverableTransform
from modules.ghunt.extensions import ghunt_registry, ghunt_set
import re

error_messages = {
    "JSONDecodeError": "\nGoogle might be rate limiting your IP address"
}

# Extract folder or file id from url
def extract_id(url):
    # Define regex patterns for different URL formats
    patterns = [
        r'/folders/([a-zA-Z0-9_-]+)',
        r'/file/d/([a-zA-Z0-9_-]+)/',
        r'/files/([a-zA-Z0-9_-]+)'
    ]

    for pattern in patterns:
        result = re.search(pattern, url)
        if result:
            return result.group(1)

@ghunt_registry.register_transform(
    display_name="Google Drive to Details [ghunt]", 
    input_entity="maltego.URL",
    description='Returns details from ghunt results on a given google drive',
    settings=[],
    output_entities=["maltego.Unknown"],
    transform_set=ghunt_set
    )
class ghuntFromDrive(DiscoverableTransform):
    
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        async def main():
            url = request.Value
            file_id = extract_id(url)

            ghunt_creds = GHuntCreds()
            ghunt_creds.load_creds(silent=True) # Check creds (but it doesn't crash if they are invalid)

            as_client = httpx.AsyncClient() # Async client

            drive = DriveHttp(ghunt_creds)
            file_found, file = await drive.get_file(as_client, file_id)

            if file_found:

                # Extract file details
                if file.created_date:
                    created_date = response.addEntity("maltego.DateTime", file.created_date)
                    created_date.setLinkLabel("Created")
                
                if file.primary_domain_name:
                    response.addEntity("maltego.Domain", value = file.primary_domain_name)

                if file.organization_display_name:
                    response.addEntity("maltego.Organization", value = file.organization_display_name)

                if file.title:
                    response.addEntity("maltego.Phrase", value = file.title)

                if file.modified_date:
                    created_date = response.addEntity("maltego.DateTime", file.modified_date)
                    created_date.setLinkLabel("Modified")

                if file.md5_checksum:
                    response.addEntity("maltego.Hash", value = file.md5_checksum)

                for item in file.parents:
                    parent = response.addEntity("maltego.URL")
                    parent.addProperty("short-title", value = item.id)
                    parent.addProperty("url", value = item.parent_link)
                    parent.setLinkLabel("Parent")

                # Check if child items
                is_folder = file.mime_type == "application/vnd.google-apps.folder"
                if is_folder:
                    children_found, _, drive_childs = await drive.get_childs(as_client, file_id)

                    if children_found:
                        for item in drive_childs.items:
                            child = response.addEntity("maltego.URL")
                            child.addProperty("short-title", value = item.id)
                            child.addProperty("url", value = item.child_link)
                            child.setLinkLabel("Child")

                # Extract user data
                users = get_users_from_file(file)
                for user in users:
                    response.addEntity("maltego.EmailAddress", value = user.email_address)
                    person = response.addEntity("maltego.Person", value = user.name)
                    person.addProperty("role", value = user.role)
                    person.addProperty("gaia_id", value = user.gaia_id)

                # Display comments
                try:
                    comments = get_comments_from_file(file)                
                    for comment in comments['items']:
                        response.addEntity("maltego.Phrase", value = comment)
                except:
                    pass

            # Handle query errors
            else:
                response.addUIMessage("Drive not found", UIM_TYPES['partial'])

        trio.run(main) # running our async code in a non-async code