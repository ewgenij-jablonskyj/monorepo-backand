from dotenv import load_dotenv
from websocket import create_connection
import os
import json

load_dotenv()

API_URL = "wss://ws.xtb.com/demo"

def login_to_api():
    try:
        web_socket = create_connection(API_URL)
        print("Połączono z serwerem. Próba logowania...")
        
        login_data = {
            "command": "login",
            "arguments": {
                "userId": os.getenv("XTB_USER"),
                "password": os.getenv("XTB_PASSWORD")
                
            }
        }
        
        web_socket.send(str(login_data))
        response = web_socket.recv()
        response_json = json.loads(response)
        
        if response_json.get("status") is True:
            session_id = response_json.get("steamSessionId")
            print(f"Zalogowano pomyślnie. ID sesji: {session_id}")
            return web_socket, session_id
        else:
            print(f"Błąd logowania: {response_json.get('errorCode')}")
            web_socket.close()
            return None, None
    except Exception as e:
        print(f"Wystąpił błąd podczas logowania: {e}")
        return None, None

if __name__ == "__main__":
    connection, session = login_to_api()
    if connection:
        connection.close()
        print("Połączenie zakończone.")