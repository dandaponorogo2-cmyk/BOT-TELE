import os
import json
import asyncio
import random
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# ==========================================
# KONFIGURASI UTAMA
# ==========================================
api_id = 30926385  # Ganti dengan API ID Anda
api_hash = 'd8966ae348811966dfa86d594421e8b1'  # Ganti dengan API Hash Anda
OWNER_ID = 8674245854 # <--- MASUKKAN ID TELEGRAM ANDA (Bukan ID bot)

# File untuk menyimpan pengaturan
CONFIG_FILE = "config_bot.json"

# Pengaturan Default (Jika file config belum ada)
default_config = {
    "daftar_grup": [-1002698177375],
    "pesan_promosi": "<b>Teks Promosi Default Anda</b>",
    "jeda_detik": 15
}

# ==========================================
# FUNGSI BACA & SIMPAN CONFIG
# ==========================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        save_config(default_config)
        return default_config

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ==========================================
# INISIALISASI BOT
# ==========================================
print("Mencoba login ke Telegram...")
session_str = os.environ.get('TG_SESSION', '')

if session_str:
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
else:
    client = TelegramClient('sesi_bot', api_id, api_hash)

admin_state = {} # Menyimpan status admin yang sedang mengedit

# ==========================================
# 1. FITUR AUTO-REPLY
# ==========================================
@client.on(events.NewMessage(incoming=True, pattern=r'(?i)DONE KAK'))
async def handler_auto_reply(event):
    if event.is_group:
        print(f"[{event.chat.title}] Ada yang chat: DONE KAK")
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.randint(2, 5))
        await event.reply("Otw kak, wait yaw...")

# ==========================================
# 2. FITUR ADMIN PANEL (/admin)
# ==========================================
@client.on(events.NewMessage(pattern=r'^/admin$', from_users=OWNER_ID))
async def admin_panel(event):
    buttons = [
        [Button.inline("📝 Edit Teks Promosi", data=b"edit_text")],
        [Button.inline("➕ Tambah Grup Target", data=b"add_group")],
        [Button.inline("📋 Lihat Daftar Grup", data=b"list_group")],
        [Button.inline("🗑️ Hapus Semua Grup", data=b"clear_group")],
        [Button.inline("⚙️ Ubah Jeda Waktu", data=b"edit_delay")]
    ]
    await event.respond("<b>🛠️ ADMIN PANEL BLAZE PEDIA</b>\nSilakan pilih menu:", buttons=buttons, parse_mode='html')

# ==========================================
# 3. HANDLER TOMBOL ADMIN PANEL
# ==========================================
@client.on(events.CallbackQuery)
async def callback_handler(event):
    if event.sender_id != OWNER_ID:
        return await event.answer("Akses ditolak. Anda bukan Owner.", alert=True)

    config = load_config()
    data = event.data.decode('utf-8')

    if data == "list_group":
        if not config['daftar_grup']:
            text = "Daftar grup kosong."
        else:
            text = "<b>Daftar Grup Target:</b>\n"
            for i, g in enumerate(config['daftar_grup']):
                text += f"{i+1}. <code>{g}</code>\n"
        await event.answer()
        await event.respond(text, parse_mode='html')

    elif data == "edit_text":
        admin_state[event.sender_id] = "edit_text"
        await event.answer()
        msg = await event.respond("Silakan balas pesan ini dengan teks promosi baru (Bisa pakai format HTML):")
        # Gunakan force reply
        await client.send_message(event.sender_id, "Ketik teks di sini...", reply_to=msg.id)

    elif data == "add_group":
        admin_state[event.sender_id] = "add_group"
        await event.answer()
        msg = await event.respond("Silakan balas pesan ini dengan ID Grup baru (contoh: -1001234567890):")
        await client.send_message(event.sender_id, "Ketik ID Grup di sini...", reply_to=msg.id)

    elif data == "edit_delay":
        admin_state[event.sender_id] = "edit_delay"
        await event.answer()
        msg = await event.respond("Silakan balas pesan ini dengan angka jeda dalam detik (contoh: 30):")
        await client.send_message(event.sender_id, "Ketik angka di sini...", reply_to=msg.id)

    elif data == "clear_group":
        config['daftar_grup'] = []
        save_config(config)
        await event.answer("Semua grup berhasil dihapus!", alert=True)

# ==========================================
# 4. MENANGKAP BALASAN INPUT DARI ADMIN
# ==========================================
@client.on(events.NewMessage(from_users=OWNER_ID))
async def admin_input_handler(event):
    user_id = event.sender_id
    
    # Cek apakah admin sedang dalam mode mengedit
    if user_id in admin_state:
        action = admin_state[user_id]
        text = event.text
        config = load_config()

        if action == "edit_text":
            config['pesan_promosi'] = text
            save_config(config)
            await event.reply("✅ Teks promosi berhasil diubah!")
            del admin_state[user_id]

        elif action == "add_group":
            try:
                # Validasi ID harus angka
                int(text) 
                if text not in config['daftar_grup']:
                    config['daftar_grup'].append(text)
                    save_config(config)
                    await event.reply(f"✅ Grup `{text}` berhasil ditambahkan!")
                else:
                    await event.reply("⚠️ Grup tersebut sudah ada di daftar.")
            except ValueError:
                await event.reply("❌ Gagal! Harap masukkan ID berupa angka (contoh: -1001234567890).")
            del admin_state[user_id]

        elif action == "edit_delay":
            try:
                angka = int(text)
                config['jeda_detik'] = angka
                save_config(config)
                await event.reply(f"✅ Jeda waktu diubah menjadi {angka} detik.")
            except ValueError:
                await event.reply("❌ Gagal! Harap masukkan angka saja.")
            del admin_state[user_id]

# ==========================================
# 5. FITUR AUTO-SHARE (KIRIM PESAN BERKALA)
# ==========================================
async def kirim_pesan_berkala():
    await asyncio.sleep(3) # Tunggu bot login
    print("Memulai proses Auto-Share...")
    
    while True:
        config = load_config() # Baca config terbaru setiap putaran
        grup_list = config.get("daftar_grup", [])
        pesan = config.get("pesan_promosi", "")
        jeda = config.get("jeda_detik", 15)

        if not grup_list:
            print("Daftar grup kosong. Menunggu 1 menit...")
            await asyncio.sleep(60)
            continue

        for grup in grup_list:
            try:
                async with client.action(grup, 'typing'):
                    await asyncio.sleep(random.randint(1, 3))
                
                await client.send_message(int(grup), pesan, parse_mode='html')
                print(f"✅ Terkirim ke {grup}")
            except Exception as e:
                print(f"❌ Gagal kirim ke {grup}: {e}")
            
            await asyncio.sleep(jeda)
        
        print("Selesai satu putaran. Menunggu 5 menit...")
        await asyncio.sleep(300)

# ==========================================
# JALANKAN PROGRAM
# ==========================================
async def main():
    await client.start()
    print("Login Berhasil! Userbot & Admin Panel berjalan...")
    
    # Jalankan auto-share di latar belakang
    client.loop.create_task(kirim_pesan_berkala())
    
    # Jalankan listener
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
