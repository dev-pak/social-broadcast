import discord
import asyncio
from simple_settings import settings


async def send_news(message, channel):
    client = discord.Client()
    try:
        await client.login(settings.discord_token)
    except discord.errors.LoginFailure:
        return None
    channel = discord.Object(channel)
    await client.send_message(channel, message)
    await client.logout()


def main(message, link=None, channel=settings.discord_channel):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_news(message, channel))
