import os
import base64
import json
from gamer.fixed import calculate_action
from gamer.operating_system import OperatingSystem
from openai import OpenAI
from dotenv import load_dotenv
from gamer.utils import get_text_element, get_text_coordinates
from gamer.config import Config
import easyocr

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
operating_system = OperatingSystem()

client = OpenAI(
    api_key=api_key,
)

# Load configuration
config = Config()


def get_sm64_operation(messages):
    if config.verbose:
        print("[poker-agent] get_sm64_operation")

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    # Call the function to capture the screen with the cursor
    operating_system.capture_screen(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    user_prompt = "See the screenshot of the game. Provide the board state in valid json."

    vision_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ],
    }
    messages.append(vision_message)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=0.7,
        max_tokens=3000,
    )

    content = response.choices[0].message.content
    if config.verbose:
        print("[poker-agent] preprocessed content", content)

    content = clean_json(content)

    assistant_message = {"role": "assistant", "content": content}

    content = json.loads(content)

    messages.append(assistant_message)

    return content


def get_poker_operation(move_or_not_messages):
    if config.verbose:
        print("[poker-agent] get_poker_operation")

    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    screenshot_filename = os.path.join(screenshots_dir, "screenshot.png")
    # Call the function to capture the screen with the cursor
    operating_system.capture_screen(screenshot_filename)

    with open(screenshot_filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    user_prompt = "See the screenshot of the game. Provide the board state in valid json."

    vision_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ],
    }
    move_or_not_messages.append(vision_message)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=move_or_not_messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=0,
        max_tokens=3000,
    )

    content = response.choices[0].message.content
    if config.verbose:
        print("[poker-agent] preprocessed content", content)

    content = clean_json(content)

    content_str = content

    content_json = json.loads(content)

    actionArguments = json.loads(content_json.get("boardState"))

    if not actionArguments:
        content_json["x"] = "0.50"
        content_json["y"] = "0.50"
        return content_json

    gameOver = actionArguments.get("isGameOver", False)

    if gameOver:
        content_json["x"] = "0.50"
        content_json["y"] = "0.50"
        return content_json

    processed_content = process_ocr(
        move_or_not_messages, content_json, content_str, screenshot_filename
    )

    return processed_content


def process_ocr(messages, content, content_str, screenshot_filename):
    if config.verbose:
        print(
            "[process_ocr] content",
            content,
        )

    processed_content = None

    if config.verbose:
        print(
            "[process_ocr] operation",
            content,
        )

    print(f'\n\nCONTENT {content} \n\n')

    communityCards = json.loads(content.get("boardState")).get("communityCards")
    holeCards = json.loads(content.get("boardState")).get("holeCards")
    currentPotValue = json.loads(content.get("boardState")).get("currentPotValue", 10)
    whoRaised = json.loads(content.get("boardState")).get("whoRaised", [])


    if not holeCards:
        content["x"] = "0.50"
        content["y"] = "0.50"
        return content
    
    raiseAmounts = [raise_['raise'] for raise_ in whoRaised]

    action = calculate_action(communityCards, holeCards, currentPotValue, raiseAmounts)

    text_to_click = action

    # if config.verbose:
    #     print(
    #         "[process_ocr] text_to_click",
    #         text_to_click,
    #     )
    # upcase the first letter of the text_to_click
    text_to_click = text_to_click[0].upper() + text_to_click[1:]

    # # Initialize EasyOCR Reader
    # reader = easyocr.Reader(["en"])

    # # Read the screenshot
    # result = reader.readtext(screenshot_filename)
    # if config.verbose:
    #     print("\n\n\n[process_ocr] results", result)
    #     print("\n\n\n")

    # try:

    #     text_element_index = get_text_element(
    #         result, text_to_click, screenshot_filename
    #     )
    #     coordinates = get_text_coordinates(
    #         result, text_element_index, screenshot_filename
    #     )
    # except Exception as e:
    #     print("[process_ocr] error:", e)
    #     print("[process_ocr] wait and try again")
    #     try:
    #         if text_to_click == "Check": 
    #             text_element_index = get_text_element(
    #                 result, "Call", screenshot_filename
    #             )
    #             coordinates = get_text_coordinates(
    #                 result, text_element_index, screenshot_filename
    #             )
    #         elif text_to_click == "Call":
    #             text_element_index = get_text_element(
    #                 result, "Check", screenshot_filename
    #             )
    #             coordinates = get_text_coordinates(
    #                 result, text_element_index, screenshot_filename
    #             )
    #     except:
    #         pass
    #     return {
    #         "thought": "It failed so I need to wait and try again",
    #         "action": "wait",
    #     }

    if text_to_click == "Check":
        coordinates = { 'x': 0.556, 'y': 0.86}
    elif text_to_click == "Call":
        coordinates = { 'x': 0.556, 'y': 0.86}
    elif text_to_click == "Fold":
        coordinates = { 'x': 0.421, 'y': 0.86}

    # add `coordinates`` to `content`
    content["x"] = coordinates["x"]
    content["y"] = coordinates["y"]

    # if config.verbose:
    #     print(
    #         "[process_ocr] text_element_index",
    #         text_element_index,
    #     )
    #     print(
    #         "[process_ocr] coordinates",
    #         coordinates,
    #     )
    #     print(
    #         "[process_ocr] final content",
    #         content,
    #     )
    processed_content = content

    # wait to append the assistant message so that if the `processed_content` step fails we don't append a message and mess up message history
    assistant_message = {"role": "assistant", "content": content_str}
    messages.append(assistant_message)

    return processed_content


def clean_json(content):
    if content.startswith("```json"):
        content = content[
            len("```json") :
        ].strip()  # Remove starting ```json and trim whitespace
    elif content.startswith("```"):
        content = content[
            len("```") :
        ].strip()  # Remove starting ``` and trim whitespace
    if content.endswith("```"):
        content = content[
            : -len("```")
        ].strip()  # Remove ending ``` and trim whitespace

    # Normalize line breaks and remove any unwanted characters
    content = "\n".join(line.strip() for line in content.splitlines())

    return content