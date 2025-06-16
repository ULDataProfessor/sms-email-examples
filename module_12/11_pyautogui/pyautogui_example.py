#create an example of using pyautogui to automate a simple task
import pyautogui
import time

# Wait for 5 seconds to switch to the target application
time.sleep(5)

# Move the mouse to a specific position (x=100, y=200)
pyautogui.moveTo(100, 200, duration=1)

# Click the mouse at the current position
pyautogui.click()

# Type a message
pyautogui.typewrite("Hello, this is an automated message!", interval=0.1)
                    
# Press the Enter key
pyautogui.press('enter')

# Move the mouse to another position (x=300, y=400)
pyautogui.moveTo(300, 400, duration=1)

# Right-click at the current position
pyautogui.rightClick()

# Take a screenshot of the current screen
screenshot = pyautogui.screenshot()

# Save the screenshot to a file
screenshot.save("screenshot.png")

