import adafruit_ssd1306
import board
import digitalio

# === OLED SETUP ===
reset_pin = digitalio.DigitalInOut(board.D25)
dc_pin = digitalio.DigitalInOut(board.D24)
cs_pin = digitalio.DigitalInOut(board.D5)
spi = board.SPI()

oled = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, dc_pin, reset_pin, cs_pin)
oled.fill(0)
oled.show()

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


# === MAIN LOOP ===
while True:
    text = input("Prompt: ")

    oled.fill(0)

    for i, line in enumerate(wrap(text)):
        oled.text(line, 0, i * CHAR_HEIGHT, 1)

    oled.show()

#ps aux | grep python
#ps aux | grep pigpiod lsmod | grep spi

"""
Place eggs in a single layer in a saucepan, add cold water to cover, cover and bring to a boil. Remove from heat, let sit for 6-7 minutes, then rinse with cold water.
import adafruit_ssd1306

# Load default font
font = ImageFont.load_default()

# Create image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.text((0, 0), "Hello Pi!", font=font, fill=255)
oled.image(image)
oled.show()

sudo find /lib/python3.11/site-packages -name "rfm9x_check.py"

"""