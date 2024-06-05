from pyrogram import Client, filters
import os
import time

api_id = int(os.environ.get("24297933"))
api_hash = os.environ.get("0313789a16a804c8fa349a644b5dd3da")
bot_token = os.environ.get("7096017790:AAHpVsWzlwwe-GzIoIAnyt_ms5unInAhtns")

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# File untuk menyimpan pesan promosi dan daftar grup
promo_messages_file = "pesan.txt"
group_ids_file = "groups.txt"
whitelist_file = "whitelist.txt"
delay_file = "delay.txt"

# Fungsi untuk membaca pesan promosi dari file
def read_promo_messages():
    if os.path.exists(promo_messages_file):
        with open(promo_messages_file, "r") as file:
            return file.readlines()
    return []

# Fungsi untuk menambah pesan promosi ke file
def add_promo_message(new_message):
    with open(promo_messages_file, "a") as file:
        file.write(new_message + "\n")

# Fungsi untuk menghapus pesan promosi dari file
def delete_promo_message(message_index):
    messages = read_promo_messages()
    if 0 <= message_index < len(messages):
        del messages[message_index]
        with open(promo_messages_file, "w") as file:
            file.writelines(messages)

# Fungsi untuk mengedit pesan promosi dalam file
def edit_promo_message(message_index, new_message):
    messages = read_promo_messages()
    if 0 <= message_index < len(messages):
        messages[message_index] = new_message + "\n"
        with open(promo_messages_file, "w") as file:
            file.writelines(messages)

# Fungsi untuk membaca ID grup dari file
def read_group_ids():
    if os.path.exists(group_ids_file):
        with open(group_ids_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

# Fungsi untuk menambah ID grup ke file
def add_group_ids(new_group_ids):
    with open(group_ids_file, "a") as file:
        for group_id in new_group_ids:
            file.write(group_id + "\n")

# Fungsi untuk membaca daftar whitelist dari file
def read_whitelist():
    if os.path.exists(whitelist_file):
        with open(whitelist_file, "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    return []

# Fungsi untuk menambah user ke whitelist
def add_to_whitelist(user_ids):
    with open(whitelist_file, "a") as file:
        for user_id in user_ids:
            file.write(str(user_id) + "\n")

# Fungsi untuk membaca jeda waktu dari file
def read_delay():
    if os.path.exists(delay_file):
        with open(delay_file, "r") as file:
            return int(file.read().strip())
    return 5  # Default delay

# Fungsi untuk menyetel jeda waktu ke file
def set_delay(new_delay):
    with open(delay_file, "w") as file:
        file.write(str(new_delay))

# Fungsi untuk memeriksa apakah pengguna di whitelist
def check_whitelist(client, message):
    user_id = message.from_user.id
    if user_id not in read_whitelist():
        message.reply("Anda tidak memiliki izin untuk menggunakan bot ini.")
        return False
    return True

@app.on_message(filters.command("delete"))
def delete_message(client, message):
    if not check_whitelist(client, message):
        return

    chat_id = message.chat.id
    message_id = message.message_id
    client.delete_messages(chat_id, message_id)

@app.on_message(filters.command("edit"))
def edit_message(client, message):
    if not check_whitelist(client, message):
        return

    chat_id = message.chat.id
    message_id = message.message_id
    new_text = "Pesan yang telah diubah."
    client.edit_message_text(chat_id, message_id, new_text)

@app.on_message(filters.command("addmessage"))
def add_message(client, message):
    if not check_whitelist(client, message):
        return

    new_message = message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else None
    if new_message:
        add_promo_message(new_message)
        message.reply("Pesan baru telah ditambahkan.")
    else:
        message.reply("Penggunaan: /addmessage <pesan baru>")

@app.on_message(filters.command("listmessages"))
def list_messages(client, message):
    if not check_whitelist(client, message):
        return

    messages = read_promo_messages()
    if messages:
        message_list = "\n".join([f"{index + 1}. {msg}" for index, msg in enumerate(messages)])
        message.reply(f"Daftar pesan promosi:\n{message_list}")
    else:
        message.reply("Tidak ada pesan promosi yang tersimpan.")

@app.on_message(filters.command("deletemessage"))
def delete_promo(client, message):
    if not check_whitelist(client, message):
        return

    try:
        message_index = int(message.text.split(maxsplit=1)[1]) - 1
        delete_promo_message(message_index)
        message.reply("Pesan promosi berhasil dihapus.")
    except:
        message.reply("Penggunaan: /deletemessage <nomor pesan>")

@app.on_message(filters.command("editmessage"))
def edit_promo(client, message):
    if not check_whitelist(client, message):
        return

    try:
        args = message.text.split(maxsplit=2)
        message_index = int(args[1]) - 1
        new_message = args[2]
        edit_promo_message(message_index, new_message)
        message.reply("Pesan promosi berhasil diubah.")
    except:
        message.reply("Penggunaan: /editmessage <nomor pesan> <pesan baru>")

@app.on_message(filters.command("setdelay"))
def set_promo_delay(client, message):
    if not check_whitelist(client, message):
        return

    try:
        new_delay = int(message.text.split(maxsplit=1)[1])
        set_delay(new_delay)
        message.reply(f"Jeda waktu antara pesan disetel ke {new_delay} detik.")
    except:
        message.reply("Penggunaan: /setdelay <detik>")

@app.on_message(filters.command("addgroup"))
def add_group(client, message):
    if not check_whitelist(client, message):
        return

    new_group_ids = message.text.split(maxsplit=1)[1].split()
    add_group_ids(new_group_ids)
    message.reply(f"Grup baru berhasil ditambahkan: {', '.join(new_group_ids)}")

@app.on_message(filters.command("listgroups"))
def list_groups(client, message):
    if not check_whitelist(client, message):
        return

    group_ids = read_group_ids()
    if group_ids:
        group_list = "\n".join(group_ids)
        message.reply(f"Daftar grup:\n{group_list}")
    else:
        message.reply("Tidak ada grup yang tersimpan.")

@app.on_message(filters.command("promosi"))
def start_promotion(client, message):
    if not check_whitelist(client, message):
        return

    try:
        promo_index = int(message.text.split(maxsplit=1)[1]) - 1
        promo_messages = read_promo_messages()
        if not 0 <= promo_index < len(promo_messages):
            message.reply("Pesan promosi tidak ditemukan.")
            return
        promo_message = promo_messages[promo_index].strip()

        group_ids = read_group_ids()
        delay = read_delay()

        for group_id in group_ids:
            try:
                client.send_message(group_id, promo_message)
                time.sleep(delay)
            except Exception as e:
                print(f"Gagal mengirim pesan ke {group_id}: {e}")

        message.reply("Promosi telah dikirim ke semua grup!")
    except:
        message.reply("Penggunaan: /promosi <nomor pesan>")

@app.on_message(filters.command("addwhitelist"))
def add_whitelist(client, message):
    if not check_whitelist(client, message):
        return

    try:
        user_ids = [int(user_id) for user_id in message.text.split(maxsplit=1)[1].split()]
        add_to_whitelist(user_ids)
        message.reply("Whitelist berhasil diperbarui.")
    except:
        message.reply("Penggunaan: /addwhitelist <user_id1> <user_id2> ...")

@app.on_message(filters.command("listwhitelist"))
def list_whitelist(client, message):
    if not check_whitelist(client, message):
        return

    whitelist = read_whitelist()
    if whitelist:
        whitelist_list = "\n".join(map(str, whitelist))
        message.reply(f"Daftar whitelist:\n{whitelist_list}")
    else:
        message.reply("Whitelist kosong.")

app.run()