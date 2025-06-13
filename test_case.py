import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import re

# def get_car_details(auto_id):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.9", }
#     url = f"https://auto.ria.com/demo/bu/mainPage/rotator/item/{auto_id}?type=bu&langId=4"
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         auto_data = data.get("auto", {}).get("autoData", {})
#         vin = auto_data.get("vin")
#         marka = auto_data.get("marka")
#         model = auto_data.get("model")
#         price = auto_data.get("price")
#         photo_url = auto_data.get("photoBig")
#         # Extract other details as needed
#         return {
#             "vin": vin,
#             "marka": marka,
#             "model": model,
#             "price": price,
#             "photo_url": photo_url,
#             # Include other details as needed
#         }
#     else:
#         print(f"Failed to retrieve data for auto ID {auto_id}: Status Code {response.status_code}")
#         return None
#
#
# # Example usage
# auto_id = "38424396"  # Replace with the actual auto ID
# car_details = get_car_details(auto_id)
# if car_details:
#     print(car_details)
#
#
# async def get_phone_api_params_from_json(auto_id: str):
#     url = f"https://auto.ria.com/demo/bu/mainPage/rotator/item/{auto_id}?type=bu&langId=4"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             if resp.status != 200:
#                 print(f"❌ Не удалось получить JSON по auto_id {auto_id}")
#                 return None
#             data = await resp.json()
#             user_secure = data.get("userSecure", {})
#             hash_ = user_secure.get("hash")
#             expires = user_secure.get("expires")
#
#             if hash_ and expires:
#                 return auto_id, hash_, expires
#             else:
#                 print(" hash или expires отсутствуют в ответе")
#                 return None
#
#
# async def main():
#     auto_id = "38410612"  # можно заменить на любой ID
#     result = await get_phone_api_params_from_json(auto_id)
#     if result:
#         auto_id, hash_, expires = result
#         print(" Параметры получены:")
#         print(f"auto_id: {auto_id}")
#         print(f"hash: {hash_}")
#         print(f"expires: {expires}")
#         print(f" URL для телефона: https://auto.ria.com/users/phones/{auto_id}?hash={hash_}&expires={expires}")
#     else:
#         print("🚫 Параметры не получены")


# def beaty_test(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
#                       " AppleWebKit/537.36 (KHTML, like Gecko)"
#                       " Chrome/114.0.0.0 Safari/537.36",
#         "Accept-Language": "uk-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     }
#
#     resp = requests.get(url, headers=headers)
#     resp.raise_for_status()  # проверка успешности запроса
#     soup = bs(resp.text, "html.parser")
#
#     # Ищем комментарии по всему документу
#     comments = soup.find_all(string=lambda text: isinstance(text, Comment))
#     pattern = re.compile(r'\b[A-HJ-NPR-Z0-9]{17}\b')
#
#     for comment in comments:
#         match = pattern.search(comment)
#         if match:
#             vin = match.group(0)
#             print("✅ VIN найден:", vin)
#             return vin
#
#     print("❌ VIN не найден.")
#     return None
#
#
# if __name__ == "__main__":
#     beaty_test("https://auto.ria.com/uk/auto_land_rover_range_rover_velar_38325532.html")
# asyncio.run(main()


import requests

url = "https://auto.ria.com/uk/bu/blocks/json/3842/384199/38419942?lang_id=4"
response = requests.get(url)
data = response.json()

vin = data.get("VIN")
print("VIN:", vin)