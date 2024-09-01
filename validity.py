from motor.motor_asyncio import AsyncIOMotorClient

from discord import Interaction

class Validity:
    @staticmethod
    async def has_any_accounts(mongo_session, interaction: Interaction):
        return True if await mongo_session["users"].count_documents(
            {
                "_id": interaction.user.id
            }
        ) == 1 else False