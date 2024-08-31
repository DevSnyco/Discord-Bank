import os
import asyncio
import traceback

from typing import Any, Coroutine
from motor.motor_asyncio import AsyncIOMotorClient

from discord import Intents
from discord.ext.commands import Bot

class DiscordBank(Bot):
	def __init__(self):
		super().__init__(command_prefix = "/", intents = Intents.all())

	async def start(self, *args, **kwargs):
		await super().start(*args, **kwargs)

	async def setup_hook(self) -> Coroutine[Any, Any, None]:
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
					print(f"Loaded \"{file[:-3]}\" extension")
				except Exception as error:
					self.unloaded_extension_list.append(file[:-3])
					traceback.print_exc(error)

		self.loop.create_task(self.sync_commands())

if __name__ == "__main__":
	asyncio.run(DiscordBank().start(os.getenv("TOKEN")))