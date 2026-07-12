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
                    print(f"[✅] Works: {proxy}")
                else:
                    print(f"[⚠] Answer {response.status}: {proxy}")

    except Exception as e:
        print(f"[❌] Not working: {proxy}")
        print(f"     {type(e).__name__}: {e}")


async def main():
    print("Enter the proxies (one per line).")
    print("HTTP and SOCKS5 are supported.")
    print("When you are finished, press Enter on an empty line.\n")

    proxies = []

    while True:
        proxy = input()

        if proxy == "":
            break

        proxies.append(proxy)

    if not proxies:
        print("No proxies entered.")
        return

    print(f"\nChecking {len(proxies)} proxy...\n")

    tasks = [check_proxy(proxy) for proxy in proxies]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())