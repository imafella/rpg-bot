import openai

# Character system message templates (minimal and reusable)
CHARACTER_SYSTEM_MESSAGES = {
    "Zen": "You are Zen, a sarcastic rogue who hides her royal blood. You value secrecy and loyalty to your brother.",
    "Theo": "You are Theo, a blunt, loyal town guard who dreams of becoming a knight. You protect others and dislike cowardice.",
    "Merp": "You are Merp, an excitable dwarf scholar obsessed with monsters. You ramble about obscure biology and ignore social cues.",
    "Rupert": "You are Rupert, a quiet magical scholar with a burning curiosity. You combine sword and spell, often lost in thought."
}

# Store short context and logs efficiently
class ConversationManager:
    def __init__(self):
        self.context_summary = "The group is resting at camp."
        self.latest_exchanges = []  # recent 1–2 turns

    def update_context(self, speaker, message):
        self.latest_exchanges.append(f"{speaker}: {message}")
        if len(self.latest_exchanges) > 2:
            self.latest_exchanges.pop(0)

    def get_prompt_context(self):
        return self.context_summary + "\n" + "\n".join(self.latest_exchanges)


class DialogueEngine:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model

    def get_character_response(self, character_name, user_input, context):
        messages = [
            {"role": "system", "content": CHARACTER_SYSTEM_MESSAGES[character_name]},
            {"role": "user", "content": f"Context: {context}\nInput: {user_input}\nYour reply:"}
        ]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.6,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()


class DialogueSystem:
    def __init__(self, api_key):
        self.engine = DialogueEngine(api_key)
        self.conversation = ConversationManager()

    def ask(self, character_name, user_input):
        context = self.conversation.get_prompt_context()
        response = self.engine.get_character_response(character_name, user_input, context)
        self.conversation.update_context(character_name, response)
        return response


# === Example usage ===
# system = DialogueSystem(api_key="your-openai-api-key")
# print(system.ask("Zen", "What do you think of the merchant with the glowing staff?"))
