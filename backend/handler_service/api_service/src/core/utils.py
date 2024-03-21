import requests

from db import cache


async def get_coefficient_to_usd(key_1, key_2):
    coefficient = await cache.cache.get(f"{key_1}-{key_2}")
    if not coefficient:
        i = 0
        for a in range(10):
            response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={key_1}&tsyms={key_2}")
            if response.status_code == 200:
                response = response.json()
                coefficient = float(response.get(f"{key_2}"))
                break
            i += 1
            if i > 10:
                coefficient = 0
                break
        await cache.cache.set(f"{key_1}-{key_2}", coefficient, 120)

    return coefficient


async def get_price_in_usd(price):

    try:
        coefficient = await get_coefficient_to_usd(key_1="ETH", key_2="USD")
        price_in_usd = round(price * coefficient, 2)
        return str(price_in_usd)

    except Exception:
        return None
