import os
from pathlib import Path

from telebot import TeleBot
from telegram_notifier.exceptions import TelegramNotifierError
from vyper import v

config_dir = Path(__file__).parent.joinpath("../../").joinpath("config")
v.set_config_name("prod")
v.add_config_path(config_dir)
v.read_in_config()


def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))
    file_path = Path(__file__).parent.joinpath("../../").joinpath("swagger-doc-dm-api-account.json")
    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption='coverage'
        )


if __name__ == '__main__':
    send_file()
