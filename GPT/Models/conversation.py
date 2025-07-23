
class conversation:
    def __init__(self, model, tokenizer, max_length=4096):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length

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
        return self.messages[-(self.max_length-1):]
    
    def update_messages(self, updated_messages: list = []):
        self.messages = updated_messages

    def clear_messages(self):
        self.messages = []