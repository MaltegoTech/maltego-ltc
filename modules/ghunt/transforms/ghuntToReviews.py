import trio, geocoder
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from maltego_trx.transform import DiscoverableTransform

from modules.ghunt.extensions import ghunt_registry, ghunt_set

@ghunt_registry.register_transform(
    display_name="Ghunt reviews to details [ghunt]", 
    input_entity="maltego.Organization",
    description='Expands dynamically added ghunt organization details into separate entities.',
    settings=[],
    output_entities=["maltego.Unknown"],
    transform_set=ghunt_set
    )
class ghuntToReviews(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        async def main():

            # Parse address into maltego.Location
            location_json = geocoder.osm(request.getProperty("address")).json
            maltego_json = {
                "country": '',
                "city": '',
                "streetaddress": '',
                "areacode": '',
                "area": '',
                "countrycode": '',
                "longitude": request.getProperty("longitude"),
                "latitude": request.getProperty("latitude")
            }
            location = response.addEntity("maltego.Location", value = request.getProperty("address"))

            if location_json:
                if "country" in location_json:
                    maltego_json["country"] = location_json["country"]

                if "city" in location_json:
                    maltego_json["city"] = location_json["city"]
                elif "town" in location_json:
                    maltego_json["city"] = location_json["town"]

                if "housenumber" in location_json and "street" in location_json:
                    maltego_json["streetaddress"] = location_json["housenumber"] + " " + location_json["street"]
                elif "street" in location_json:
                    maltego_json["streetaddress"] = location_json["street"]

                if "region" in location_json:
                    maltego_json["area"] = location_json["region"]
                elif "state" in location_json:
                    maltego_json["area"] = location_json["state"]

                if "country_code" in location_json:
                    maltego_json["countrycode"] = location_json["country_code"]

                if maltego_json["country"] and maltego_json["city"]:
                    location.value = maltego_json["city"] + ", " + maltego_json["country"]

            else:
                response.addUIMessage("Failed to parse address")

            # Commit maltego json properties to the entity
            for p in maltego_json:
                location.addProperty(p, value = maltego_json[p])

            # Display rating
            rating = response.addEntity("maltego.Sentiment", value = request.getProperty("rating"))

            # List industry types
            types = eval(request.getProperty("type"))
            for t in types:
                response.addEntity("maltego.Industry", value = t)

            # List tags
            tags = eval(request.getProperty("tags"))
            for t in tags:
                response.addEntity("maltego.hashtag", value = t)  

        trio.run(main) # running our async code in a non-async code