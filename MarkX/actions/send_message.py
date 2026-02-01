import time
import pyautogui
from tts import edge_speak

REQUIRED_PARAMS = ["receiver", "message_text", "platform"]

def send_message(parameters: dict, response: str | None = None, player=None, session_memory=None) -> bool:
    """
    Send a message via Windows app (WhatsApp, Telegram, etc.)

    Multi-step support: asks for missing parameters using temporary memory.

    Expected parameters:
        - receiver (str)
        - message_text (str)
        - platform (str, default: "WhatsApp")
    """

    if session_memory is None:
        msg = "Session memory missing, cannot proceed."
        if player:
            player.write_log(msg)
        edge_speak(msg, player)
        return False

    if parameters:
        session_memory.update_parameters(parameters)

    for param in REQUIRED_PARAMS:
        value = session_memory.get_parameter(param)
        if not value:
        
            session_memory.set_current_question(param)
            question_text = ""
            if param == "receiver":
                question_text = "Sir, who should I send the message to?"
            elif param == "message_text":
                question_text = "Sir, what should I say?"
            elif param == "platform":
                question_text = "Sir, which platform should I use? (WhatsApp, Telegram, etc.)"
            else:
                question_text = f"Sir, please provide {param}."

            if player:
                player.write_log("AI :", question_text)
            edge_speak(question_text, player)
            return False  

    receiver = session_memory.get_parameter("receiver").strip()
    platform = session_memory.get_parameter("platform").strip() or "WhatsApp"
    message_text = session_memory.get_parameter("message_text").strip()

    if response:
        if player:
            player.write_log(response)
        edge_speak(response, player)

    try:
        pyautogui.PAUSE = 0.1

        pyautogui.press("win")
        time.sleep(0.3)
        pyautogui.write(platform, interval=0.03)
        pyautogui.press("enter")
        time.sleep(0.6)

        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.2)
        pyautogui.write(receiver, interval=0.03)
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(0.2)

        pyautogui.write(message_text, interval=0.03)
        pyautogui.press("enter")

        session_memory.clear_current_question()
        session_memory.clear_pending_intent()
        session_memory.update_parameters({})  

        # -----------------------------
        # Log success
        # -----------------------------
        success_msg = f"Sir, message sent to {receiver} via {platform}."
        if player:
            player.write_log(success_msg)
        edge_speak(success_msg, player)

        return True

    except Exception as e:
        msg = f"Sir, I failed to send the message. ({e})"
        if player:
            player.write_log(msg)
        edge_speak(msg, player)
        return False
