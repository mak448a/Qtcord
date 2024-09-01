from PySide6.QtCore import QRunnable, Slot, Signal, QObject
import discord_integration


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
