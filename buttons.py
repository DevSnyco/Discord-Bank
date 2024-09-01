import os

from discord import ButtonStyle, Interaction
from discord.ui import Button, View, button

class TransactionButtons(View):
	def __init__(self, mongo_session, sender_id: str, sender: int, receipient: int, amount: float):
		super().__init__(timeout = 60)
		self.database = mongo_session
		self.sender_id = sender_id
		self.sender = sender
		self.receipient = receipient
		self.amount = amount

	@button(
		label = "Confirm",
		emoji = os.getenv("SEND_EMOJI"),
		style = ButtonStyle.green
	)
	async def confirm(self, button: Button, interaction: Interaction):
		for child in self.children:
			child.disabled = True

		await self.bot.database["users"].update_one(
			{
				"accounts.account": int(self.account_number)
			},
			{
				"$inc": {
					f"accounts.$.balance": -self.amount
				}
			}
		)
		await self.bot.database["users"].update_one(
			{
				"accounts.account": int(self.receipient)
			},
			{
				"$inc": {
					f"accounts.$.balance": self.amount
				}
			}
		)

		await interaction.edit_original_response(
			f"{os.getenv("SUCCESS_EMOJI")} Sent {os.getenv("MONEY_EMOJI")} {self.amount} to `{self.sender_id}` (`{self.receipient}`)",
			view = self
		)

	@button(
		label = "Cancel",
		emoji = os.getenv("CANCEL_EMOJI"),
		style = ButtonStyle.red
	)
	async def cancel(self, button: Button, interaction: Interaction):
		for child in self.child:
			child.disabled = True

		await interaction.edit_original_response(
			f"{os.getenv("SUCCESS_EMOJI")} Cancelled Transaction",
			view = self
		)