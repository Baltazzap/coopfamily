import discord
from discord.ext import commands
from discord import Permissions
from discord.ui import Button, View
import os
from dotenv import load_dotenv
import random
import asyncio

# Загрузка переменных окружения из .env файла
load_dotenv()

# --- НАСТРОЙКИ ---
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("❌ Error: DISCORD_TOKEN not found in environment variables!")
    print("💡 Please create a .env file with DISCORD_TOKEN=your_token_here")
    exit(1)

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

bot = commands.Bot(command_prefix='!', intents=INTENTS, help_command=None)

# --- ID КАНАЛОВ ---
CHANNEL_IDS = {
    "rules": "1479178350823211068",
    "roles": "1479178355701186695",
    "general": "1479178361535201513",
    "lfg-pve": "1479178383601434675"
}

# --- ID АВТО-РОЛИ ---
AUTO_ROLE_ID = 1479178344976089179

# --- ID РОЛЕЙ ЯЗЫКОВ ---
LANG_ENGLISH = 1479604985774735371
LANG_RUSSIAN = 1479605065445806294

# --- ID РОЛЕЙ ДЛЯ САМОВЫДАЧИ ---
SELF_ASSIGNABLE_ROLES = {
    "PC": {"id": 1479178336755388448, "emoji": "🖥️", "label": "PC Gamer", "desc_en": "Play on PC (Steam/Ubisoft)", "desc_ru": "Игра на ПК (Steam/Ubisoft)"},
    "PlayStation": {"id": 1479178337732792632, "emoji": "🎮", "label": "PlayStation", "desc_en": "Play on PS4/PS5", "desc_ru": "Игра на PS4/PS5"},
    "Xbox": {"id": 1479178338819117207, "emoji": "🕹️", "label": "Xbox", "desc_en": "Play on Xbox One/Series", "desc_ru": "Игра на Xbox One/Series"},
    "PvE-Hardcore": {"id": 1479178339884204032, "emoji": "⚔️", "label": "PvE Hardcore", "desc_en": "Raids, Heroic, Optimized builds", "desc_ru": "Рейды, Героик, Оптимизированные билды"},
    "PvE-Casual": {"id": 1479178340941172737, "emoji": "🌿", "label": "PvE Casual", "desc_en": "Missions, Farming, relaxed gameplay", "desc_ru": "Миссии, Фарм, расслабленная игра"},
    "BattlePass-Grind": {"id": 1479178342069571787, "emoji": "🏆", "label": "BattlePass Grind", "desc_en": "Focus on Battle Pass progression", "desc_ru": "Фокус на прогресс Боевого пропуска"},
    "Ping-Events": {"id": 1479178342572884099, "emoji": "📢", "label": "Ping Events", "desc_en": "Get notified about clan events", "desc_ru": "Уведомления о клан-ивентах"},
    "Ping-LFG": {"id": 1479178343885836562, "emoji": "🔍", "label": "Ping LFG", "desc_en": "Get notified about group finding", "desc_ru": "Уведомления о поиске группы"},
    "English": {"id": LANG_ENGLISH, "emoji": "🇬🇧", "label": "English", "desc_en": "English language", "desc_ru": "Английский язык"},
    "Русский": {"id": LANG_RUSSIAN, "emoji": "🇷🇺", "label": "Русский", "desc_en": "Russian language", "desc_ru": "Русский язык"}
}

# --- ЦВЕТА РОЛЕЙ ---
ROLE_COLORS = {
    "Leader": 0xFF6B35,
    "Officer": 0xFFD700,
    "Veteran": 0xC0C0C0,
    "Raid-Leader": 0xE74C3C,
    "PC": 0x3498DB,
    "PlayStation": 0x0070D1,
    "Xbox": 0x107C10,
    "PvE-Hardcore": 0x8E44AD,
    "PvE-Casual": 0x27AE60,
    "BattlePass-Grind": 0xF1C40F,
    "Ping-Events": 0xE91E63,
    "Ping-LFG": 0x1ABC9C,
    "English": 0x3498DB,
    "Русский": 0xE74C3C,
    "New-Agent": 0x7F8C8D,
    "Muted": 0x2C3E50
}

# --- БАЗА ДАННЫХ ЭКЗОТИКОВ ---
EXOTICS_DB = [
    {"name": "Merciless & Ruthless", "type": "Rifle & Pistol", "talent": "The Show Must Go On", "location": "Invaded District Union Arena", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/0/02/Merciless.png"},
    {"name": "Chatterbox", "type": "SMG", "talent": "Unhinged", "location": "Invaded Bank Headquarters", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/9/9a/Chatterbox.png"},
    {"name": "Lady Death", "type": "SMG", "talent": "Obliterate", "location": "Invaded Tidal Basin", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/1/1a/Lady_Death.png"},
    {"name": "Pestilence", "type": "Assault Rifle", "talent": "Plague", "location": "Invaded Capitol Building", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/8/8a/Pestilence.png"},
    {"name": "Nemesis", "type": "Sniper Rifle", "talent": "Perfect Unwavering", "location": "Invaded Potomac Event Center", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/5/5a/Nemesis.png"},
    {"name": "Dodge City Gunslinger", "type": "Holster", "talent": "Fan the Hammer", "location": "Invaded Manning National Zoo", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/3/3a/Dodge_City.png"},
    {"name": "Heartbreaker", "type": "LMG", "talent": "Perfect Sledgehammer", "location": "Iron Horse Raid", "difficulty": "Raid", "image": "https://static.wikia.nocookie.net/thedivision/images/6/6a/Heartbreaker.png"},
    {"name": "Paradox", "type": "Assault Rifle", "talent": "Perfect Time Dilation", "location": "Manhunt Targets", "difficulty": "Heroic", "image": "https://static.wikia.nocookie.net/thedivision/images/7/7a/Paradox.png"}
]

# --- КОМПЛИМЕНТЫ ---
COMPLIMENTS_EN = [
    "You're an amazing agent! 🧡",
    "Your gameplay is legendary! 🏆",
    "You make the team better! 🎯",
    "Your positivity is contagious! ✨",
    "You're a true Division veteran! 🎖️"
]

COMPLIMENTS_RU = [
    "Ты потрясающий агент! 🧡",
    "Твой геймплей легендарен! 🏆",
    "Ты делаешь команду лучше! 🎯",
    "Твой позитив заразителен! ✨",
    "Ты настоящий ветеран Division! 🎖️"
]

# --- ЗАПРЕЩЁННЫЕ СЛОВА ---
FORBIDDEN_WORDS = [
    "scam", "hack", "cheat", "glitch", "exploit",
    "toxic", "hate", "spam", "nsfw",
    "скам", "чит", "глитч", "токсик"
]

# --- ВОПРОСЫ ДЛЯ ВИКТОРИНЫ ---
TRIVIA_QUESTIONS = [
    {"question_en": "What is the name of the AI system used by Division agents?", "question_ru": "Как называется ИИ-система агентов Division?", "options": ["ISAC", "JTF", "SHD", "BTSU"], "answer": 0},
    {"question_en": "Which faction controls the White House at the start of Division 2?", "question_ru": "Какая фракция контролирует Белый Дом в начале Division 2?", "options": ["Hyenas", "Outcasts", "True Sons", "Black Tusk"], "answer": 2},
    {"question_en": "What is the max Gear Score in Warlords of New York?", "question_ru": "Какой максимальный Gear Score в Warlords of New York?", "options": ["450", "500", "515", "600"], "answer": 2},
    {"question_en": "Which exotic SMG has the 'Obliterate' talent?", "question_ru": "Какой SMG имеет талант 'Obliterate'?", "options": ["Chatterbox", "Lady Death", "Tommy Gun", "Vector"], "answer": 1},
    {"question_en": "What year was The Division 2 released?", "question_ru": "В каком году вышла The Division 2?", "options": ["2017", "2018", "2019", "2020"], "answer": 2}
]

# --- СИСТЕМА ОЧКОВ ВИКТОРИНЫ ---
trivia_scores = {}
active_trivia = None

# ============================================
# ✅ ФУНКЦИЯ ОПРЕДЕЛЕНИЯ ЯЗЫКА
# ============================================
async def get_user_language(member):
    """
    🌐 Определяет язык пользователя по роли
    """
    for role in member.roles:
        if role.id == LANG_ENGLISH:
            return "en"
        if role.id == LANG_RUSSIAN:
            return "ru"
    return "en"  # По умолчанию английский

# ============================================
# ✅ КЛАСС ДЛЯ КНОПОК ЭКЗОТИКОВ
# ============================================
class ExoticSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎲 Random Exotic", style=discord.ButtonStyle.blurple, emoji="🎲", custom_id="exotic_random")
    async def random_exotic(self, interaction: discord.Interaction, button: Button):
        lang = await get_user_language(interaction.user)
        exotic = random.choice(EXOTICS_DB)
        
        if lang == "ru":
            embed = discord.Embed(title=f"🎲 Случайный экзотик: {exotic['name']}", description=f"**Тип:** {exotic['type']}\n**Талант:** `{exotic['talent']}`", color=0xFFD700)
            embed.add_field(name="📍 Место дропа", value=exotic['location'], inline=False)
            embed.add_field(name="⚠️ Сложность", value=exotic['difficulty'], inline=False)
            embed.set_footer(text="CoopFamily • Удачи в фарме!", icon_url="https://i.imgur.com/sAnFJ4c.png")
        else:
            embed = discord.Embed(title=f"🎲 Random Exotic: {exotic['name']}", description=f"**Type:** {exotic['type']}\n**Talent:** `{exotic['talent']}`", color=0xFFD700)
            embed.add_field(name="📍 Drop Location", value=exotic['location'], inline=False)
            embed.add_field(name="⚠️ Difficulty", value=exotic['difficulty'], inline=False)
            embed.set_footer(text="CoopFamily • Good luck farming!", icon_url="https://i.imgur.com/sAnFJ4c.png")
        
        embed.set_thumbnail(url=exotic['image'])
        await interaction.response.edit_message(embed=embed, view=ExoticSelectView())
    
    @discord.ui.button(label="📋 All Exotics", style=discord.ButtonStyle.gray, emoji="📋", custom_id="exotic_all")
    async def all_exotics(self, interaction: discord.Interaction, button: Button):
        lang = await get_user_language(interaction.user)
        
        if lang == "ru":
            embed = discord.Embed(title="📋 Список всех экзотиков", description="Все доступные экзотические оружия и снаряжение", color=0xFFD700)
            for i, exotic in enumerate(EXOTICS_DB, 1):
                embed.add_field(name=f"{i}. {exotic['name']}", value=f"**Тип:** {exotic['type']}\n**Место:** {exotic['location']}", inline=False)
            embed.set_footer(text="CoopFamily • Используйте !exotics <название> для деталей", icon_url="https://i.imgur.com/sAnFJ4c.png")
        else:
            embed = discord.Embed(title="📋 All Exotics List", description="Here are all available exotic weapons and gear", color=0xFFD700)
            for i, exotic in enumerate(EXOTICS_DB, 1):
                embed.add_field(name=f"{i}. {exotic['name']}", value=f"**Type:** {exotic['type']}\n**Location:** {exotic['location']}", inline=False)
            embed.set_footer(text="CoopFamily • Use !exotics <name> for details", icon_url="https://i.imgur.com/sAnFJ4c.png")
        
        await interaction.response.edit_message(embed=embed, view=ExoticSelectView())

# ============================================
# ✅ КЛАСС ДЛЯ КНОПОК РОЛЕЙ
# ============================================
class RoleSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for role_key, role_data in SELF_ASSIGNABLE_ROLES.items():
            emoji = role_data["emoji"]
            if role_key in ["PC", "PlayStation", "Xbox"]:
                style = discord.ButtonStyle.blurple
            elif role_key in ["Ping-Events", "Ping-LFG"]:
                style = discord.ButtonStyle.green
            elif role_key in ["English", "Русский"]:
                style = discord.ButtonStyle.blurple
            else:
                style = discord.ButtonStyle.gray
            self.add_item(RoleButton(role_key, role_data["id"], emoji, style, custom_id=f"role_{role_key}"))

class RoleButton(Button):
    def __init__(self, role_key, role_id, emoji, style, custom_id):
        super().__init__(style=style, label=role_key, emoji=emoji, custom_id=custom_id)
        self.role_key = role_key
        self.role_id = role_id
    
    async def callback(self, interaction: discord.Interaction):
        lang = await get_user_language(interaction.user)
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(self.role_id)
        
        if not role:
            if lang == "ru":
                await interaction.response.send_message("❌ Роль не найдена!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Role not found!", ephemeral=True)
            return
        
        if role in member.roles:
            await member.remove_roles(role)
            if lang == "ru":
                await interaction.response.send_message(f"❌ Удалена роль <@&{self.role_id}>!", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Removed <@&{self.role_id}>!", ephemeral=True)
        else:
            await member.add_roles(role)
            if lang == "ru":
                await interaction.response.send_message(f"✅ Добавлена роль <@&{self.role_id}>!", ephemeral=True)
            else:
                await interaction.response.send_message(f"✅ Added <@&{self.role_id}>!", ephemeral=True)

# ============================================
# ✅ КЛАСС ДЛЯ КНОПОК ВИКТОРИНЫ (ИСПРАВЛЕНО)
# ============================================
class TriviaView(View):
    def __init__(self, correct_answer: int, question_data: dict, lang: str):  # ✅ Исправлено: question_data: dict
        super().__init__(timeout=30)
        self.correct_answer = correct_answer
        self.question_data = question_data
        self.lang = lang
        self.answered = False
    
    @discord.ui.button(label="A", style=discord.ButtonStyle.blurple, custom_id="trivia_a")
    async def option_a(self, interaction: discord.Interaction, button: Button):
        await self.check_answer(interaction, 0)
    
    @discord.ui.button(label="B", style=discord.ButtonStyle.blurple, custom_id="trivia_b")
    async def option_b(self, interaction: discord.Interaction, button: Button):
        await self.check_answer(interaction, 1)
    
    @discord.ui.button(label="C", style=discord.ButtonStyle.blurple, custom_id="trivia_c")
    async def option_c(self, interaction: discord.Interaction, button: Button):
        await self.check_answer(interaction, 2)
    
    @discord.ui.button(label="D", style=discord.ButtonStyle.blurple, custom_id="trivia_d")
    async def option_d(self, interaction: discord.Interaction, button: Button):
        await self.check_answer(interaction, 3)
    
    async def check_answer(self, interaction: discord.Interaction, answer: int):
        if self.answered:
            if self.lang == "ru":
                await interaction.response.send_message("⏰ Уже отвечено!", ephemeral=True)
            else:
                await interaction.response.send_message("⏰ Already answered!", ephemeral=True)
            return
        
        self.answered = True
        user = interaction.user
        
        if answer == self.correct_answer:
            trivia_scores[user.id] = trivia_scores.get(user.id, 0) + 10
            if self.lang == "ru":
                await interaction.response.send_message(f"✅ **Правильно!** +10 очков, {user.name}!", ephemeral=True)
            else:
                await interaction.response.send_message(f"✅ **Correct!** +10 points, {user.name}!", ephemeral=True)
        else:
            if self.lang == "ru":
                await interaction.response.send_message(f"❌ **Неправильно!** Ответ был {chr(65 + self.correct_answer)}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ **Wrong!** The answer was {chr(65 + self.correct_answer)}.", ephemeral=True)
        
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(view=self)

# --- СОБЫТИЯ ---
@bot.event
async def on_ready():
    print(f'✅ Bot Online: {bot.user.name}')
    print(f'🔗 Server ID: {bot.guilds[0].id if bot.guilds else "N/A"}')
    await bot.change_presence(activity=discord.Game(name="The Division 2 | !help"))
    bot.add_view(RoleSelectView())
    bot.add_view(ExoticSelectView())

@bot.event
async def on_member_join(member):
    try:
        auto_role = member.guild.get_role(AUTO_ROLE_ID)
        if auto_role:
            await member.add_roles(auto_role)
    except Exception as e:
        print(f"❌ Error assigning auto-role: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await auto_moderate(message)
    await bot.process_commands(message)

# --- АВТО-МОДЕРАЦИЯ ---
async def auto_moderate(message):
    if message.author.guild_permissions.administrator:
        return
    
    content = message.content
    
    # 1. Блокировка инвайтов Discord
    if "discord.gg/" in content.lower() or "discord.com/invite" in content.lower():
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, Discord invites are not allowed!", delete_after=5)
        return
    
    # 2. Блокировка спама ссылок
    link_count = content.count("http://") + content.count("https://")
    if link_count > 3:
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, Too many links!", delete_after=5)
        return
    
    # 3. Блокировка КАПСА
    if len(content) > 10:
        caps_ratio = sum(1 for c in content if c.isupper()) / len(content)
        if caps_ratio > 0.7:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, Please don't use all caps!", delete_after=5)
            return
    
    # 4. Блокировка запрещённых слов
    for word in FORBIDDEN_WORDS:
        if word in content.lower():
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, That word is not allowed!", delete_after=5)
            return

# --- КОМАНДЫ ---

@bot.command(name='welcome')
@commands.has_permissions(manage_messages=True)
async def send_welcome(ctx):
    # Английский эмбед
    embed_en = discord.Embed(title="🧡 Welcome to CoopFamily", description='"United We Stand, Divided We Fall" — Our motto in Washington.', color=0xFF6B35)
    embed_en.add_field(name="🎯 What to Expect?", value="• 🤝 Friendly PvE Community\n• 🔍 24/7 LFG for Missions & Farming\n• 📚 Guides, Builds & Newbie Help\n• 🏆 Joint Battlepass & Exotic Farming\n• 🎙️ Active Voice Chats", inline=False)
    embed_en.add_field(name="📋 First Steps:", value=f"1️⃣ Read rules in <#{CHANNEL_IDS['rules']}>\n2️⃣ Pick your platform in <#{CHANNEL_IDS['roles']}>\n3️⃣ Introduce yourself in <#{CHANNEL_IDS['general']}>\n4️⃣ Find a group in <#{CHANNEL_IDS['lfg-pve']}>", inline=False)
    embed_en.set_footer(text="CoopFamily • SHD Network Active", icon_url="https://i.imgur.com/sAnFJ4c.png")
    embed_en.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed_en)
    
    # Русский эмбед (отдельным сообщением)
    embed_ru = discord.Embed(title="🧡 Добро пожаловать в CoopFamily", description='"Вместе мы сильны, по отдельности мы падаем" — Наш девиз в Вашингтоне.', color=0xFF6B35)
    embed_ru.add_field(name="🎯 Что вас ждёт?", value="• 🤝 Дружелюбное PvE-комьюнити\n• 🔍 Поиск группы 24/7 для миссий и фарма\n• 📚 Гайды, билды и помощь новичкам\n• 🏆 Совместный фарм Battle Pass и экзотики\n• 🎙️ Активные голосовые чаты", inline=False)
    embed_ru.add_field(name="📋 Первые шаги:", value=f"1️⃣ Прочти правила в <#{CHANNEL_IDS['rules']}>\n2️⃣ Выбери платформу в <#{CHANNEL_IDS['roles']}>\n3️⃣ Представься в <#{CHANNEL_IDS['general']}>\n4️⃣ Найди группу в <#{CHANNEL_IDS['lfg-pve']}>", inline=False)
    embed_ru.set_footer(text="CoopFamily • Сеть SHD активна", icon_url="https://i.imgur.com/sAnFJ4c.png")
    embed_ru.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed_ru)

@bot.command(name='rules')
@commands.has_permissions(manage_messages=True)
async def send_rules(ctx):
    # Английский эмбед
    embed_en = discord.Embed(title="📜 CoopFamily Server Rules", description='"With great power comes great responsibility"', color=0xFF6B35)
    embed_en.add_field(name="🛡️ General Conduct", value="1️⃣ **Be Respectful**\n2️⃣ **No Toxicity**\n3️⃣ **English Only** in public channels\n4️⃣ **No Spam**\n5️⃣ **No NSFW**", inline=False)
    embed_en.add_field(name="🎮 Division 2 Rules", value="6️⃣ **PvE Focus**\n7️⃣ **No Cheating**\n8️⃣ **Share Loot**\n9️⃣ **Use Mic for Raids**\n🔟 **Help New Agents**", inline=False)
    embed_en.add_field(name="⚠️ Rule Violations", value="🟡 **Warning** — Minor offenses\n🟠 **Mute** — Repeated disruptions\n🔴 **Kick/Ban** — Severe violations", inline=False)
    embed_en.set_footer(text="CoopFamily • By joining, you agree", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed_en)
    
    # Русский эмбед (отдельным сообщением)
    embed_ru = discord.Embed(title="📜 Правила сервера CoopFamily", description='"С большой силой приходит большая ответственность"', color=0xFF6B35)
    embed_ru.add_field(name="🛡️ Общие правила", value="1️⃣ **Уважайте других**\n2️⃣ **Нет токсичности**\n3️⃣ **Английский** в публичных каналах\n4️⃣ **Нет спаму**\n5️⃣ **Нет NSFW**", inline=False)
    embed_ru.add_field(name="🎮 Правила Division 2", value="6️⃣ **Фокус на PvE**\n7️⃣ **Нет читам**\n8️⃣ **Делитесь лутом**\n9️⃣ **Микрофон для рейдов**\n🔟 **Помогайте новичкам**", inline=False)
    embed_ru.add_field(name="⚠️ Нарушения", value="🟡 **Предупреждение** — Малые нарушения\n🟠 **Мут** — Повторные нарушения\n🔴 **Кик/Бан** — Серьёзные нарушения", inline=False)
    embed_ru.set_footer(text="CoopFamily • Присоединяясь, вы соглашаетесь", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed_ru)

@bot.command(name='roles')
@commands.has_permissions(manage_messages=True)
async def send_roles(ctx):
    lang = await get_user_language(ctx.author)
    
    if lang == "ru":
        embed = discord.Embed(title="🎁 Выберите свои роли", description="Нажмите кнопки ниже чтобы получить роли! Нажмите ещё раз чтобы удалить.\n\n**Пинги ролей:**", color=0x3498DB)
        
        platforms_value = ""
        for key in ["PC", "PlayStation", "Xbox"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            platforms_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_ru']}\n"
        embed.add_field(name="🎮 Платформы", value=platforms_value, inline=False)
        
        playstyle_value = ""
        for key in ["PvE-Hardcore", "PvE-Casual", "BattlePass-Grind"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            playstyle_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_ru']}\n"
        embed.add_field(name="⚔️ Стиль игры", value=playstyle_value, inline=False)
        
        notifications_value = ""
        for key in ["Ping-Events", "Ping-LFG"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            notifications_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_ru']}\n"
        embed.add_field(name="🔔 Уведомления", value=notifications_value, inline=False)
        
        language_value = ""
        for key in ["English", "Русский"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            language_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_ru']}\n"
        embed.add_field(name="🌐 Язык", value=language_value, inline=False)
        
        embed.add_field(name="⚠️ Ограниченные роли", value="`Leader` `Officer` `Veteran` — Выдаются только администрацией", inline=False)
        embed.set_footer(text="CoopFamily • Нажмите кнопки для выбора ролей", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        embed = discord.Embed(title="🎁 Select Your Roles", description="Click buttons below to get roles! Click again to remove.\n\n**Role Pings:**", color=0x3498DB)
        
        platforms_value = ""
        for key in ["PC", "PlayStation", "Xbox"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            platforms_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_en']}\n"
        embed.add_field(name="🎮 Platforms", value=platforms_value, inline=False)
        
        playstyle_value = ""
        for key in ["PvE-Hardcore", "PvE-Casual", "BattlePass-Grind"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            playstyle_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_en']}\n"
        embed.add_field(name="⚔️ Playstyle", value=playstyle_value, inline=False)
        
        notifications_value = ""
        for key in ["Ping-Events", "Ping-LFG"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            notifications_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_en']}\n"
        embed.add_field(name="🔔 Notifications", value=notifications_value, inline=False)
        
        language_value = ""
        for key in ["English", "Русский"]:
            role_data = SELF_ASSIGNABLE_ROLES[key]
            language_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc_en']}\n"
        embed.add_field(name="🌐 Language", value=language_value, inline=False)
        
        embed.add_field(name="⚠️ Restricted Roles", value="`Leader` `Officer` `Veteran` — Assigned by administrators only", inline=False)
        embed.set_footer(text="CoopFamily • Click buttons to self-assign roles", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed, view=RoleSelectView())

@bot.command(name='exotics')
@commands.has_permissions(manage_messages=True)
async def send_exotics(ctx, *, exotic_name: str = None):
    lang = await get_user_language(ctx.author)
    
    if exotic_name:
        found = next((e for e in EXOTICS_DB if exotic_name.lower() in e['name'].lower()), None)
        if found:
            if lang == "ru":
                embed = discord.Embed(title=f"🎯 Экзотик: {found['name']}", description=f"**Тип:** {found['type']}\n**Талант:** `{found['talent']}`", color=0xFFD700)
                embed.add_field(name="📍 Место", value=found['location'], inline=False)
                embed.set_footer(text="CoopFamily • Удачи в фарме!", icon_url="https://i.imgur.com/sAnFJ4c.png")
            else:
                embed = discord.Embed(title=f"🎯 Exotic: {found['name']}", description=f"**Type:** {found['type']}\n**Talent:** `{found['talent']}`", color=0xFFD700)
                embed.add_field(name="📍 Location", value=found['location'], inline=False)
                embed.set_footer(text="CoopFamily • Good luck farming!", icon_url="https://i.imgur.com/sAnFJ4c.png")
            embed.set_thumbnail(url=found['image'])
            await ctx.send(embed=embed, view=ExoticSelectView())
        else:
            if lang == "ru":
                await ctx.send(f"❌ Экзотик **{exotic_name}** не найден! Используйте `!exotics` чтобы увидеть все.")
            else:
                await ctx.send(f"❌ Exotic **{exotic_name}** not found! Use `!exotics` to see all.")
    else:
        if lang == "ru":
            embed = discord.Embed(title="🎯 Экзотические оружия и снаряжение", description="Нажмите кнопки ниже для случайного экзотика или полного списка!", color=0xFFD700)
        else:
            embed = discord.Embed(title="🎯 Exotic Weapons & Gear", description="Click buttons below for random exotic or full list!", color=0xFFD700)
        
        featured = random.sample(EXOTICS_DB, min(5, len(EXOTICS_DB)))
        for i, exotic in enumerate(featured, 1):
            if lang == "ru":
                embed.add_field(name=f"{i}. {exotic['name']}", value=f"**Тип:** {exotic['type']}\n**Место:** {exotic['location'][:50]}...", inline=False)
            else:
                embed.add_field(name=f"{i}. {exotic['name']}", value=f"**Type:** {exotic['type']}\n**Location:** {exotic['location'][:50]}...", inline=False)
        
        if lang == "ru":
            embed.set_footer(text="CoopFamily • Используйте !exotics <название> для деталей", icon_url="https://i.imgur.com/sAnFJ4c.png")
        else:
            embed.set_footer(text="CoopFamily • Use !exotics <name> for details", icon_url="https://i.imgur.com/sAnFJ4c.png")
        
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed, view=ExoticSelectView())

@bot.command(name='compliment')
async def send_compliment(ctx, member: discord.Member = None):
    lang = await get_user_language(ctx.author)
    
    if not member:
        member = ctx.author
    
    if lang == "ru":
        compliment = random.choice(COMPLIMENTS_RU)
        embed = discord.Embed(title="💝 Комплимент!", description=f"{member.mention}, {compliment}", color=0xE91E63)
        embed.set_footer(text="CoopFamily • Распространяйте позитив!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        compliment = random.choice(COMPLIMENTS_EN)
        embed = discord.Embed(title="💝 Compliment!", description=f"{member.mention}, {compliment}", color=0xE91E63)
        embed.set_footer(text="CoopFamily • Spread positivity!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed)

@bot.command(name='trivia')
async def start_trivia(ctx):
    global active_trivia
    lang = await get_user_language(ctx.author)
    
    if active_trivia:
        if lang == "ru":
            await ctx.send("⏰ Вопрос викторины уже активен!")
        else:
            await ctx.send("⏰ A trivia question is already active!")
        return
    
    question_data = random.choice(TRIVIA_QUESTIONS)
    active_trivia = question_data
    
    if lang == "ru":
        embed = discord.Embed(title="🧠 Викторина Division 2!", description=f"**{question_data['question_ru']}**\n\n🅰️ {question_data['options'][0]}\n🅱️ {question_data['options'][1]}\n🅾️ {question_data['options'][2]}\n🇩️ {question_data['options'][3]}", color=0x9B59B6)
        embed.add_field(name="⏱️ Время", value="30 секунд", inline=False)
        embed.add_field(name="🏆 Приз", value="10 очков за правильный ответ", inline=False)
        embed.set_footer(text="CoopFamily Викторина • Используйте кнопки для ответа!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        embed = discord.Embed(title="🧠 Division 2 Trivia!", description=f"**{question_data['question_en']}**\n\n🅰️ {question_data['options'][0]}\n🅱️ {question_data['options'][1]}\n🅾️ {question_data['options'][2]}\n🇩️ {question_data['options'][3]}", color=0x9B59B6)
        embed.add_field(name="⏱️ Time Limit", value="30 seconds", inline=False)
        embed.add_field(name="🏆 Prize", value="10 points per correct answer", inline=False)
        embed.set_footer(text="CoopFamily Trivia • Use buttons to answer!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed, view=TriviaView(question_data['answer'], question_data, lang))
    
    await asyncio.sleep(30)
    active_trivia = None

@bot.command(name='trivia-leaderboard')
async def trivia_leaderboard(ctx):
    lang = await get_user_language(ctx.author)
    
    if not trivia_scores:
        if lang == "ru":
            await ctx.send("📊 Очков викторины ещё нет! Начните с `!trivia`")
        else:
            await ctx.send("📊 No trivia scores yet! Start with `!trivia`")
        return
    
    sorted_scores = sorted(trivia_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if lang == "ru":
        embed = discord.Embed(title="🏆 Таблица лидеров викторины", description="Топ-10 чемпионов викторины!", color=0xFFD700)
        for i, (user_id, score) in enumerate(sorted_scores, 1):
            user = await bot.fetch_user(user_id)
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(name=f"{medal} {user.name}", value=f"**{score} очков**", inline=False)
        embed.set_footer(text="CoopFamily Викторина • Продолжайте играть!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        embed = discord.Embed(title="🏆 Trivia Leaderboard", description="Top 10 trivia champions!", color=0xFFD700)
        for i, (user_id, score) in enumerate(sorted_scores, 1):
            user = await bot.fetch_user(user_id)
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(name=f"{medal} {user.name}", value=f"**{score} points**", inline=False)
        embed.set_footer(text="CoopFamily Trivia • Keep playing!", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    lang = await get_user_language(ctx.author)
    
    if lang == "ru":
        embed = discord.Embed(title="🤖 Команды бота CoopFamily", description="Все доступные команды для сервера!", color=0x3498DB)
        embed.add_field(name="🎮 The Division 2", value="`!exotics` — Информация об экзотиках\n`!exotics <название>` — Поиск экзотика\n`!trivia` — Начать викторину\n`!trivia-leaderboard` — Таблица лидеров", inline=False)
        embed.add_field(name="💝 Комьюнити", value="`!compliment @user` — Сделать комплимент", inline=False)
        embed.add_field(name="🏓 Утилиты", value="`!help` — Показать это меню\n`!ping` — Проверить задержку", inline=False)
        embed.set_footer(text="CoopFamily Bot v2.0 • Двуязычный бот", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        embed = discord.Embed(title="🤖 CoopFamily Bot Commands", description="Here are all available commands!", color=0x3498DB)
        embed.add_field(name="🎮 The Division 2", value="`!exotics` — Exotic info\n`!exotics <name>` — Search exotic\n`!trivia` — Start trivia\n`!trivia-leaderboard` — Show scores", inline=False)
        embed.add_field(name="💝 Community", value="`!compliment @user` — Give compliment", inline=False)
        embed.add_field(name="🏓 Utilities", value="`!help` — Show this menu\n`!ping` — Check latency", inline=False)
        embed.set_footer(text="CoopFamily Bot v2.0 • Bilingual Bot", icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    lang = await get_user_language(ctx.author)
    latency = round(bot.latency * 1000)
    
    if lang == "ru":
        embed = discord.Embed(title="🏓 Понг!", description=f"Задержка бота: **{latency}мс**", color=0x2ECC71)
        embed.set_footer(text="CoopFamily • Двуязычный бот", icon_url="https://i.imgur.com/sAnFJ4c.png")
    else:
        embed = discord.Embed(title="🏓 Pong!", description=f"Bot latency: **{latency}ms**", color=0x2ECC71)
        embed.set_footer(icon_url="https://i.imgur.com/sAnFJ4c.png")
    
    await ctx.send(embed=embed)

# --- ОБРАБОТКА ОШИБОК ---
@send_welcome.error
@send_rules.error
@send_roles.error
@send_exotics.error
async def perm_error(ctx, error):
    lang = await get_user_language(ctx.author)
    if isinstance(error, commands.MissingPermissions):
        if lang == "ru":
            await ctx.send("❌ Требуются права **Manage Messages**!")
        else:
            await ctx.send("❌ You need **Manage Messages** permissions!")
    else:
        await ctx.send(f"❌ Error: {error}")

@help_command.error
@ping_command.error
async def cmd_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    try:
        print("🚀 Starting CoopFamily Bot v2.0...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token!")
    except Exception as e:
        print(f"❌ Error: {e}")
