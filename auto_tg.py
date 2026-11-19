import os
from telethon.sessions import StringSession
from telethon import TelegramClient, events
import asyncio
import random

# ==========================================
# ISI DATA KAMU DI SINI
# ==========================================
api_id = 30926385  # Ganti dengan API ID kamu (angka)
api_hash = 'd8966ae348811966dfa86d594421e8b1' # Ganti dengan API Hash kamu

# Daftar Grup (Bisa tambah lebih dari satu, pisahkan dengan koma)
daftar_grup = [
    -1002698177375,-1002319391976,-1001607582097,-1001487018151,-1001545495459,-1001487018151,-1002220417522,-1001782699823,
    -1001211846518,-1001564240791,
]

# TEKS PROMOSI (FORMAT HTML 100%)
pesan_promosi = """ ┈➤ <b>BUTUH BOOST SOSMED, APP PREMIUM & NOKOS? SEMUA ADA!</b> 
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
<code>Part Of</code>
╰┈➤ <code>@Cozhua</code>

<blockquote><b>📱 JASA SOSMED:</b>
➤ Followers IG & TikTok
➤ Likes IG
➤ SUBS YOUTUBE
➤ VIEWS YOUTUBE</blockquote>

<blockquote><b>💎 APP PREMIUM:</b>
➤ Telegram Premium
➤ Telegram Stars
➤ Capcut Pro & Canva Pro
➤ VIU Private
➤ Netflix</blockquote>

<blockquote><b>👥 KEBUTUHAN GRUP:</b>
➤ MEMBER GRUP WA
➤ MEMBER CHANNEL WA
➤ REACT CHANNEL WA
➤ MEMBER GRUP TELEGRAM
➤ MEMBER CHANNEL TELEGRAM</blockquote>

<b>📱 OTHER APPS</b>
➤ CHATGPT 
➤ VPN 
➤ CHEAT ALL GAME
➤ TOP UP ROBUX 

<b>📞 NOKOS/OTP INSTAN:</b>
➤ Nokos WhatsApp & Telegram

━━━━━━━━━━━━━━━━━━━━━━
🛡️ <b>100% AMAN & GARANSI</b>
⚡ <b>PROSES CEPAT & OTOMATIS</b>
💸 <b>HARGA? DIJAMIN MURAH!</b>

<b>🛒 BOT AUTO ORDER 24/7</b>
🤖 @blazeorderrrbot
📢 <a href="https://t.me/infoblazepedia/98">KLIK DISINI UNTUK CATALOG</a>

<blockquote>🎁 FREE JASTEB @cozhua</blockquote>"""

# Auto-Reply
kata_kunci = "DONE KAK" 
balasan_otomatis = "Otw kak wait yaw"
# ==========================================

print("Mencoba login ke Telegram...")
session_str = os.environ.get('TG_SESSION', '')

if session_str:
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
else:
    client = TelegramClient('sesi_bot', api_id, api_hash)

# --- FITUR AUTO-REPLY + SIMULASI MENGETIK ---
@client.on(events.NewMessage(incoming=True, pattern=f'(?i){kata_kunci}'))
async def handler_auto_reply(event):
    if event.is_group:
        print(f"[{event.chat.title}] Ada yang chat '{kata_kunci}', menyiapkan balasan...")
        
        # SIMULASI MENGETIK (2 sampai 5 detik)
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.randint(2, 5))
            
        # Tambahkan parse_mode='html' jika balasan Anda mengandung format
        await event.reply(balasan_otomatis, parse_mode='html')
        print("Balasan terkirim!")

# --- FITUR KIRIM MULTI-GRUP + SIMULASI MENGETIK ---
async def kirim_pesan_berkala():
    while True:
        for grup in daftar_grup:
            try:
                # SIMULASI MENGETIK (0 sampai 1 detik)
                async with client.action(grup, 'typing'):
                    await asyncio.sleep(random.randint(0, 1))
                
                # Kirim pesan dengan mode HTML
                await client.send_message(grup, pesan_promosi, parse_mode='html')
                print(f"Pesan promosi terkirim ke {grup}")
            except Exception as e:
                print(f"Gagal kirim ke {grup}: {e}")
            
            # Jeda antar grup (3-7 detik)
            jeda = random.randint(3, 7)
            print(f"Menunggu {jeda} detik sebelum ke grup berikutnya...")
            await asyncio.sleep(jeda)
        
        # PERBAIKAN: Tidur 300 detik (5 menit) agar sesuai dengan teks print
        print("Semua grup sudah dikirimi. Menunggu 5 menit...")
        await asyncio.sleep(300)

async def main():
    await client.start()
    print("Login Berhasil! Bot berjalan dengan Simulasi Mengetik...")
    
    # Jalankan fitur kirim pesan di latar belakang
    client.loop.create_task(kirim_pesan_berkala())
    
    # Jalankan bot untuk mendengarkan pesan masuk
    await client.run_until_disconnected()

# Mulai program
with client:
    client.loop.run_until_complete(main())
