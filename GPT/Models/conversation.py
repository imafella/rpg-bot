
class conversation:
    def __init__(self,max_history_length=8):
        self.max_history_length = max_history_length
        self.location = None
        self.present_characters = []

        # The entire conversation history
        # This will be a list of dictionaries with 'role' and 'content'
        # 'role' can be 'user', 'assistant', or 'system'
        # 'content' is the text of the message
        # This will be used to maintain the conversation context
        self.messages = []

    def add_message(self, role, content):
        # doesn't need to check for max_length here, as it will be handled in get_messages
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages[-(self.max_history_length-1):]
    
    def get_messsage_contents(self):
        return [msg['content'] for msg in self.messages[-(self.max_history_length-1):]]
    
    def update_messages(self, updated_messages: list = []):
        self.messages = updated_messages

    def clear_messages(self):
        self.messages = []