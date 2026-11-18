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
    -1004489967653,-1003967195113,-1003789805526,-1003967195113,-1002098986854,
]

pesan_promosi = "FB/LB GERCEP DONE RC https://www.tiktok.com/@cozzhua?_r=1&_t=ZS-9BULWt86hdc"

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
            
        await event.reply(balasan_otomatis)
        print("Balasan terkirim!")

# --- FITUR KIRIM MULTI-GRUP + SIMULASI MENGETIK ---
async def kirim_pesan_berkala():
    while True:
        for grup in daftar_grup:
            try:
                # SIMULASI MENGETIK (3 sampai 8 detik)
                async with client.action(grup, 'typing'):
                    await asyncio.sleep(random.randint(0, 1))
                
                await client.send_message(grup, pesan_promosi)
                print(f"Pesan promosi terkirim ke {grup}")
            except Exception as e:
                print(f"Gagal kirim ke {grup}: {e}")
            
            # Jeda antar grup (5-30 detik)
            jeda = random.randint(3, 7)
            print(f"Menunggu {jeda} detik sebelum ke grup berikutnya...")
            await asyncio.sleep(jeda)
        
        print("Semua grup sudah dikirimi. Menunggu 5 menit...")
        await asyncio.sleep(40)

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
