from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_LINK, fps_options

subscribe_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Subscribe", url=CHANNEL_LINK)],
    [InlineKeyboardButton(text="Check", callback_data="subchek")]
])

def main_kb(fps = 10, width = 480, starts = 0, duration = "Full"):
    main_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"FPS: {fps}", callback_data="choose_fps"),InlineKeyboardButton(text=f"width: {width}px", callback_data="edit_width")],
        [InlineKeyboardButton(text=f"Starts: {starts}s", callback_data="chose_start_time"), InlineKeyboardButton(text=f"End: {duration}", callback_data="duration_adjust")],
        [InlineKeyboardButton(text="Conver now✅", callback_data="convert_video")]

    ])
    return main_buttons
def create_setfps():
    # Show FPS options
    keyboard = []
    row = []
    
    for fps in fps_options:
        row.append(InlineKeyboardButton(
            text=str(fps),
            callback_data=f"fps{fps}"
        ))
        if len(row) == 3:  # 3 buttons per row
            keyboard.append(row)
            row = []
    
    if row:  # Add any remaining buttons
        keyboard.append(row)
        
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            text="🔙 Back",
            callback_data="back_to_main"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
def create_markap_kb(name, url):
    if name == "None" or url== "None":
        return None
    ads_channel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, url=url)]
    ])
    return ads_channel