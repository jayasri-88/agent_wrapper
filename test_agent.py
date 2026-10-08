from app.agent import create_chat
chat=create_chat()


print(chat.send_message("What is 1234*5678? Then tell me the time.").text)