
import requests


class WikipediaService:

    @staticmethod
    def get_image(place_name):

        try:

            search_url = (
                "https://en.wikipedia.org/w/api.php"
            )

            params = {

                "action": "query",

                "format": "json",

                "titles": place_name,

                "prop": "pageimages",

                "piprop": "original"

            }

            response = requests.get(

                search_url,

                params=params,

                headers={

                    "User-Agent":
                    "SmartTravelPlanner/1.0"

                },

                timeout=10

            )

            data = response.json()

            pages = (

                data.get("query", {})
                .get("pages", {})

            )

            for page in pages.values():

                if "original" in page:

                    image_url = (

                        page["original"]["source"]

                    )

                    return image_url

            return None

        except Exception as e:

            print(

                "Wikipedia Image Error:",

                e

            )

            return None