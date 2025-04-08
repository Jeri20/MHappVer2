from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

chat_history = {}

def get_chat_response(user_id, user_input):
    if user_id not in chat_history:
        chat_history[user_id] = []

    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat(chat_history[user_id] + [new_input_ids], dim=-1) if chat_history[user_id] else new_input_ids
    output = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    response = tokenizer.decode(output[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    chat_history[user_id].append(new_input_ids)
    chat_history[user_id].append(output)

    return response
