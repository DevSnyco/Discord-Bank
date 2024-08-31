import os
import asyncio
import traceback

from typing import Any, Coroutine
from dotenv import find_dotenv, load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from discord import Intents
from discord.ext.commands import Bot

from console import Console

class DiscordBank(Bot):
	def __init__(self):
		super().__init__(command_prefix = "/", intents = Intents.all())

	async def start(self, *args, **kwargs):
		await super().start(*args, **kwargs)
		Console.info("Started Bot")

	async def setup_hook(self) -> Coroutine[Any, Any, None]:
		Console.info("Setup hook initiated")
		if os.getenv("MONGO_TLS") == "True":
			self.database = AsyncIOMotorClient(
				os.getenv("MONGO"),
				tls = True,
				tlsCertificateKeyFile = "mongo_cert.pem"
			)["bank"]
		else:
			self.database = AsyncIOMotorClient(os.getenv("MONGO"))["bank"]

		for file in os.listdir("./cogs"):
			if file.endswith(".py"):
				try:
					await self.load_extension(f"cogs.{file[:-3]}")
					self.loaded_extension_list.append(file[:-3])
					Console.info(f"Loaded \"\033[93m{file[:-3]}\033[0m\" extension")
				except Exception as error:
					self.unloaded_extension_list.append(file[:-3])
					Console.error(error)
					continue

		self.loop.create_task(self.sync_commands())
		Console.info("Setup hook completed")

if __name__ == "__main__":
	asyncio.run(DiscordBank().start(os.getenv("TOKEN")))