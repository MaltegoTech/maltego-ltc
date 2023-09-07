import httpx, trio
from ghunt.apis.peoplepa import PeoplePaHttp
from ghunt.objects.base import GHuntCreds
from ghunt.helpers import gmaps
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg, UIM_TYPES
from maltego_trx.transform import DiscoverableTransform

from modules.ghunt.extensions import ghunt_registry, ghunt_set

error_messages = {
    "JSONDecodeError": "\nGoogle might be rate limiting your IP address"
}

@ghunt_registry.register_transform(
    display_name="Gmail address to Details [ghunt]", 
    input_entity="maltego.EmailAddress",
    description='Returns details from ghunt results on a given gmail address',
    settings=[],
    output_entities=["maltego.Unknown"],
    transform_set=ghunt_set
    )
class ghuntFromEmail(DiscoverableTransform):
    
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        async def main():
            email = request.Value

            ghunt_creds = GHuntCreds()
            ghunt_creds.load_creds(silent=True) # Check creds (but it doesn't crash if they are invalid)

            as_client = httpx.AsyncClient() # Async client

            people_api = PeoplePaHttp(ghunt_creds)
            found, person = await people_api.people_lookup(as_client, email, params_template="max_details")
                                                                            # You can have multiple "params_template" for the GHunt APIs,
                                                                            # for example, on this endpoint, you have "just_gaia_id" by default,
                                                                            # "just_name" or "max_details" which is used in the email CLI module.

            if found:

                # Name
                if "PROFILE" in person.names:
                    name = response.addEntity("maltego.Person", value = person.names["PROFILE"].fullname)
                    name.addProperty("firstname", value = person.names["PROFILE"].firstName)
                    name.addProperty("lastname", value = person.names["PROFILE"].lastName)

                # Profile Photo
                if "PROFILE" in person.profilePhotos and person.profilePhotos['PROFILE'].isDefault == False:
                    profile_photo = response.addEntity("maltego.Image")
                    profile_photo.addProperty("description", value = person.profilePhotos["PROFILE"].flathash)
                    profile_photo.addProperty("url", value = person.profilePhotos["PROFILE"].url)
                    profile_photo.setLinkLabel("Profile")

                # Cover Photo
                if "PROFILE" in person.coverPhotos and person.coverPhotos['PROFILE'].isDefault == False:
                    profile_photo = response.addEntity("maltego.Image")
                    profile_photo.addProperty("description", value = person.coverPhotos["PROFILE"].flathash)
                    profile_photo.addProperty("url", value = person.coverPhotos["PROFILE"].url)
                    profile_photo.setLinkLabel("Cover")

                # Enabled applications
                if "PROFILE" in person.inAppReachability:

                    for a in person.inAppReachability["PROFILE"].apps:
                        app = response.addEntity("maltego.Service", value = a)
                        app.addProperty("banner", value = "Google App")

                # Reviews
                try:
                    err, stats, reviews, photos = await gmaps.get_reviews(as_client, person.personId)
                    if reviews:
                        for r in reviews:
                            organization = response.addEntity("maltego.Organization", value = r.location.name)
                            organization.additionalFields.append(["rating", "Rating", '', str(r.rating) + "/5"])
                            organization.additionalFields.append(["address", "Address", '', r.location.address])
                            organization.additionalFields.append(["type", "Type", '', r.location.types])
                            organization.additionalFields.append(["tags", "Tags", '', r.location.tags])
                            organization.additionalFields.append(["comment", "Comment", '', r.comment])
                            organization.additionalFields.append(["latitude", "Latitude", '', r.location.position.latitude])
                            organization.additionalFields.append(["longitude", "Longitude", '', r.location.position.longitude])
                except Exception as e:
                   error_type = type(e).__name__
                   error_message = f"{error_type}: {e}"
                   if error_type in error_messages:
                       error_message += error_messages[error_type]
                   response.addUIMessage(error_message, UIM_TYPES['partial'] )

            # Handle query errors
            else:
                response.addUIMessage("Email address not found", UIM_TYPES['partial'])

        trio.run(main) # running our async code in a non-async code