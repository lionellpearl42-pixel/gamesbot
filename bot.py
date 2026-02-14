
import os
import random
from groq import Groq
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =============================
# CONFIG
# =============================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# =============================
# FUNÇÃO IA GROQ
# =============================

def gerar_resposta_ia(prompt):
    resposta = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Você é um criador de jogos divertido para grupos do Telegram."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return resposta.choices[0].message.content


# =============================
# COMANDOS
# =============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 BOT IA DE JOGOS ATIVADO!\n\n"
        "/quiz - Quiz inteligente\n"
        "/verdade - Verdade\n"
        "/consequencia - Consequência\n"
        "/pergunta - Pergunta criativa\n"
        "/ia - Pergunte qualquer coisa"
    )


# QUIZ IA
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Gerando pergunta...")

    pergunta = gerar_resposta_ia(
        "Crie uma pergunta de quiz com 4 alternativas e diga a resposta correta no final."
    )

    await update.message.reply_text(f"🎯 QUIZ:\n\n{pergunta}")


# VERDADE
async def verdade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤫 Preparando verdade...")

    resposta = gerar_resposta_ia(
        "Crie uma pergunta ousada e divertida de Verdade para um grupo de amigos."
    )

    await update.message.reply_text(f"🗣 VERDADE:\n\n{resposta}")


# CONSEQUÊNCIA
async def consequencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Pensando na consequência...")

    resposta = gerar_resposta_ia(
        "Crie uma consequência engraçada e criativa para um jogo em grupo no Telegram."
    )

    await update.message.reply_text(f"⚡ CONSEQUÊNCIA:\n\n{resposta}")


# PERGUNTA PARA MOVIMENTAR GRUPO
async def pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = gerar_resposta_ia(
        "Crie uma pergunta divertida que gere debate em um grupo do Telegram."
    )

    await update.message.reply_text(f"❓ PERGUNTA DO DIA:\n\n{resposta}")


# IA LIVRE
async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = " ".join(context.args)

    if not texto_usuario:
        await update.message.reply_text("Digite algo após /ia")
        return

    resposta = gerar_resposta_ia(texto_usuario)

    await update.message.reply_text(resposta)


# =============================
# MAIN
# =============================

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("verdade", verdade))
    app.add_handler(CommandHandler("consequencia", consequencia))
    app.add_handler(CommandHandler("pergunta", pergunta))
    app.add_handler(CommandHandler("ia", ia))

    print("Bot rodando com IA Groq 🚀")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
