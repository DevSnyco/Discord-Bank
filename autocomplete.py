from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from discord import Interaction
from discord.app_commands import Choice

class Autocomplete():
	def __init__(self, mongo_session: AsyncIOMotorClient):
		self.mongo_session = mongo_session

	async def internal_accounts(
		self,
		interaction: Interaction,
		current: str
	) -> List[Choice[str]]:
		if await self.mongo_session["users"].count_documents(
			{
				"_id": interaction.user.id
			}
		) == 0:
			return []

		else:
			bank_accounts = self.mongo_session["users"].find_one(
				{
					"_id": interaction.user.id
				}
			).get("accounts")
			return [
				Choice(name=account_number, value=account_number)
				for account_number in [
					str(account.get("account"))
					for account in bank_accounts
				] if current.lower() in account_number.lower()
			]