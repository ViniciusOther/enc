from pyrogram import Client, filters, raw, types
import json
from config import config


conf = config()
app = Client("my_account", conf.API_ID, conf.API_HASH)

@app.on_message(filters.command('chats'))
def list_chats(c, m):
    if m.chat.id != conf.PARENT_CHAT_ID:
        return
    chats = app.send(raw.functions.messages.GetAllChats(except_ids=[]))
    if(conf.write_json("chats.json", json.loads(str(chats)))):
        m.reply_document("chats.json")
    else:
        m.reply("Can't send you your chats for some reason, sorry :(")

@app.on_message(filters.regex('>'))
def add_relation(c, m):
    l = m.text.split('>')
    source = l[0]
    target = l[1]
    conf.add_relation(source, target)
    m.reply("added to relations")

@app.on_message(filters.media)
def forward(c, m):
    relation = conf.read_json()
    if(str(m.chat.id) in relation):
        for target in relation:
            m.forward(int(target))

@app.on_message(filters.regex(
    r"^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
) | filters.regex(
    r"^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
))
def forward_url(c, m):
    if not conf.ALLOW_URLS:
        return
    relation = conf.read_json()
    if(str(m.chat.id) in relation):
        for target in relation:
            m.forward(int(target))

@app.on_message(filters.command('allow_url'))
def allow_urls(c, m):
    if m.chat.id != conf.PARENT_CHAT_ID:
        return
    conf.ALLOW_URLS = not conf.ALLOW_URLS
    m.reply(f"allow urls is now {str(conf.ALLOW_URLS)}")

app.run()
