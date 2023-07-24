import logging

from telegram import Bot

import config
from apartment import Apartment

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def send_apartment(apartment: Apartment):
    bot = Bot(token=config.bot_token)
    # formatted message, add link if available
    message = f"""
{'❗ WBS erforderlich' if 'wbs' in apartment and apartment['wbs'] == 'erforderlich' else ''}
📍 {apartment['addr']}
💶 {f"{apartment['price']:.2f}".replace('.', ',')} € kalt
📐 {apartment['sqm']} m²
🛏 {apartment['rooms']} Zimmer
📅 {apartment['timeframe']}
🏗️ Baujahr {apartment['year']}
🛗 Etage {apartment['floor']}
{'🔗 ' + apartment['link'] if 'link' in apartment else ''}
    """.strip()
    # send image if available
    if 'image' in apartment:
        await bot.send_photo(chat_id=config.chat_id, photo=apartment['image'], caption=message)
    else:
        await bot.send_message(chat_id=config.chat_id, text=message, timeout=10)
