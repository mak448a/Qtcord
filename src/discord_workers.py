from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QByteArray
import discord_integration
import os
import platformdirs
import requests
import xxhash


class SendMessageWorker(QObject, QRunnable):
    finished = Signal()

    def __init__(self, text_message, channel_id):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.text_message = text_message
        self.channel_id = channel_id

    @Slot()
    def run(self):
        discord_integration.send_message(self.text_message, self.channel_id)
        self.finished.emit()


class SendTypingWorker(QObject, QRunnable):
    def __init__(self, channel_id):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.channel_id = channel_id

    @Slot()
    def run(self):
        discord_integration.send_typing(self.channel_id)


class UpdateMessagesWorker(QObject, QRunnable):
    update = Signal(dict)

    def __init__(self, channel_id):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.channel_id = channel_id

    @Slot()
    def run(self):
        self.update.emit(discord_integration.get_messages(self.channel_id))


class FileRequestWorker(QObject, QRunnable):
    finished = Signal(QByteArray)

    def __init__(self, url, cache_subdir):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.url = url
        self.cache_subdir = cache_subdir

    @Slot()
    def run(self):
        cache_dir = f"{platformdirs.user_cache_dir('Qtcord')}/{self.cache_subdir}"
        cache_hash = self.get_cache_hash()
        save_path = f"{cache_dir}/{cache_hash}"

        data = b""
        try:
            with open(save_path, "rb") as f:
                data = f.read()
        except OSError:
            response = requests.get(self.url)

            if response.status_code == 404:
                save_path = ""
            else:
                if not os.path.exists(f"{cache_dir}"):
                    os.makedirs(f"{cache_dir}")

                with open(save_path, "wb") as f:
                    for chunk in response.iter_content():
                        f.write(chunk)
                        data += chunk

        self.finished.emit(QByteArray(data))

    def get_cache_hash(self):
        return xxhash.xxh64(self.url).hexdigest()
