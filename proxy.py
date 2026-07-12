import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector

TEST_URL = "https://api.telegram.org"

TIMEOUT = 10


async def check_proxy(proxy: str):
    proxy = proxy.strip()

    if not proxy:
        return

    try:
        connector = ProxyConnector.from_url(proxy)

        timeout = aiohttp.ClientTimeout(total=TIMEOUT)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:

            async with session.get(TEST_URL) as response:
                if response.status == 200:
                    print(f"[✅] Работает: {proxy}")
                else:
                    print(f"[⚠] Ответ {response.status}: {proxy}")

    except Exception as e:
        print(f"[❌] Не работает: {proxy}")
        print(f"     {type(e).__name__}: {e}")


async def main():
    print("Вставьте прокси (по одному в строке).")
    print("Поддерживаются HTTP и SOCKS5.")
    print("Когда закончите — нажмите Enter на пустой строке.\n")

    proxies = []

    while True:
        proxy = input()

        if proxy == "":
            break

        proxies.append(proxy)

    if not proxies:
        print("Прокси не введены.")
        return

    print(f"\nПроверяю {len(proxies)} прокси...\n")

    tasks = [check_proxy(proxy) for proxy in proxies]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())