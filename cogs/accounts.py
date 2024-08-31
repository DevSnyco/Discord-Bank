import os

from random import randint
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from discord import Embed, Interaction
from discord.app_commands import autocomplete, command
from discord.ext.commands import Bot, GroupCog

class Accounts(GroupCog, group_name = "account"):
	def __init__(self, bot: Bot):
		self.bot = bot

	@command(
		name = "create",
		description = "Create a bank account under your Discord ID."
	)
	async def create(self, interaction: Interaction):
		if await self.bot.database["users"].count_documents(
			{
				"_id": interaction.user.id
			}
		) == 0:
			account_number = randint(100000000, 999999999)
			await self.bot.database["users"].insert_one(
				{
					"accounts": [
						{
							"account": account_number,
							"balance": 0.0,
							"created_at": int(datetime.now().timestamp())
						}
					]
				}
			)
			embed = Embed(
				description = f"Your bank account has been created, here is your account information:\n**Account:** `{account_number}`\n**Bank Balance:** `0.00`\n**Creation Time:** <t:{int(datetime.now().timestamp())}:d> <t:{int(datetime.now().timestamp())}:T>",
				colour = 0x313338
			).set_author(
				name = "Created Account",
				icon_url = os.getenv("SUCCESS_ICON")
			)
			return await interaction.response.send_message(embed = embed, ephemeral = True)

		user_account = self.bot.database["users"].find_one(
			{
				"_id": interaction.user.id
			}
		)

		if len(user_account.get("accounts")) > 3:
			embed = Embed(
				description = "You have reached the maximum number of bank accounts per discord account.",
				colour = 0x313338
			).set_author(
				name = "Creation Failed",
				icon_url = os.getenv("FAILED_ICON")
			)
			await interaction.response.send_message(embed = embed)

		else:
			account_number = randint(100000000, 999999999)
			await self.bot.database["users"].update_one(
				{
					"_id": interaction.user.id
				},
				{
					"$addToSet": {
						"accounts": {
							"account": account_number,
							"balance": 0.0,
							"created_at": int(datetime.now().timestamp())
						}
					}
				}
			)
			embed = Embed(
				description = f"Your bank account has been created, here is your account information:\n**Account:** `{account_number}`\n**Bank Balance:** `0.00`\n**Creation Time:** <t:{int(datetime.now().timestamp())}:d> <t:{int(datetime.now().timestamp())}:T>",
				colour = 0x313338
			).set_author(
				name = "Created Account",
				icon_url = os.getenv("SUCCESS_ICON")
			)
			return await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot: Bot):
	await bot.add_cog(Accounts(bot))