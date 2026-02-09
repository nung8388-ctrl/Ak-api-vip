import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  


# GLOBAL SETTINGS 
RELEASEVERSION = "OB52"
MAJOR_LOGIN_CLIENT_VERSION = "1.120.2"


# ADMIN INFO FUNCTION FOR ADMIN COMMAND 
ADMIN_UID = "14444548421"
server2 = "BD"
key2 = "mg24"
BYPASS_TOKEN = "your_bypass_token_here"


# VariabLes dyli 
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
#------------------------------------------#
# NEW MG24 GAMER VARIABLES 
bot_enabled = True
Uid = None
Pw =None
spam_request_running = False
spam_request_task = None

# Badge values for s1 to s5 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 64,         # Your fourth badge
    "s5": 262144     # Your seventh badge
}
# RARE LOOK CHANGER BUNDLE ID
BUNDLE = {
    "rampage": 914000002,
    "cannibal": 914000003,
    "devil": 914038001,
    "scorpio": 914039001,
    "frostfire": 914042001,
    "paradox": 914044001,
    "naruto": 914047001,
    "aurora": 914047002,
    "midnight": 914048001,
    "itachi": 914050001,
    "dreamspace": 914051001
}
# Admin Functions
def is_admin(uid):
    return str(uid) == ADMIN_UID

# Mute Functions 
def is_off():
    return not bot_enabled

def ff_num(val):
    return xMsGFixinG(str(val)) if val not in (None, "") else "N/A"

def human_time(ts):
    try:
        ts = int(ts)
        return datetime.fromtimestamp(ts).strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

# STICKER VALUES FUNCTION 
def get_random_sticker():
    """
    Randomly select one sticker from available packs
    """

    sticker_packs = [
        # NORMAL STICKERS (1200000001-1 to 24)
        ("1200000001", 1, 24),

        # KELLY EMOJIS (1200000002-1 to 15)
        ("1200000002", 1, 15),

        # MAD CHICKEN (1200000004-1 to 13)
        ("1200000004", 1, 13),
    ]

    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)

    return f"[1={pack_id}-{sticker_no}]"

# Load emotes from JSON file (your format)
def load_emotes_from_json():
    """Load emote IDs from emotes.json file with your exact format"""
    emotes_file = "emotes.json"
    
    try:
        with open(emotes_file, 'r') as f:
            emotes_data = json.load(f)
        
        # Access using your structure: data["EMOTES"]["numbers"] and data["EMOTES"]["names"]
        number_emotes = emotes_data.get("EMOTES", {}).get("numbers", {})
        name_emotes = emotes_data.get("EMOTES", {}).get("names", {})
        
        print(f"✅ Loaded {len(number_emotes)} number emotes and {len(name_emotes)} named emotes")
        return {
            "numbers": number_emotes,
            "names": name_emotes
        }
        
    except Exception as e:
        print(f"❌ Error loading {emotes_file}: {e}")
        # Return empty dictionaries as fallback
        return {"numbers": {}, "names": {}}

# Load emotes globally
EMOTES_DATA = load_emotes_from_json()
NUMBER_EMOTES = EMOTES_DATA["numbers"]
NAME_EMOTES = EMOTES_DATA["names"]

#CHAT WITH AI
def talk_with_ai(question):
    url = f"https://princeaiapi.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."

#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://mg24-gamer-spam-api.vercel.app/send_requests?uid={player_id}&region=bd"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."

def get_player_info(uid):
    try:
        url = f"https://info-api-mg24-pro.vercel.app/get?uid={uid}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return None, f"API Error: {res.status_code}"

        data = res.json()

        # basic validation
        if "AccountInfo" not in data:
            return None, "Invalid API response"

        return data

    except requests.exceptions.Timeout:
        return None, "Request timeout"

    except Exception as e:
        return None, str(e)

# ADD FRIEND 
def add_friend(uid, pw, target_uid):
    try:
        url = (
            "https://danger-friend-manager.vercel.app/adding_friend"
            f"?uid={Uid}&password={Pw}&friend_uid={target_uid}"
        )

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return "[C][B][FF5C8A]API ERROR"

        data = res.json()

        success = data.get("success", False)
        name = data.get("nickname", "Unknown")
        region = data.get("region", "N/A")
        friend_uid = data.get("friend_uid", target_uid)

        if success:
            status_color = "4CFFB0"
            status_text = "FRIEND ADDED"
        else:
            status_color = "FF5C8A"
            status_text = "FAILED"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]FRIEND MANAGER
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Action   : [{status_color}]{status_text}
[C][E6E6FA]Bot Name     : [9AD0FF]{name}
[C][E6E6FA]Target Uid : [9AD0FF]{xMsGFixinG(friend_uid)}
[C][E6E6FA]Region   : [9AD0FF]{region}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[C][B][FF5C8A]ERROR: {e}"

def remove_friend(uid, pw, target_uid):
    try:
        url = (
            "https://danger-friend-manager.vercel.app/remove_friend"
            f"?uid={Uid}&password={Pw}&friend_uid={target_uid}"
        )

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return "[C][B][FF5C8A]API ERROR"

        data = res.json()

        success = data.get("success", False)
        name = data.get("nickname", "Unknown")
        region = data.get("region", "N/A")
        friend_uid = data.get("friend_uid", target_uid)

        if success:
            status_color = "FF6EC7"
            status_text = "FRIEND REMOVED"
        else:
            status_color = "FF5C8A"
            status_text = "FAILED"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]FRIEND MANAGER
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Action   : [{status_color}]{status_text}
[C][E6E6FA]Bot Name     : [9AD0FF]{name}
[C][E6E6FA]Target Uid : [9AD0FF]{xMsGFixinG(friend_uid)}
[C][E6E6FA]Region   : [9AD0FF]{region}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[C][B][FF5C8A]ERROR: {e}"

#GET PLAYER BIO 
def get_player_bio(uid):
    try:
        url = f"https://info-api-mg24-pro.vercel.app.vercel.app/get?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Bio is inside socialInfo -> signature
            bio = data.get('socialinfo', {}).get('signature', 'No Bio Found')
            if bio:
                return bio
            else:
                return "No bio available"
        else:
            return f"Failed to fetch bio. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

def check_ban(uid):
    try:
        url = f"https://mg24-ban-check.vercel.app/ban?uid={uid}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return "[B][C][FF0000]❌ API ERROR"

        data = res.json()

        name = data.get("nickname", "Unknown")
        account_id = data.get("account_id", uid)
        region = data.get("region", "N/A")
        status = data.get("ban_status", "Unknown")
        period = data.get("ban_period") or "No Ban"

        status_lower = status.lower()

        # ✅ SIMPLE + SAFE RULE
        if "not" in status_lower:
            status_color = "66FF00"
            period_color = "66FF00"
        else:
            status_color = "FF4444"
            period_color = "FF4444"

        return f"""
[C][B][5DA9FF]━━━━━━━━━━━━━
[C][B][FF6EC7]BAN STATUS CHECK
[C][5DA9FF]━━━━━━━━━━━━━
[C][E6E6FA]Name    : [9AD0FF]{name}
[C][E6E6FA]UID     : [9AD0FF]{xMsGFixinG(account_id)}
[C][E6E6FA]Region  : [9AD0FF]{region}
[C][E6E6FA]Status  : [{status_color}]{status}
[C][E6E6FA]Period  : [{period_color}]{period}
[C][B][5DA9FF]━━━━━━━━━━━━━
"""

    except Exception as e:
        return f"[B][C][FF0000]❌ Error: {e}"

async def send_full_player_info(data, chat_type, uid, chat_id, key, iv):

    acc = data.get("AccountInfo", {})
    guild = data.get("GuildInfo", {})
    social = data.get("socialinfo", {})
    captain = data.get("captainBasicInfo", {})

    # ────────── MESSAGE 1 : COMMON ACCOUNT INFO ──────────
    msg1 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]COMMON ACCOUNT INFO
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Name      : [66FF00]{acc.get('AccountName', 'N/A')}
[C][FFFFFF]UID       : [66FF00]{ff_num(captain.get('accountId'))}
[C][FFFFFF]Level     : [66FF00]{acc.get('AccountLevel', 'N/A')}
[C][FFFFFF]EXP       : [66FF00]{ff_num(acc.get('AccountEXP'))}
[C][FFFFFF]Likes     : [66FF00]{ff_num(acc.get('AccountLikes'))}
[C][FFFFFF]Region    : [66FF00]{acc.get('AccountRegion', 'N/A')}
[C][FFFFFF]BP Badge  : [66FF00]{ff_num(acc.get('AccountBPID'))}
[C][FFFFFF]Version   : [66FF00]{acc.get('ReleaseVersion', 'N/A')}
"""

    await safe_send_message(chat_type, msg1, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 2 : DATE + RANK INFO ──────────
    lang = social.get("language", "N/A")
    if "_" in lang:
        lang = lang.split("_")[-1]   # ARABIC, ENGLISH
    msg2 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]ACCOUNT DETAILS
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Create Date : [66FF00]{human_time(acc.get('AccountCreateTime'))[:16]}
[C][FFFFFF]Last Login  : [66FF00]{human_time(acc.get('AccountLastLogin'))[:16]}
[C][FFFFFF]BR Max Rank     : [66FF00]{ff_num(acc.get('BrMaxRank'))}
[C][FFFFFF]BR Points   : [66FF00]{ff_num(acc.get('BrRankPoint'))}
[C][FFFFFF]CS Max Rank     : [66FF00]{ff_num(acc.get('CsMaxRank'))}
[C][FFFFFF]CS Points   : [66FF00]{ff_num(acc.get('CsRankPoint'))}
[C][FFFFFF]Language    : [66FF00]{lang}
"""

    await safe_send_message(chat_type, msg2, uid, chat_id, key, iv)
    await asyncio.sleep(0.5)

    # ────────── MESSAGE 3 : FULL GUILD INFO ──────────
    msg3 = f"""
[C][B][FFAA00]━━━━━━━━━━━━━
[C][B][FFFFFF]GUILD INFORMATION
[C][FFAA00]━━━━━━━━━━━━━
[C][FFFFFF]Guild Name   : [66FF00]{guild.get('GuildName', 'No Guild')}
[C][FFFFFF]Guild ID     : [66FF00]{ff_num(guild.get('GuildID'))}
[C][FFFFFF]Owner UID    : [66FF00]{ff_num(guild.get('GuildOwner'))}
[C][FFFFFF]Guild Level  : [66FF00]{guild.get('GuildLevel', 'N/A')}
[C][FFFFFF]Members      : [66FF00]{guild.get('GuildMember', '0')}/{guild.get('GuildCapacity', '0')}
"""

    await safe_send_message(chat_type, msg3, uid, chat_id, key, iv)

#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://your-like-api.vercel.app/like?uid={uid}&server_name=bd",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]MG24 GAMER [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': RELEASEVERSION
    }

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

def replace_color_keywords(text):
    colors = {
        "[red]": "[FF0000]", "[green]": "[00FF00]", "[blue]": "[0000FF]",
        "[yellow]": "[FFFF00]", "[pink]": "[FF00FF]", "[cyan]": "[00FFFF]",
        "[white]": "[FFFFFF]", "[bold]": "[B]", "[br]": "\n", "[italic]": "[I]"
    }
    for key, val in colors.items():
        text = text.replace(key, val)
        text = text.replace(key.upper(), val)
    return text

# ---- Random Avatar ----
async def get_random_avatar():
    await asyncio.sleep(0)  # makes it async but instant
    avatar_list = [
        '902042010', '902037031', '902042010', '902037031', '902042010',
        '902037031', '902042010', '902037031', '902042010', '902037031'
    ]
    return random.choice(avatar_list)

# SAFE MESSAGE SEND
async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False

# ACCEPT TEAM INVITE 
async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)

# BADGE JOIN REQUESTS 
async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} {xMsGFixinG(int(123456789))}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {xMsGFixinG(target_uid)}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Reset bot state
        await reset_bot_state(key, iv, region)
        
        # Create and send join packets
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 3
        
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.1)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent {spam_count} Join Requests!\n🎯 Target: {xMsGFixinG(target_uid)}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

# STICKER SEND FUNCTION 
async def send_sticker(target_uid, chat_id, key, iv, nickname="MG24"):
    """Send Random Sticker using /sticker command"""
    try:
        sticker_value = get_random_sticker()

        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(get_random_avatar()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 66,
                    12: 66,
                    13: {1: 2},
                    14: {
                        1: 1158053040,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }

        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()

        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"

        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)

        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)

        print(f"✅ Sticker Sent: {sticker_value}")
        return final_packet

    except Exception as e:
        print(f"❌ Sticker error: {e}")
        return None

async def bundle_packet_async(bundle_id, key, iv, region="ind"):
    """Create bundle packet"""
    fields = {
        1: 88,
        2: {
            1: {
                1: bundle_id,
                2: 1
            },
            2: 2
        }
    }
    
    # Use your CrEaTe_ProTo function
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use your encrypt_packet function
    encrypted = await encrypt_packet(packet_hex, key, iv)
    
    # Use your DecodE_HeX function
    header_length = len(encrypted) // 2
    header_length_hex = await DecodE_HeX(header_length)
    
    # Build final packet based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    
    # Determine header based on length
    if len(header_length_hex) == 2:
        final_header = f"{packet_type}000000"
    elif len(header_length_hex) == 3:
        final_header = f"{packet_type}00000"
    elif len(header_length_hex) == 4:
        final_header = f"{packet_type}0000"
    elif len(header_length_hex) == 5:
        final_header = f"{packet_type}000"
    else:
        final_header = f"{packet_type}000000"
    
    final_packet_hex = final_header + header_length_hex + encrypted
    return bytes.fromhex(final_packet_hex)

# CHANGE BOT ACCOUNT BIO
async def update_player_bio(uid, password, bio_text):
    formatted_bio = replace_color_keywords(bio_text)
    encoded_bio = quote(formatted_bio)
    
    # URL structure exactly as per your requirement
    api_url = f"https://long-bio-mg24.vercel.app/bio_upload?uid={uid}&pass={password}&bio={encoded_bio}"
    
    try:
        # SSL verify=False is used to prevent certificate errors on some environments
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(api_url, timeout=20) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Check if API returned success code
                    if data.get("code") == 200 or data.get("status") == "✅ Success":
                        return True, "Success"
                    else:
                        return False, data.get("status", "API Rejected Request")
                return False, f"Server HTTP Error: {resp.status}"
    except Exception as e:
        return False, f"System Error: {str(e)}"

# BADGE JOIN REQUESTS FUNCTION 
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Send join request with specific badge - converted from your old TCP"""
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] KRISHNA",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value  # Dynamic badge value
            },
            32: badge_value,    # Dynamic badge value
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    

async def spam_request_loop(target_uid, key, iv, region):
    """Spam request function that creates group and sends join requests in loop - FIXED VERSION"""
    global spam_request_running
    count = 0
    max_requests = 30  # Send exactly 30 requests
    
    while spam_request_running and count < max_requests:
        try:
            # Create squad
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.3)  # Increased delay for stability
            
            # Send invite
            V = await SEnd_InV(5, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            await asyncio.sleep(0.3)  # Increased delay for stability
            
            # Leave squad
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            
            count += 1
            print(f"Sent request #{count} to {target_uid}")
            
            # Delay between requests
            await asyncio.sleep(0.8)  # Increased delay for stability
            
        except Exception as e:
            print(f"Error in spam_request_loop for uid {target_uid}: {e}")
            # Continue with next request instead of breaking
            await asyncio.sleep(1)

# BOT STATE RESET FUNCTION 
async def reset_bot_state(key, iv, region):
    """Reset bot to solo mode before spam - Critical step from your old TCP"""
    try:
        # Leave any current squad (using your exact leave_s function)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Bot state reset - left squad")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting bot: {e}")
        return False    
    
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = MAJOR_LOGIN_CLIENT_VERSION
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019116753"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 
           
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):  
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave, mute_until, bot_enabled  
    while True:  
        try:  
            reader , writer = await asyncio.open_connection(ip, int(port))  
            online_writer = writer  
            bytes_payload = bytes.fromhex(AutHToKen)  
            online_writer.write(bytes_payload)  
            await online_writer.drain()  
            while True:  
                data2 = await reader.read(9999)  
                if not data2: break  
                  
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:  
                    try:  
                        print(data2.hex()[10:])  
                        packet = await DeCode_PackEt(data2.hex()[10:])  
                        print(packet)  
                        packet = json.loads(packet)  
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)  
  
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)  
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)  
  
  
                        time.sleep(0.5)  
                        message = '[00FF00]WELCOME !!'  
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)  
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)  
  
                    except:  
                        if data2.hex().startswith('0500') and len(data2.hex()) > 1000:  
                            try:  
                                print(data2.hex()[10:])  
                                packet = await DeCode_PackEt(data2.hex()[10:])  
                                print(packet)  
                                packet = json.loads(packet)  
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)  
  
                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)  
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)  
  
  
                                time.sleep(0.5)  
                                message = f'Cool outfit!'  
                                P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)  
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)  
                            except:  
                                pass  
  
            online_writer.close() ; await online_writer.wait_closed() ; online_writer = None  
  
        except Exception as e: print(f"- ErroR With {ip}:{port} - {e}") ; online_writer = None  
        await asyncio.sleep(reconnect_delay)  

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, online_writer, chat_id, XX, uid, Spy, data2, Chat_Leave, bot_enabled, spam_request_running, spam_request_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        MsG = response.Data.msg.lower()
                    except:
                        response = None
                    if response:

                        # ========= ON =========
                        if inPuTMsG.startswith('/on'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "❌ Only admin can use /on", uid, chat_id, key, iv)
                                continue

                            bot_enabled = True
                            await safe_send_message(response.Data.chat_type, "✅ Bot is now ON", uid, chat_id, key, iv)
                            continue


                        # ========= OFF =========
                        if inPuTMsG.startswith('/off'):
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "❌ Only admin can use /off", uid, chat_id, key, iv)
                                continue

                            bot_enabled = False
                            await safe_send_message(response.Data.chat_type, "⛔ Bot is now OFF", uid, chat_id, key, iv)
                            continue


                        # ========= BLOCK WHEN OFF (ONLY HERE) =========
                        if not bot_enabled:
                            await safe_send_message(response.Data.chat_type, "⛔ Bot is OFF", uid, chat_id, key, iv)
                            continue

                        # ========= ADD BIO COMMAND =========
                        if inPuTMsG.startswith('/add_bio'):
                            global Uid, Pw # Ensure these are accessible
                            
                            if not is_admin(uid):
                                await safe_send_message(response.Data.chat_type, "❌ Admin Only!", uid, chat_id, key, iv)
                                continue

                            if not Uid or not Pw:
                                await safe_send_message(response.Data.chat_type, "❌ Error: Bot UID/Pass not loaded!", uid, chat_id, key, iv)
                                continue

                            parts = inPuTMsG.split(' ', 1)
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "❌ Usage: /add_bio [red]Text", uid, chat_id, key, iv)
                                continue
                            
                            bio_to_set = parts[1]
                            # Sending initial processing message
                            await safe_send_message(response.Data.chat_type, "[B][C][FFFF00]⏳ Updating... Please wait.", uid, chat_id, key, iv)

                            try:
                                # Call the update function
                                success, result_msg = await update_player_bio(Uid, Pw, bio_to_set)
                                
                                if success:
                                    preview = replace_color_keywords(bio_to_set)
                                    final_msg = f"[B][C][00FF00]✅ Bio Updated!\n[C]{preview}"
                                else:
                                    final_msg = f"[B][C][FF0000]❌ Failed: {result_msg}"
                                
                                await safe_send_message(response.Data.chat_type, final_msg, uid, chat_id, key, iv)
                            except Exception as cmd_err:
                                await safe_send_message(response.Data.chat_type, f"❌ Crash: {str(cmd_err)}", uid, chat_id, key, iv)
                            continue

                        # NEW COMMAND-/sticker
                        if MsG.strip().startswith('/emoji'):
                            packet = await send_sticker(uid, chat_id, key, iv)                   
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', packet)

                                #GET PLAYER LIKE
                        if inPuTMsG.strip().startswith('/like'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /like <uid>\nExample: /like 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending Likes...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                like_result = send_likes(target_uid)

                                await safe_send_message(response.Data.chat_type, like_result, uid, chat_id, key, iv)

                                #GET PLAYER LIKE
                        if inPuTMsG.strip().startswith('/check'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /check <uid>\nExample: /check 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nChecking Ban Status...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                ban_result = check_ban(target_uid)

                                await safe_send_message(response.Data.chat_type, ban_result, uid, chat_id, key, iv)

                                #GET PLAYER BIO-/bio
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching the player bio...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)


                                bio_result = get_player_bio(target_uid)

                                await safe_send_message(response.Data.chat_type, f"[B][C]{get_random_color()}\n{bio_result}", uid, chat_id, key, iv)

# ================= BUNDLE COMMAND START =================
   # ================= FINAL BUNDLE COMMAND (FAST) =================
                        if inPuTMsG.strip().startswith('/bundle'):
                            print('Processing bundle command')
    
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                                # Show available bundles
                                bundle_list = """[B][C][00FF00]🎁 AVAILABLE BUNDLES 🎁
[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FFFFFF]• midnight
[FFFFFF]• aurora
[FFFFFF]• naruto  
[FFFFFF]• paradox
[FFFFFF]• frostfire
[FFFFFF]• rampage
[FFFFFF]• cannibal
[FFFFFF]• devil
[FFFFFF]• scorpio
[FFFFFF]• dreamspace
[FFFFFF]• itachi
[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[00FF00]Usage: /bundle [name]
[FFFFFF]Example: /bundle midnight"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
        
                                # All bundles use the same ID: 914000002
                                bundle_id = BUNDLE.get(bundle_name)
        
                                initial_msg = f"[B][C][00FF00]🎁 Sending {bundle_name}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create bundle packet
                                    bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
            
                                    if bundle_packet and online_writer:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_packet)
                                        success_msg = f"[B][C][00FF00]✅ Done: {bundle_name}"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ Failed to create bundle packet!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error sending bundle: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                                #GET PLAYER INFO
                        if inPuTMsG.strip().startswith('/info'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /info <uid>\nExample: /info 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGetting Player Info...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                info_data = get_player_info(target_uid)

                                await send_full_player_info(info_data, response.Data.chat_type, uid, chat_id, key, iv)

                                #GET PLAYER SPAM
                        if inPuTMsG.strip().startswith('/spam_req'):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /spam_req <uid>\nExample: /spam_req 436🤫856🤫97🤫33\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending Requests...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                spam_result = spam_requests(target_uid)

                                await safe_send_message(response.Data.chat_type, spam_result, uid, chat_id, key, iv)

                        # AI Command - /ai
                        if inPuTMsG.strip().startswith('/ai '):
                            print('Processing AI command in any chat type')
                            
                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}\n🤖 AI is thinking...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                ai_response = await talk_with_ai(question)
                                
                                # Format the AI response
                                ai_message = f"""
[B][C][00FF00]🤖 AI Response:

[00FFFF]{ai_response}

[C][B][FFB300]Question: [FFFFFF]{question}
"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Please provide a question after /ai\nExample: /ai What is Free Fire?\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                                #TEAM SPAM MESSAGE COMMAND
                        if inPuTMsG.strip().startswith('/ms '):
                            print('Processing /ms command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/ms <message>\n"
                                        "Example: /ms MG24 GAMER"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(30):
                                        color = get_random_color()  # random color from your list
                                        colored_message = f"[B][C]{color} {user_message}"  # correct format
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # PLAYER INVITE 
                        if inPuTMsG.strip().startswith('/inv'):
                            print('Processing invite command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Sending Team Invite To {xMsGFixinG(target_uid)}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:

                                    V = await SEnd_InV(4, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)

                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # FIXED Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spam_inv'):
                            print('Processing spam request in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f" [C][FF0000]❌ ERROR! Usage: /spm_inv (uid)\nExample: /spm_inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    
                                    # Stop any existing spam request
                                    if spam_request_task and not spam_request_task.done():
                                        spam_request_running = False
                                        spam_request_task.cancel()
                                        await asyncio.sleep(0.5)
                                    
                                    # Start new spam request
                                    spam_request_running = True
                                    spam_request_task = asyncio.create_task(spam_request_loop(target_uid, key, iv, region))
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f" [C][00FF00]✅ SUCCESS! Spam request started!\nTarget: {target_uid}\nRequests: 30\nSpeed: Fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f" [C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith(('/add ', '/remove ')):

                            parts = inPuTMsG.strip().split()

                            if not Uid or not Pw:
                                await safe_send_message(response.Data.chat_type, "❌ Error: Bot UID/Pass not loaded!", uid, chat_id, key, iv)
                                continue

                            if len(parts) < 2:
                                error_msg = (
                                    "[C][B][FF5C8A]USAGE ERROR\n"
                                    "[C][E6E6FA]/add <uid>\n"
                                    "[C][E6E6FA]/remove <uid>"
                                )
                                await safe_send_message(
                                    response.Data.chat_type,
                                    error_msg,
                                    uid,
                                    chat_id,
                                    key,
                                    iv
                                )
                                return

                            cmd = parts[0].lower()
                            target_uid = parts[1]

                            wait_msg = (
                                "[C][B][5DA9FF]━━━━━━━━━━━━━\n"
                                "[C][FF6EC7]FRIEND MANAGER\n"
                                "[C][E6E6FA]Processing request...\n"
                                "[C][5DA9FF]━━━━━━━━━━━━━"
                            )
                            await safe_send_message(
                                response.Data.chat_type,
                                wait_msg,
                                uid,
                                chat_id,
                                key,
                                iv
                            )

                            if cmd == "/add":
                                result = add_friend(uid, Pw, target_uid)

                            elif cmd == "/remove":
                                result = remove_friend(uid, Pw, target_uid)

                            else:
                                result = "[C][B][FF5C8A]UNKNOWN COMMAND"

                            await safe_send_message(
                                response.Data.chat_type,
                                result,
                                uid,
                                chat_id,
                                key,
                                iv
                            )

                        if inPuTMsG.startswith(("/5")):
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nAccepT My Invitation FasT\n\n"
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                C = await cHSq(5, uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                E = await ExiT(None , key , iv)
                                await asyncio.sleep(3)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , E)
                            except:
                                print('msg in squad')

                        # Individual command handlers for /s1 to /s5
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s5'):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                            #ALL BADGE SPAM REQUEST 
                        if inPuTMsG.strip().startswith('/spam_join'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spam_join <uid>\nExample: /spam_join {xMsGFixinG(int(123456789))}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                total_requests = 10  # total join requests
                                sequence = ['s1', 's2', 's3', 's4', 's5']  # all badge commands

                                # Send initial consolidated message
                                initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {xMsGFixinG(target_uid)} with all badges...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                count = 0
                                while count < total_requests:
                                    for cmd in sequence:
                                        if count >= total_requests:
                                            break
                                        # Build a fake command string like "/s1 {xMsGFixinG(int(123456789))}"
                                        fake_command = f"/{cmd} {xMsGFixinG(target_uid)}"
                                        await handle_badge_command(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        count += 1

                                # Success message after all 30 requests
                                success_msg = f"[B][C][00FF00]✅ Successfully sent {total_requests} Join Requests!\n🎯 Target: {xMsGFixinG(target_uid)}\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/e'):
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
    
                            parts = inPuTMsG.strip().split()
    
                            # Check if user wants to list emotes or show help
                            if len(parts) == 1 or (len(parts) == 2 and parts[1].lower() == 'list'):
                                # Show available emotes
                                emote_list_msg = f"[B][C][00FF00]🎭 EMOTE SYSTEM\n"
                                emote_list_msg += f"[FFFFFF]────────────────\n"
                                emote_list_msg += f"[00FF00]📊 STATS:\n"
                                emote_list_msg += f"[FFFFFF]• Number emotes: 1-{len(NUMBER_EMOTES)}\n"
                                emote_list_msg += f"[FFFFFF]• Named emotes: {len(NAME_EMOTES)} names\n"
                                emote_list_msg += f"[FFFFFF]────────────────\n"
                                emote_list_msg += f"[00FF00]🎯 USAGE:\n"
                                emote_list_msg += f"[FFFFFF]/e [number/name] → Send to yourself\n"
                                emote_list_msg += f"[FFFFFF]/e [uid] [number/name] → Send to UID\n"
                                emote_list_msg += f"[FFFFFF]────────────────\n"
                                emote_list_msg += f"[00FF00]🔥 POPULAR NAMES:\n"
        
                                # Show popular named emotes
                                popular_names = ["ak", "m60", "p90", "scar", "famas", "heart", "love", "dance", "hello", "money"]
                                line = ""
                                for name in popular_names:
                                    if name.lower() in NAME_EMOTES:
                                        line += f"[00FF00]{name}[FFFFFF], "
                                if line:
                                    emote_list_msg += line.rstrip(", ") + "\n"
        
                                emote_list_msg += f"[FFFFFF]────────────────\n"
                                emote_list_msg += f"[00FF00]📖 EXAMPLES:\n"
                                emote_list_msg += f"[FFFFFF]/e ak → Send AK emote to yourself\n"
                                emote_list_msg += f"[FFFFFF]/e {xMsGFixinG(int(123456789))} heart → Send ❤️ to UID\n"
                                emote_list_msg += f"[FFFFFF]/e {xMsGFixinG(int(123456789))} 1 → Send emote #1 to UID\n"
                                emote_list_msg += f"[FFFFFF]/e ring → Send ring emote to yourself\n"
                                emote_list_msg += f"[FFFFFF]/e list names → Show all named emotes\n"
        
                                # Check if user wants detailed name list
                                if len(parts) == 2 and parts[1].lower() == 'names':
                                    emote_list_msg += f"[FFFFFF]────────────────\n"
                                    emote_list_msg += f"[00FF00]📝 ALL NAMED EMOTES:\n"
            
                                    # Show all named emotes in groups
                                    all_names = sorted(NAME_EMOTES.keys())
                                    for i in range(0, min(len(all_names), 30), 5):  # Show first 30 names
                                        group = all_names[i:i+5]
                                        emote_list_msg += f"[FFFFFF]{' | '.join(group)}\n"
            
                                    if len(all_names) > 30:
                                        emote_list_msg += f"[FFFFFF]... and {len(all_names) - 30} more\n"
        
                                await safe_send_message(response.Data.chat_type, emote_list_msg, uid, chat_id, key, iv)
                                continue
    
                            # Parse command
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e [emote_name_or_number]\n"
                                error_msg += f"[FFFFFF]Examples:\n"
                                error_msg += f"[00FF00]/e ak[FFFFFF] → AK emote to yourself\n"
                                error_msg += f"[00FF00]/e {xMsGFixinG(int(123456789))} heart[FFFFFF] → ❤️ to UID\n"
                                error_msg += f"[00FF00]/e {xMsGFixinG(int(123456789))} 1[FFFFFF] → Emote #1 to UID\n"
                                error_msg += f"[00FF00]/e ring[FFFFFF] → Send ring emote to yourself\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
    
                            # Show "preparing" message
                            initial_message = f'[B][C]{get_random_color()}\n🎭 Preparing emote...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            target_uids = []
                            emote_key = None
    
                            try:
                                # Determine if last part is emote key (could be number or name)
                                last_part = parts[-1].lower()
        
                                # Check if last part is an emote (number or name)
                                # Note: Your numbers go up to 417, so check for 3-digit numbers too
                                is_number = last_part.isdigit() and last_part in NUMBER_EMOTES
                                is_name = last_part in NAME_EMOTES
        
                                if is_number or is_name:
                                    # Case 1: /e ak or /e 1 (only emote - send to sender)
                                    if len(parts) == 2:
                                        emote_key = last_part
                                        target_uids.append(int(response.Data.uid))
            
                                    # Case 2: /e {xMsGFixinG(int(123456789))} heart (UID + emote)
                                    elif len(parts) == 3:
                                        target_uids.append(int(parts[1]))
                                        emote_key = last_part
            
                                    # Case 3: /e 111 222 333 ak (multiple UIDs + emote)
                                    else:
                                        for i in range(1, len(parts) - 1):
                                            target_uids.append(int(parts[i]))
                                        emote_key = last_part
                                else:
                                    # Last part is not a valid emote
                                    error_msg = f"[B][C][FF0000]❌ Invalid emote: '{last_part}'\n"
                                    error_msg += f"[FFFFFF]Use numbers (1-{len(NUMBER_EMOTES)}) or names like 'ak', 'heart', 'dance', 'ring'\n"
                                    error_msg += f"[FFFFFF]Use /e list names to see all available names\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
        
                                # Get emote ID from either number or name dictionary
                                emote_id = None
                                emote_name_display = None
                                
                                if is_number:
                                    # Number-based emote
                                    emote_id = NUMBER_EMOTES.get(emote_key)
                                    emote_name_display = f"#{emote_key}"
                                else:
                                    # Name-based emote
                                    emote_id = NAME_EMOTES.get(emote_key)
                                    emote_name_display = emote_key
        
                                if not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ Emote '{emote_name_display}' not found!\n"
                                    if emote_key.isdigit():
                                        error_msg += f"[FFFFFF]Available numbers: 1-{len(NUMBER_EMOTES)}\n"
                                    else:
                                        error_msg += f"[FFFFFF]Use /e list names to see all available names\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
        
                                # Send emotes
                                success_count = 0
                                failed_uids = []
        
                                for target_uid in target_uids:
                                    try:
                                        H = await Emote_k(target_uid, int(emote_id), key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        success_count += 1
                                        await asyncio.sleep(0.1)
                                    except Exception as e:
                                        print(f"Error sending emote to {xMsGFixinG(target_uid)}: {e}")
                                        failed_uids.append(str(target_uid))
        
                                # Success message
                                if success_count > 0:
                                    if target_uids[0] == int(response.Data.uid):
                                        target_list = "Yourself"
                                    elif len(target_uids) == 1:
                                        target_list = str(target_uids[0])
                                    else:
                                        target_list = f"{len(target_uids)} players"
            
                                    success_msg = f"[B][C][00FF00]✅ EMOTE SENT!\n"
                                    success_msg += f"[FFFFFF]────────────────\n"
                                    success_msg += f"[00FF00]🎭 Emote: {emote_name_display}\n"
                                    success_msg += f"[00FF00]🆔 ID: {emote_id}\n"
                                    success_msg += f"[00FF00]👤 Target: {target_list}\n"
                                    success_msg += f"[00FF00]📊 Status: {success_count}/{len(target_uids)} successful\n"
            
                                    if failed_uids:
                                        success_msg += f"[FF0000]❌ Failed: {', '.join(failed_uids)}\n"
            
                                    success_msg += f"[FFFFFF]────────────────\n"
            
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                else:
                                    error_msg = f"[B][C][FF0000]❌ Failed to send emote to any target!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                            except ValueError as ve:
                                print("ValueError:", ve)
                                error_msg = f"[B][C][FF0000]❌ Invalid format!\n"
                                error_msg += f"[FFFFFF]UIDs must be numbers (like {xMsGFixinG(int(123456789))})\n"
                                error_msg += f"[FFFFFF]Examples: /e ak, /e {xMsGFixinG(int(123456789))} heart, /e 1, /e ring\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            except Exception as e:
                                print(f"Error processing /e command: {e}")
                                error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    

                        # In your TcPChaT function, add this command handler:
                        if inPuTMsG.strip().startswith('/dm'):
                            print('Processing private message command')
    
                            parts = inPuTMsG.strip().split(maxsplit=2)  # maxsplit=2 to keep message together
    
                            if len(parts) < 3:
                                error_msg = f"""[B][C][FF0000]❌ Usage: /dm (target_uid) (message)
        
📝 Examples:
/dm {xMsGFixinG(int(123456789))} Hello!
/dm {xMsGFixinG(int(123456789))} How are you?
/dm {xMsGFixinG(int(123456789))} Let's play together!

🔧 What it does:
• Sends private message to specified UID
• Works even if target is not in your squad
• Bot sends message from its account
• Target sees message in private chat
"""
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            target_uid = parts[1]
                            message = parts[2]
                            message_text = f"[B]{message}"
                            
                            # Validate target UID
                            if not target_uid.isdigit() or len(target_uid) < 8:
                                error_msg = f"[B][C][FF0000]❌ Invalid UID! Must be 8+ digits\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Validate message length
                            if len(message_text) > 100:
                                error_msg = f"[B][C][FF0000]❌ Message too long! Max 100 characters\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                return
    
                            # Send initial confirmation
                            initial_msg = f"[B][C][00FF00]📩 SENDING PRIVATE MESSAGE\n"
                            initial_msg += f"👤 To: {xMsGFixinG(target_uid)}\n"
                            initial_msg += f"📝 Message: {message_text[:30]}...\n"
                            initial_msg += f"⏳ Sending...\n"
    
                            await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
    
                            try:
                                # Get bot's UID from login data
                                bot_uid = 13888885520
        
                                # Create the private message packet
                                # Tp = 2 (Private message)
                                # Tp2 = target_uid (recipient)
                                # id = bot_uid (sender)
                                private_msg_packet = await xSEndMsg(
                                    Msg=message_text,
                                    Tp=2,  # 2 = Private message
                                    Tp2=int(target_uid),  # Recipient UID
                                    id=int(bot_uid),  # Sender UID (your bot)
                                    K=key,
                                    V=iv
                                )
        
                                if private_msg_packet and whisper_writer:
                                    # Send via Whisper connection (chat connection)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', private_msg_packet)
            
                                    success_msg = f"""[B][C][00FF00]✅ PRIVATE MESSAGE SENT!

👤 To: {xMsGFixinG(target_uid)}
📝 Message: {message_text}
✅ Status: Delivered

💡 Target will see this in their private messages!
"""
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Private message sent to {xMsGFixinG(target_uid)}: {message_text}")
                                else:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create message packet!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
            
                            except Exception as e:
                                print(f"❌ Private message error: {e}")
                                error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        if inPuTMsG.startswith('/x/'):
                            CodE = inPuTMsG.split('/x/')[1]
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                EM = await GenJoinSquadsPacket(CodE , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)


                            except:
                                print('msg in squad')

                        if inPuTMsG.startswith('/exit'):
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

                        if inPuTMsG.strip().startswith('/s'):
                            EM = await FS(key , iv , region)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

                        if inPuTMsG.strip().startswith('@a'):

                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nCommand Available OnLy In Team Chat Section! \n\n"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except:
                                print('msg in Team')

                                parts = inPuTMsG.strip().split()
                                print(response.Data.chat_type, uid, chat_id)
                                message = f'122809569'

                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)

                                uid2 = uid3 = uid4 = uid5 = None
                                s = False

                                try:
                                    uid = int(parts[1])
                                    uid2 = int(parts[2])
                                    uid3 = int(parts[3])
                                    uid4 = int(parts[4])
                                    uid5 = int(parts[5])
                                    idT = int(parts[5])

                                except ValueError as ve:
                                    print("ValueError:", ve)
                                    s = True

                                except Exception:
                                    idT = len(parts) - 1
                                    idT = int(parts[idT])
                                    print(idT)
                                    print(uid)

                                if not s:
                                    try:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                        H = await Emote_k(uid, idT, key, iv,region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)

                                        if uid2:
                                            H = await Emote_k(uid2, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid3:
                                            H = await Emote_k(uid3, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid4:
                                            H = await Emote_k(uid4, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid5:
                                            H = await Emote_k(uid5, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        

                                    except Exception as e:
                                        pass

                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "hello", "hi"):

                            header = f"[C][B][FF1493]Hey User Welcome To [00FFAA]MG24 GAMER's BOT"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu1 = """[C][B][FFD700]═══⚡ TEAM & BASIC ⚡═══
[00FF00]01. /help [FFFFFF]--> Show Help Menu
[32CD32]0🤫2🤫. /3 [FFFFFF]--> 🤫3 Player Team
[228B22]0🤫3🤫. /5 [FFFFFF]--> 🤫5 Player Team
[008000]0🤫4🤫. /6 [FFFFFF]--> 🤫6 Player Team
[ADFF2F]05. /join [tc] [FFFFFF]--> Join Team
[7FFF00]06. /exit [FFFFFF]--> Leave Team
[00FF7F]07. /start [FFFFFF]--> Start Match
[98FB98]08. /kick [uid] [FFFFFF]--> Kick Player
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu1, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu2 = """[C][B][800080]═══⚡ SPAM & ATTACK ⚡═══
[FF4500]09. /inv [uid] [FFFFFF]--> Invite Player
[FF6347]10. /lag [tc] [FFFFFF]--> Lag Team
[FF0000]11. /attack [tc] [FFFFFF]--> Attack Team
[DC143C]12. /spam [uid] [FFFFFF]--> Spam Join Req
[B22222]13. /spm_inv [uid] [FFFFFF]--> Spam Invite
[FF7F50]14. /ms [txt] [FFFFFF]--> Message Spam
[CD5C5C]15. /mg [txt] [FFFFFF]--> Wave Msg Spam
[E9967A]16. /dm [uid] [FFFFFF]--> Direct Message
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu2, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu3 = """[C][B][FF0000]═══⚡ EMOTE COMMANDS ⚡═══
[9370DB]17. /emote [FFFFFF]--> Show Emote List
[8A2BE2]18. /e [emt] [FFFFFF]--> Emote To Self
[9400D3]19. /e [uid] [FFFFFF]--> Emote To Player
[9932CC]20. /e [id][id][et] [FFFFFF]--> Multi Emt
[BA55D3]21. /evos [FFFFFF]--> Evo Cycle Self
[DA70D6]22. /evos [uid] [FFFFFF]--> Evo Cycle Player
[EE82EE]23. /sevos [FFFFFF]--> Stop Evo Cycle
[D8BFD8]24. /d [tc][uid][et] [FFFFFF]--> Emt No Bot
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu3, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu4 = """[C][B][00FFAA]═══⚡ EXTRA FEATURES ⚡═══
[1E90FF]25. /play [uid][id] [FFFFFF]--> Custom Emt
[00BFFF]26. /bundle [FFFFFF]--> Bundle Menu
[87CEEB]27. /bundle [name] [FFFFFF]--> Set Bundle
[00CED1]28. /gali [name] [FFFFFF]--> Gali To Friend
[40E0D0]29. /check [uid] [FFFFFF]--> Check Ban
[48D1CC]30. /info [uid] [FFFFFF]--> Player Info
[AFEEEE]31. /like [uid] [FFFFFF]--> Send Likes
[5F9EA0]32. /ai [ques] [FFFFFF]--> Chat With AI
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu4, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu5 = """[C][B][FFD700]═══⚡ PROFILE & BADGE ⚡═══
[FFD700]33. /name [uid] [FFFFFF]--> Get Name
[DAA520]34. /bio [uid] [FFFFFF]--> Get Bio
[B8860B]35. /visit [FFFFFF]--> Profile Visit
[F0E68C]36. /s1 [uid] [FFFFFF]--> Craftland Bdg
[EEE8AA]37. /s2 [uid] [FFFFFF]--> V Badge Req
[FFFACD]38. /s3 [uid] [FFFFFF]--> Moderator Bdg
[FFFFE0]39. /s4 [uid] [FFFFFF]--> Old V Badge
[FAFAD2]40. /s5 [uid] [FFFFFF]--> Pro Badge Req
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu5, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu6 = """[C][B][1E90FF]═══⚡ UTILITIES ⚡═══
[FF8C00]41. /spam_req [uid] [FFFFFF]--> Spam Req
[FFA500]42. /admin [FFFFFF]--> Admin Info
[FFDAB9]43. /store [FFFFFF]--> Parche Store
[FFE4B5]44. /title [FFFFFF]--> Rare Title
[FFEFD5]45. /emoji [FFFFFF]--> Single Emoji
[FFF8DC]46. /emoji [cnt] [FFFFFF]--> Multi Emoji
[FFE4C4]47. /ghost [tc] [FFFFFF]--> Ghost Join
[F5DEB3]48. bb_lag [tc] [FFFFFF]--> Bundle Spam
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu6, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu7 = """[C][B][FF1493]═══⚡ ADMIN ONLY ⚡═══
[FF00FF]49. /add [uid] [FFFFFF]--> Add Friend
[C71585]50. /remove [uid] [FFFFFF]--> Remove Friend
[DB7093]51. /add_bio [bio] [FFFFFF]--> Change Bio
[FF1493]52. /off [FFFFFF]--> Off Bot
[FF69B4]53. /on [FFFFFF]--> On Bot
[FFB6C1]54. /status [FFFFFF]--> Bot Status
[FA8072]55. /100 [FFFFFF]--> 100 Lvl Emt
[E9967A]56. /100 [uid] [FFFFFF]--> 100 Lvl Player
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu7, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            menu8 = """[C][B][32CD32]═══⚡ AUTOMATIC ⚡═══
[FFFFFF]57. Auto Accept Team Invite
[F0F0F0]58. Auto Reply 'noob'
[E0E0E0]59. Auto Play Ring After Join
[D0D0D0]60. Auto Ring For Inviter
[00AAFF]━━━━━━━━━━━━"""
                            await safe_send_message(response.Data.chat_type, menu8, uid, chat_id, key, iv)

                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    global Uid, Pw
    GARENA = base64.b64decode("TUcyNEdBTUVSLnR4dA==").decode('utf-8')
    
    credentials = {}
    
    if os.path.exists(GARENA):
        with open(GARENA, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key.strip()] = value.strip()
        
        Uid = credentials.get('UID')
        Pw = credentials.get('PASSWORD')
    

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("ErroR - InvaLid AccounT") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin DaTa !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    print(ToKen)
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
     
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    os.system('clear')
    print(render('MG24', colors=['white', 'red'], align='center'))
    print('')
    #print(' - ReGioN => {region}'.format(region))
    print(f" - BoT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}\n")
    print(f" - BoT sTaTus > GooD | MG24 GAMER! (:")    
    print(f" - YOUTUBE > MG24 GAMER | File by ! (:")    
    await asyncio.gather(task1 , task2)
    
async def StarTinG():
    while True:
        try: await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    asyncio.run(StarTinG())