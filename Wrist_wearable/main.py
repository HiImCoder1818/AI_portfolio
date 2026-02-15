from llama_cpp import Llama
import adafruit_ssd1306
import board
import digitalio

reset_pin = digitalio.DigitalInOut(board.D25)
dc_pin = digitalio.DigitalInOut(board.D24)
cs_pin = digitalio.DigitalInOut(board.D5)
spi = board.SPI()

oled = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc_pin, reset_pin, cs_pin)
oled.fill(0)
oled.show()

def show_text(text, x, y):
    oled.fill(0)
    oled.text(text, x, y, 1)
    oled.show()

show_text("Loading Model", 0, 0)

# Load the model
llm = Llama(
    model_path="model.gguf",  # replace with your actual path
    n_ctx=512,
    n_threads=6,           # Raspberry Pi 5 has 6 cores
    chat_format="llama-3", # VERY important for system prompts
    verbose=True           # optional: shows logs
)

CHAR_WIDTH = 6    # Default font width in pixels
CHAR_HEIGHT = 8   # Default font height in pixels
MAX_CHARS_PER_LINE = oled.width // CHAR_WIDTH
MAX_LINES = oled.height // CHAR_HEIGHT

# === Character-based wrap function ===
def wrap(text, max_chars=21, max_lines=8):
    lines = []
    i = 0
    while i < len(text) and len(lines) < max_lines:
        chunk = text[i:i + max_chars]
        lines.append(chunk)

        i += max_chars

        # If the next character is a space and the current line ended *exactly* at max_chars,
        # skip the space (to avoid space at the beginning of the next line)
        if i < len(text) and text[i] == " " and len(chunk) == max_chars:
            i += 1  # Skip space
    return lines

# Define the system and user prompt
messages = [
    {"role": "system", "content": "You are to provide the answer in the most straightforward way, specificlly under 168 characters, more formally as under 42-45 tokens."},
    {"role": "user", "content": ""}
]

show_text("Llama 3.2 3B", 0, 0)

while True:
    prompt = input("Prompt: ")

    if prompt == "stop":
        break

    messages[1]["content"] = prompt

    show_text("Waiting for response", 0, 0)

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=60,
        temperature=0.7,
        top_p=0.95,
        stop=["</s>"]
    )

    text = response["choices"][0]["message"]["content"]

    oled.fill(0)
    for i, line in enumerate(wrap(text)):
        oled.text(line, 0, i * CHAR_HEIGHT, 1)
    oled.show()