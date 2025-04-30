import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
import aiohttp
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def fetch_tokens():
    url = "https://api.mevx.io/tokens"  # Example endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

def format_message(token):
    return f"""{token['name']} ({token['symbol']})
CA: {token['address']}
Network: {token['network'].upper()}
Age: {token['age']} | Views: {token['views']}

Token Stats
Price: {token['price']}
MC: {token['market_cap']}
Vol: {token['volume']}
LP: {token['liquidity']}
1H: {token['change_1h']}
ATH: {token['ath']} ({token['ath_change']} | {token['ath_time']})

Links
{'Website' if token.get('website') else ''} {'Telegram' if token.get('telegram') else ''} {'X' if token.get('twitter') else ''}

Security
Top 10: {token['top10_percent']} | {token['holders']} holders
TH: {' | '.join(map(str, token['top_holders']))}
Dev Sold: {token['dev_sold']}
Dex Paid: {token['dex_paid']}

Chart: https://mevx.io/token/{token['address']}
"""


async def send_token_updates():
    tokens = await fetch_tokens()
    for token in tokens:
        # Filter logic
        if token['volume'] < 100_000 or token['market_cap'] < 60_000 or token['age_hours'] > 6 or token['change_1h_percent'] < 30:
            continue
        msg = format_message(token)
        await bot.send_message(CHANNEL_ID, msg, parse_mode=ParseMode.HTML)

async def main():
    await send_token_updates()

if __name__ == "__main__":
    asyncio.run(main())
