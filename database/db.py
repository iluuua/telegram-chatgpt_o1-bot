from pathlib import Path
import datetime
import sqlite3

path = Path(__file__).parent / 'db.sqlite'


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(f'{path}', check_same_thread=False)

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS USER 
            (
                id INTEGER PRIMARY KEY,
                is_admin BOOLEAN,
                is_subscribed BOOLEAN,

                last_tokens_update TEXT NOT NULL,
                subscription_start TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TOKENS
            (
                user_id INTEGER PRIMARY KEY,
                chatgpt_tokens INTEGER,
                image_gen_tokens INTEGER,
                image_rec_tokens INTEGER,
                tts_tokens INTEGER,
                whisper_tokens INTEGER,
                FOREIGN KEY (user_id) REFERENCES USER(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MODELS 
            (
                user_id INTEGER PRIMARY 
                chatgpt_model TEXT,
                image_model TEXT,
                audio_model TEXT,
            )
        """)

        self.connection.commit()
        cursor.close()

    def check_user_exists(self, user_id):
        cursor = self.connection.cursor()
        try:
            user_id = int(user_id)
            cursor.execute("SELECT 1 FROM USER WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return bool(result)
        except ValueError:
            print(f"Invalid user ID: {user_id}. Please provide an integer.")
            cursor.close()
            return False

    def add_user(self, user_id, is_admin):
        if self.check_user_exists(user_id):
            return

        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO USER (id, is_admin, last_tokens_update) 
        VALUES (?, ?, ?)
        """, (user_id, is_admin, datetime.datetime.now()))

        cursor.execute("""
        INSERT INTO TOKENS (user_id, chatgpt_tokens, image_gen_tokens, )
        VALUES ()
        """, ())

        self.connection.commit()

        cursor.execute("""
        
        """)

        cursor.close()

    def subscribe(self, id):
        cursor = self.connection.cursor()
        cursor.execute("""
        
        """)

        self.connection.commit()
        cursor.close()

    # def check_tokens_available(self, id, service):
    #     if service == "chatgpt":
    #
