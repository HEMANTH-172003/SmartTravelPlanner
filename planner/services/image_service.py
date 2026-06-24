import requests


class ImageService:

    ACCESS_KEY = "XQi9Wcv79Gfw_Eu080j2JHoztaZojsR_IHqgAwVnSG4"

    @staticmethod
    def get_image(query):

        try:

            url = (
                "https://api.unsplash.com/search/photos"
            )

            headers = {
                "Authorization":
                f"Client-ID {ImageService.ACCESS_KEY}"
            }

            params = {
                "query": query,
                "per_page": 1
            }

            response = requests.get(
                url,
                headers=headers,
                params=params
            )

            data = response.json()

            if data.get("results"):

                return data["results"][0][
                    "urls"
                ]["regular"]

        except Exception as e:

            print(e)

        return None