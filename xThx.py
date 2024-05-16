# Name: xThx
__version__ = (0, 0, 4)
# meta developer: @iamtox
from .. import loader, utils
import asyncio
from telethon.tl.types import Message
from ..inline.types import InlineCall
import re

@loader.tds
class xThx(loader.Module):
    '''Thx в - @mine_evo_bot'''
    strings = {
        "name": "xThx",
    }
    async def client_ready(self, client, db):
        self.config["thx"] = False
        self.client = client
        self.plasma_thx = self.get("plasma_thx")
        if self.plasma_thx is None:
            self.set("plasma_thx", 0)
        self.sun_thx = self.get("sun_thx")
        if self.sun_thx is None:
            self.set("sun_thx", 0)
        self.plasma_from_thx = self.get("plasma_from_thx")
        if self.plasma_from_thx is None:
            self.set("plasma_from_thx", 0)
        self.sun_from_thx = self.get("sun_from_thx")
        if self.sun_from_thx is None:
            self.set("sun_from_thx", 0)
       
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "thx",
                False,
                lambda: "Авто-Thx включён" if self.config.get("thx") else "Авто-Thx выключен",
                validator=loader.validators.Boolean()
            ),
        )
    @loader.command()
    async def xthx(self, message):
        '''- Авто-Thx'''
        self.config["thx"] = not self.config.get("thx", False)
        await utils.answer(message, f"<b><emoji document_id=5472189549473963781>🙏</emoji> Авто-Thx  {'включен <emoji document_id=5980930633298350051>✅</emoji>' if self.config['thx'] else 'выключен <emoji document_id=5980953710157632545>❌</emoji>'}</b>")

    @loader.watcher(only_messages=True)
    async def watcher(self, message: Message):
        if (
            self.config["thx"]
            and message.chat_id == 5522271758
            and "Используй команду Thx чтобы поблагодарить и получить бонус!" in message.raw_text
        ):
            await self.client.send_message("@mine_evo_bot", "Thx")
            if "Глобальный Руда" in message.raw_text:
                await asyncio.sleep(3540)
                await self.client.send_message("@mine_evo_bot", "Бур") 
        if message.chat_id == 5522271758 and "🎆" in message.text.lower() and "ты поблагодарил(а) игрока" in message.text.lower():
            plasma_text = r"\+(\d{1,3}(,\d{3})*(\.\d+)?)"
            match = re.search(plasma_text, message.text, re.IGNORECASE)
            if match:
                plasma_amount_str = match.group(1).replace(',', '') 
                current_plasma_count = self.get("plasma_thx", 0)
                self.set("plasma_thx", current_plasma_count + int(plasma_amount_str))
        if message.chat_id == 5522271758 and "☀" in message.text.lower() and "ты поблагодарил(а) игрока" in message.text.lower():
            sun_text = r"\+(\d+)\s*☀"
            match = re.search(sun_text, message.text, re.IGNORECASE)
            if match:
                sun_amount_str = match.group(1)
                current_sun_count = self.get("sun_thx", 0)
                self.set("sun_thx", current_sun_count + int(sun_amount_str))
        if message.chat_id == 5522271758 and "ты уже поблагодарил(а) этого игрока" in message.text.lower():
            await message.delete()
        if message.chat_id == 5522271758 and "поблагодарил(а) тебя" in message.text.lower():
            plasma_regex = r"\+(\d{1,3}(?:,\d{3})*)(?:\s*\d*)?\s*🎆"
            sun_regex = r"\+(\d+)\s*☀"
            match_plasma = re.search(plasma_regex, message.text)
            match_sun = re.search(sun_regex, message.text)          
            if match_plasma:
                plasma_amount_str = match_plasma.group(1).replace(',', '')
                current_plasma_count = self.get("plasma_from_thx", 0)
                self.set("plasma_from_thx", current_plasma_count + int(plasma_amount_str))            
            if match_sun:
                sun_amount_str = match_sun.group(1)
                current_sun_count = self.get("sun_from_thx", 0)
                self.set("sun_from_thx", current_sun_count + int(sun_amount_str))
                
    @loader.command()
    async def xstat(self, message):
        '''- Статистика Thx'''
        message_text = (
            f"<b>Награда с Thx: <emoji document_id=5431783411981228752>🎆</emoji> {self.get('plasma_thx')} | ☀️ {self.get('sun_thx')}\n</b>"
            f"<b>Награда с Глобальных Бустов: <emoji document_id=5431783411981228752>🎆</emoji> {self.get('plasma_from_thx')} | ☀️ {self.get('sun_from_thx')}\n</b>"              
        )  
        await utils.answer(message, message_text)
         
    @loader.command()
    async def xsbros(self, message):
        '''- Сброс статистики'''
        self.set("plasma_thx", 0)
        self.set("sun_thx", 0)
        self.set("plasma_from_thx", 0)
        self.set("sun_from_thx", 0)
        await utils.answer(message, "<b>Статистика сброшена!</b>")
   
