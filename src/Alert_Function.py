from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
import pygame
import threading
import tkinter as tk

class Alert_Function():
    def __init__(self):
        # Initialize LineBotApi with your channel access token
        Line_API = 'TbRiL19SkLU7FtdJevjawji2GrTcC2R2mn2lBS/X5itewl7AN3fGr7RM6AC50g3VUmoFU7xNIq1q5ZegJeATWw2REvGJ1lQrLwFgWZJAEWQSJq24+Pkcomd13bTMS9HcLGArUexhYj/1Hvpox5uzpgdB04t89/1O/w1cDnyilFU='
        self.line_bot_api = LineBotApi(Line_API)
        self.User_Id = "U6efd4c25a06c2f86676f50b8bab25c28"

    def Send_Line_Message(self, Message):
        try:
            self.line_bot_api.push_message(self.User_Id, TextSendMessage(text=Message))
            print("Message sent successfully.")
        except LineBotApiError as e:
            print(f"Failed to send message: {e.status_code}, {e.error.message}")

    def Alert_Sound(Self):
        # Initialize Pygame
        pygame.mixer.init()

        sound_file = "Sound\\Emergency_Sound.mp3"
        # Load the sound file
        sound = pygame.mixer.Sound(sound_file)

        # Play the sound in a separate thread
        def play_sound_thread():
            sound.play()
            while pygame.mixer.get_busy():
                pygame.time.wait(100)
            pygame.mixer.quit()

        # Create and start the thread
        sound_thread = threading.Thread(target=play_sound_thread)
        sound_thread.start()

    def show_notification(self, message):
        root = tk.Toplevel()
        root.title("Notification")
        root.geometry("700x700+{}+{}".format(
            root.winfo_screenwidth()//2,
            100
        ))

        label = tk.Label(root, text=message, font=("Helvetica", 14, "bold"))
        label.pack(pady=20)

        # Close notification window after 5 seconds
        root.after(5000, root.destroy)
