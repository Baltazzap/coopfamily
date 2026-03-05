import discord
from discord.ext import commands
from discord import Permissions
from discord.ui import Button, View
import os
from dotenv import load_dotenv

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

# --- ID РОЛЕЙ ДЛЯ САМОВЫДАЧИ ---
SELF_ASSIGNABLE_ROLES = {
    "PC": {"id": 1479178336755388448, "emoji": "🖥️", "label": "PC Gamer", "desc": "Play on PC (Steam/Ubisoft)"},
    "PlayStation": {"id": 1479178337732792632, "emoji": "🎮", "label": "PlayStation", "desc": "Play on PS4/PS5"},
    "Xbox": {"id": 1479178338819117207, "emoji": "🕹️", "label": "Xbox", "desc": "Play on Xbox One/Series"},
    "PvE-Hardcore": {"id": 1479178339884204032, "emoji": "⚔️", "label": "PvE Hardcore", "desc": "Raids, Heroic, Optimized builds"},
    "PvE-Casual": {"id": 1479178340941172737, "emoji": "🌿", "label": "PvE Casual", "desc": "Missions, Farming, relaxed gameplay"},
    "BattlePass-Grind": {"id": 1479178342069571787, "emoji": "🏆", "label": "BattlePass Grind", "desc": "Focus on Battle Pass progression"},
    "Ping-Events": {"id": 1479178342572884099, "emoji": "📢", "label": "Ping Events", "desc": "Get notified about clan events"},
    "Ping-LFG": {"id": 1479178343885836562, "emoji": "🔍", "label": "Ping LFG", "desc": "Get notified about group finding"}
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
    "New-Agent": 0x7F8C8D,
    "Muted": 0x2C3E50
}

# --- СТРУКТУРА КАНАЛОВ ---
CATEGORIES = {
    "🏠 WELCOME & INFO": [
        ("👋・welcome", "text"),
        ("📜・rules", "text"),
        ("📢・announcements", "text"),
        ("🎁・roles", "text"),
        ("🔗・useful-links", "text")
    ],
    "💬 GENERAL CHAT": [
        ("💬・general", "text"),
        ("🎮・gaming-chat", "text"),
        ("📸・screenshots", "text"),
        ("🤖・bot-commands", "text"),
        ("💡・suggestions", "text")
    ],
    "🎯 THE DIVISION 2: GAME HUB": [
        ("📰・td2-news", "text"),
        ("⚙️・builds-theory", "text"),
        ("🗺️・missions-help", "text"),
        ("👾・boss-strats", "text"),
        ("🛠️・tech-support", "text")
    ],
    "🔍 LFG / ACTIVITIES": [
        ("🔍・lfg-pve", "text"),
        ("🔥・lfg-raids", "text"),
        ("🏆・lfg-battlepass", "text"),
        ("🕐・scheduled-runs", "text"),
        ("🌍・lfg-global", "text")
    ],
    "🔊 VOICE CHANNELS": [
        ("🔊・Lobby", "voice"),
        ("🔊・Squad-1", "voice"),
        ("🔊・Squad-2", "voice"),
        ("🔊・Raid-Command", "voice"),
        ("🔊・AFK / Chill", "voice")
    ],
    "🛠️ STAFF & ADMIN": [
        ("🔐・staff-chat", "text"),
        ("📋・applications", "text"),
        ("🗑️・mod-logs", "text"),
        ("⚙️・server-setup", "text")
    ]
}

# --- КЛАСС ДЛЯ КНОПОК РОЛЕЙ ---
class RoleSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        for role_key, role_data in SELF_ASSIGNABLE_ROLES.items():
            emoji = role_data["emoji"]
            
            if role_key in ["PC", "PlayStation", "Xbox"]:
                style = discord.ButtonStyle.blurple
            elif role_key in ["Ping-Events", "Ping-LFG"]:
                style = discord.ButtonStyle.green
            else:
                style = discord.ButtonStyle.gray
            
            button = RoleButton(role_key, role_data["id"], emoji, style)
            self.add_item(button)

class RoleButton(Button):
    def __init__(self, role_key, role_id, emoji, style):
        super().__init__(style=style, label=role_key, emoji=emoji)
        self.role_key = role_key
        self.role_id = role_id
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        role = guild.get_role(self.role_id)
        
        if not role:
            await interaction.response.send_message("❌ Role not found!", ephemeral=True)
            return
        
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"❌ Removed <@&{self.role_id}>!", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Added <@&{self.role_id}>!", ephemeral=True)

# --- СОБЫТИЯ ---
@bot.event
async def on_ready():
    print(f'✅ Bot Online: {bot.user.name}')
    print(f'🔗 Server ID: {bot.guilds[0].id if bot.guilds else "N/A"}')
    await bot.change_presence(activity=discord.Game(name="The Division 2 | !help"))
    bot.add_view(RoleSelectView())

@bot.event
async def on_member_join(member):
    try:
        auto_role = member.guild.get_role(AUTO_ROLE_ID)
        if auto_role:
            await member.add_roles(auto_role)
            print(f"✅ Auto-role assigned to {member.name}")
            try:
                await member.send(
                    f"🧡 **Welcome to CoopFamily, {member.name}!**\n\n"
                    f"You've been assigned the **New-Agent** role.\n\n"
                    f"📋 **Next steps:**\n"
                    f"• Read rules in <#{CHANNEL_IDS['rules']}>\n"
                    f"• Get your roles in <#{CHANNEL_IDS['roles']}>\n"
                    f"• Introduce yourself in <#{CHANNEL_IDS['general']}>\n\n"
                    f"*United We Stand, Divided We Fall*"
                )
            except discord.Forbidden:
                print(f"⚠️ Cannot send DM to {member.name}")
    except Exception as e:
        print(f"❌ Error assigning auto-role: {e}")

# --- КОМАНДЫ ---

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    guild = ctx.guild
    await ctx.send("🚀 **Starting CoopFamily Server Setup...**")

    created_roles = {}
    for role_name, color in ROLE_COLORS.items():
        try:
            role = await guild.create_role(name=role_name, color=discord.Color(color), reason="CoopFamily Setup")
            created_roles[role_name] = role
        except Exception as e:
            print(f"❌ Error creating role {role_name}: {e}")
    
    await ctx.send(f"🎨 **Created {len(created_roles)} roles.**")

    for cat_name, channels in CATEGORIES.items():
        try:
            category = await guild.create_category_channel(cat_name)
            if "STAFF" in cat_name:
                await category.set_permissions(guild.default_role, view_channel=False)
                if "Leader" in created_roles:
                    await category.set_permissions(created_roles["Leader"], view_channel=True)
                if "Officer" in created_roles:
                    await category.set_permissions(created_roles["Officer"], view_channel=True)
            for ch_name, ch_type in channels:
                if ch_type == "text":
                    await guild.create_text_channel(ch_name, category=category)
                elif ch_type == "voice":
                    await guild.create_voice_channel(ch_name, category=category)
        except Exception as e:
            print(f"❌ Error in category {cat_name}: {e}")

    await ctx.send("✅ **Server Setup Complete!**")

@bot.command(name='welcome')
@commands.has_permissions(manage_messages=True)
async def send_welcome(ctx):
    embed = discord.Embed(
        title="🧡 Welcome to CoopFamily",
        description='"United We Stand, Divided We Fall" — Our motto in Washington.',
        color=0xFF6B35
    )
    embed.add_field(
        name="🎯 What to Expect?",
        value="• 🤝 Friendly PvE Community\n• 🔍 24/7 LFG for Missions & Farming\n• 📚 Guides, Builds & Newbie Help\n• 🏆 Joint Battlepass & Exotic Farming\n• 🎙️ Active Voice Chats (No Toxicity)",
        inline=False
    )
    embed.add_field(
        name="📋 First Steps:",
        value=f"1️⃣ Read rules in <#{CHANNEL_IDS['rules']}>\n2️⃣ Pick your platform in <#{CHANNEL_IDS['roles']}>\n3️⃣ Introduce yourself in <#{CHANNEL_IDS['general']}>\n4️⃣ Find a group in <#{CHANNEL_IDS['lfg-pve']}>",
        inline=False
    )
    embed.add_field(
        name="🔗 Useful Links",
        value="[📖 Official Wiki](https://division.fandom.com)\n[🧮 Build Calculator](https://d2calc.com)\n[🎮 Clan Name: CoopFamily]",
        inline=False
    )
    embed.set_footer(text="CoopFamily • SHD Network Active • Est. 2026", icon_url="https://i.imgur.com/sAnFJ4c.png")
    embed.timestamp = discord.utils.utcnow()
    await ctx.send(embed=embed)

@bot.command(name='rules')
@commands.has_permissions(manage_messages=True)
async def send_rules(ctx):
    """
    📜 Sends beautiful rules embed for the clan.
    """
    embed = discord.Embed(
        title="📜 CoopFamily Server Rules",
        description='"With great power comes great responsibility" — Follow these rules to keep our community safe and fun!',
        color=0xFF6B35  # SHD Orange
    )
    
    # 🛡️ General Rules
    embed.add_field(
        name="🛡️ General Conduct",
        value="1️⃣ **Be Respectful** — No harassment, hate speech, or discrimination\n"
              "2️⃣ **No Toxicity** — We're here to have fun, not to argue\n"
              "3️⃣ **English Only** in public channels (use DMs for other languages)\n"
              "4️⃣ **No Spam** — Avoid excessive pings, caps, or repeated messages\n"
              "5️⃣ **No NSFW Content** — Keep it family-friendly",
        inline=False
    )
    
    # 🎮 Game-Specific Rules
    embed.add_field(
        name="🎮 Division 2 Rules",
        value="6️⃣ **PvE Focus** — This is a PvE community; keep PvP discussions minimal\n"
              "7️⃣ **No Cheating/Glitching** — Report bugs, don't exploit them\n"
              "8️⃣ **Share Loot Fairly** — Be generous with group drops\n"
              "9️⃣ **Communicate in Voice** — Mic required for raids and coordinated runs\n"
              "🔟 **Help New Agents** — We all started somewhere!",
        inline=False
    )
    
    # 🔊 Voice & LFG Rules
    embed.add_field(
        name="🔊 Voice & LFG Etiquette",
        value="• Use appropriate voice channels for your activity\n"
              "• Keep raid channels clear for tactical comms only\n"
              "• In LFG posts, specify: `[Platform] [Activity] [Requirements]`\n"
              "• Don't leave groups mid-mission without notice\n"
              "• Respect the Raid Leader's calls during operations",
        inline=False
    )
    
    # ⚠️ Consequences
    embed.add_field(
        name="⚠️ Rule Violations",
        value="🟡 **Warning** — Minor first-time offenses\n"
              "🟠 **Mute** — Repeated disruptions or minor toxicity\n"
              "🔴 **Kick/Ban** — Severe violations, cheating, or harassment\n\n"
              "*All decisions are made by @Officer+ staff. Appeals via ticket.*",
        inline=False
    )
    
    # ✅ Footer with image
    embed.set_footer(
        text="CoopFamily • By joining, you agree to these rules",
        icon_url="https://i.imgur.com/sAnFJ4c.png"
    )
    embed.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed)

@bot.command(name='roles')
@commands.has_permissions(manage_messages=True)
async def send_roles(ctx):
    embed = discord.Embed(
        title="🎁 Select Your Roles",
        description="Click the buttons below to get your roles! Click again to remove them.\n\n**Role Pings:**",
        color=0x3498DB
    )
    
    platforms_value = ""
    for key in ["PC", "PlayStation", "Xbox"]:
        role_data = SELF_ASSIGNABLE_ROLES[key]
        platforms_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc']}\n"
    embed.add_field(name="🎮 Platforms", value=platforms_value, inline=False)
    
    playstyle_value = ""
    for key in ["PvE-Hardcore", "PvE-Casual", "BattlePass-Grind"]:
        role_data = SELF_ASSIGNABLE_ROLES[key]
        playstyle_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc']}\n"
    embed.add_field(name="⚔️ Playstyle", value=playstyle_value, inline=False)
    
    notifications_value = ""
    for key in ["Ping-Events", "Ping-LFG"]:
        role_data = SELF_ASSIGNABLE_ROLES[key]
        notifications_value += f"{role_data['emoji']} <@&{role_data['id']}> — {role_data['desc']}\n"
    embed.add_field(name="🔔 Notifications", value=notifications_value, inline=False)
    
    embed.add_field(
        name="⚠️ Restricted Roles",
        value="`Leader` `Officer` `Veteran` — Assigned by administrators only",
        inline=False
    )
    
    embed.set_footer(text="CoopFamily • Click buttons to self-assign roles", icon_url="https://i.imgur.com/sAnFJ4c.png")
    embed.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed, view=RoleSelectView())

@bot.command(name='help')
@commands.has_permissions(manage_messages=True)
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 CoopFamily Bot Commands",
        description="Here are all available commands for the server.",
        color=0x3498DB
    )
    embed.add_field(name="🛠️ Server Setup", value="`!setup` — Create roles & channels (Admin)", inline=False)
    embed.add_field(
        name="📢 Messages", 
        value="`!welcome` — Send welcome message\n`!rules` — Send server rules\n`!roles` — Send role panel\n`!help` — Show this menu",
        inline=False
    )
    embed.add_field(name="🏓 Utilities", value="`!ping` — Check bot latency", inline=False)
    embed.set_footer(text="CoopFamily Bot v1.3", icon_url="https://i.imgur.com/sAnFJ4c.png")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Bot latency: **{latency}ms**", color=0x2ECC71)
    embed.set_footer(icon_url="https://i.imgur.com/sAnFJ4c.png")
    await ctx.send(embed=embed)

# --- ОБРАБОТКА ОШИБОК ---
@setup_server.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Administrator** permissions!")
    else:
        await ctx.send(f"❌ Error: {error}")

@send_welcome.error
@send_rules.error
@send_roles.error
async def perm_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Manage Messages** permissions!")
    else:
        await ctx.send(f"❌ Error: {error}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    try:
        print("🚀 Starting CoopFamily Bot v1.3...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Check DISCORD_TOKEN.")
    except Exception as e:
        print(f"❌ Error: {e}")
