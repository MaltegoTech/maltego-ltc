from dotenv import dotenv_values
from atop.atop import *
from maltego_trx.maltego import MaltegoTransform

class Util():

    config = None
    telegram_pivot = True

    def __init__(self):
        try:
            self.config = dotenv_values(".env")
        except:
            pass

    @staticmethod
    def check_format(_string):
        if re.match(r"\+?888[0-9\s]{0,12}", _string.strip()):
            return "NUMBER"
        if re.match(r"[a-z0-9-_]+\.ton", _string.strip()):
            return "DOMAIN"
        if re.match(r"@[a-z0-9_]", _string.strip()):
            return "NICKNAME"
        return None


    def create_atop_entities(self, input_string, response: MaltegoTransform, nft_type=None):
        search_maltego = input_string.lower()
        if nft_type and nft_type == "USERNAME":
            search_maltego = "@" + search_maltego

        try:
            if not self.config or (
                    not self.config["API_ID"]
                    or not self.config["API_HASH"]
                    or not self.config["SESSION_STRING"]
            ):
                self.telegram_pivot = False

            if self.telegram_pivot:
                current_parser = Ton_retriever(
                    search_maltego,
                    True,
                    False,
                    True,
                    self.telegram_pivot,
                    None,
                    self.config["API_HASH"],
                    self.config["API_ID"],
                    None,
                    self.config["SESSION_STRING"],
                )
            else:
                current_parser = Ton_retriever(
                    search_maltego, True, False, True, self.telegram_pivot
                )
            current_parser.start_searching()
        except Exception as exx:
            response.addUIMessage("There was an error while parsing the TON data")
            exit(0)

        if current_parser.address != "":
            owner = response.addEntity("atop.TONaddress", value=current_parser.address)
            owner.addProperty("balance", value=str(
                round(int(current_parser.info["result"]["balance"]) / 1000000000, 2)
            ))
            if current_parser.owner_name and current_parser.owner_name != "":
                owner.addProperty("nickname", value=current_parser.owner_name)

        if current_parser.nfts:
            if "data" in current_parser.nfts.keys():
                if "nftItemsByOwner" in current_parser.nfts["data"].keys():
                    for item in current_parser.nfts["data"]["nftItemsByOwner"]["items"]:
                        if "Usernames" in item["collection"]["name"]:
                            type_entity = "atop.TONnickname"
                        elif "Numbers" in item["collection"]["name"]:
                            type_entity = "atop.TONtelephonenumber"
                        elif "TON DNS" in item["collection"]["name"]:
                            type_entity = "atop.TONdomain"
                        else:
                            type_entity = "atop.TONnft"
                        nft = response.addEntity(type_entity, value=current_parser.address)
                        nft.addProperty("address", value=item["name"])

                        if self.telegram_pivot:
                            id = ""
                            name = ""
                            nickname = ""
                            kind = ""
                            photo = ""
                            description = ""

                            if "tg-data" in item.keys():
                                if "apidetail" in item["tg-data"][2].keys():
                                    id = str(item["tg-data"][2]["apidetail"].id)
                                    if item["tg-data"][2]["apidetail"].first_name:
                                        name = name + item["tg-data"][2]["apidetail"].first_name
                                    if item["tg-data"][2]["apidetail"].last_name:
                                        name = name + item["tg-data"][2]["apidetail"].last_name

                                if "webdetail" in item["tg-data"][2].keys():
                                    if (
                                            item["tg-data"][2]["webdetail"]["nickname"]
                                            and item["tg-data"][2]["webdetail"]["nickname"] != "N/A"
                                    ):
                                        nickname = item["tg-data"][2]["webdetail"]["nickname"]

                                    if (
                                            item["tg-data"][2]["webdetail"]["kind"]
                                            and item["tg-data"][2]["webdetail"]["kind"] != "N/A"
                                    ):
                                        kind = item["tg-data"][2]["webdetail"]["kind"]

                                    if (
                                            item["tg-data"][2]["webdetail"]["image"]
                                            and item["tg-data"][2]["webdetail"]["image"] != "N/A"
                                    ):
                                        photo = item["tg-data"][2]["webdetail"]["image"]

                                    if (
                                            item["tg-data"][2]["webdetail"]["description"]
                                            and item["tg-data"][2]["webdetail"]["description"]
                                            != "N/A"
                                    ):
                                        description = item["tg-data"][2]["webdetail"][
                                            "description"
                                        ]

                                    nft = response.addEntity("atop.TelegramEntity", value=id)
                                    nft.addProperty("name", value=name)
                                    nft.addProperty("nickname", value=nickname)
                                    nft.addProperty("kind", value=kind)
                                    nft.addProperty("description", value=description)


                                if photo != "" and photo != "N/A":
                                    photo_maltego = response.addEntity("maltego.Image", value=photo)
                                    photo_maltego.addProperty("url", value=photo)


        if current_parser.ens_detail:
            if "data" in current_parser.ens_detail.keys():
                if "domains" in current_parser.ens_detail["data"].keys():
                    if len(current_parser.ens_detail["data"]["domains"]) > 0:
                        ens_name = response.addEntity("atop.ENSdomain", value=current_parser.ens_detail["data"]["domains"][0]["name"])
                        ens_name.addProperty("owner-address", value=current_parser.ens_detail["data"]["domains"][0]["owner"]["address"])