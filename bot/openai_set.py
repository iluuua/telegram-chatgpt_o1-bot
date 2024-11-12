import openai
import datetime


class ChatGPT_conversation:
    def __init__(self, user_id, max_history_length=5, history_duration_minutes=30):
        self.user_id = user_id
        self.history = []
        self.max_history_length = max_history_length
        self.history_duration_minutes = history_duration_minutes

    def add_message(self, role, content):
        """Adds a message with a timestamp to the conversation history."""
        timestamp = datetime.datetime.now()
        self.history.append({"role": role, "content": content, "timestamp": timestamp})
        self.history = self.history[-self.max_history_length:]

        # Clear history if older than duration
        self.clear_old_messages(timestamp)

    def get_history(self):
        """Returns the conversation history as a list of dictionaries."""
        return self.history

    def clear_history(self):
        """Clears the entire conversation history."""
        self.history = []

    def clear_old_messages(self, current_timestamp):
        """Removes messages older than the specified duration from the history."""
        threshold_timestamp = current_timestamp - datetime.timedelta(minutes=self.history_duration_minutes)
        self.history = [
            msg for msg in self.history if msg["timestamp"] >= threshold_timestamp
        ]


def chatgpt_response(user_id, prompt, openai_api_key):
    openai.api_key = openai_api_key
    user_history = ChatGPT_conversation(user_id)
    user_history.add_message("user", prompt)

    messages = [
        {"role": "system", "content": "You are a helpful and informative AI assistant."},
        *user_history.get_history()
    ]

    response = openai.ChatCompletion.create(
        model="o1-mini",
        messages=messages,
        temperature=0.65
    )

    user_history.add_message("assistant", response.choices[0].message.content)

    return response.choices[0].message.content
