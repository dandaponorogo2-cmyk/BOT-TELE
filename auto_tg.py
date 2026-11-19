import os
import json
import asyncio
import random
from telethon.sessions import StringSession
from telethon import TelegramClient, events

# ==========================================
# KONFIGURASI
# ==========================================
api_id = 30926385
api_hash = 'd8966ae348811966dfa86d594421e8b1'
CONFIG_CHANNEL_ID = -1004361614429  # <--- MASUKKAN ID CHANNEL "BLAZE CONFIG" DI SINI

# Pengaturan Default (Jika belum ada perintah dari bot)
pengaturan = {
    "daftar_grup": [-1002698177375],
    "pesan_promosi": "Teks promosi default...",
    "jeda_detik": 15
}

print("Mencoba login ke Telegram...")
session_str = os.environ.get('TG_SESSION', '')
if session_str:
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
else:
    client = TelegramClient('sesi_bot', api_id, api_hash)

# ==========================================
# LISTENER: MENDENGARKAN PERUBAHAN DARI BOT NODE.JS
# ==========================================
@client.on(events.NewMessage(chats=CONFIG_CHANNEL_ID))
async def config_listener(event):
    global pengaturan
    teks = event.message.message
    
    # Jika bot Node.js mengirim format "UPDATE_CONFIG: {json}"
    if teks.startswith("UPDATE_CONFIG:"):
        try:
            json_baru = teks.replace("UPDATE_CONFIG:", "").strip()
            pengaturan = json.loads(json_baru)
            print("✅ Pengaturan berhasil diperbarui dari Admin Panel!")
            print(f"Total Grup: {len(pengaturan['daftar_grup'])}, Jeda: {pengaturan['jeda_detik']}s")
        except Exception as e:
            print(f"❌ Gagal membaca config dari channel: {e}")

# ==========================================
# FITUR KIRIM PESAN BERKALA
# ==========================================
async def kirim_pesan_berkala():
    while True:
        # Ambil data terbaru dari variabel pengaturan
        grup_list = pengaturan.get("daftar_grup", [])
        pesan = pengaturan.get("pesan_promosi", "")
        jeda = pengaturan.get("jeda_detik", 15)

        for grup in grup_list:
            try:
                async with client.action(grup, 'typing'):
                    await asyncio.sleep(1)
                
                await client.send_message(grup, pesan, parse_mode='html')
                print(f"Terkirim ke {grup}")
            except Exception as e:
                print(f"Gagal kirim ke {grup}: {e}")
            
            await asyncio.sleep(jeda)
        
        print("Selesai satu putaran. Menunggu 5 menit...")
        await asyncio.sleep(300)

async def main():
    await client.start()
    print("Userbot berjalan! Menunggu perintah dari Admin Panel...")
    client.loop.create_task(kirim_pesan_berkala())
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
