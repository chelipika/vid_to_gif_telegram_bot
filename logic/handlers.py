import os
from moviepy.editor import VideoFileClip
from random import randint
from aiogram import F, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery, FSInputFile, ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from config import TOKEN, CHANNEL_ID, CHANNEL_LINK, fps_options
from datetime import datetime, timedelta
from collections import defaultdict
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database.requests as rq

bot = Bot(token=TOKEN)
import logic.keyboards as kb

# File to store chat history
class AdvMsg(StatesGroup):
    img = State()
    audio = State()
    txt = State()
    inline_link_name = State()
    inline_link_link = State()

DEFAULT_SETTINGS = {
    "fps": 10,
    "width": 480,
    "start": 0,
    "duration": None  # None means full video
}

super_facts = [
    "🐝 Honeybees can recognize human faces, despite having brains the size of a sesame seed.",
    "🔭 A day on Venus is longer than a year on Venus—it takes 243 Earth days to rotate once on its axis but only 225 Earth days to orbit the Sun.",
    "🚶 The average person walks the equivalent of five times around the world in their lifetime.",
    "🦩 Flamingos can only eat with their heads upside down.",
    "🌊 Sloths can hold their breath underwater for up to 40 minutes, and are surprisingly good swimmers.",
    "📫 The world's deepest postbox is 10 meters underwater in Susami Bay, Japan.",
    "💃 A group of flamingos is called a 'flamboyance.'",
    "👩‍🚀 Astronauts cannot cry in space because without gravity, tears don't fall—they just form a blob around the eye.",
    "🐾 Wombats produce cube-shaped poop, which they use to mark territory. It's the only animal known to produce cubic feces.",
    "🥏 The inventor of the Frisbee was cremated and turned into Frisbees after his death, per his request.",
    "🐄 Cows have best friends and get stressed when separated from them.",
    "🛩️ The shortest commercial flight in the world lasts only 53 seconds (between the Scottish islands of Westray and Papa Westray).",
    "🦐 Mantis shrimp can punch with the force of a .22 caliber bullet, fast enough to create tiny bubbles that produce light and heat.",
    "🐬 Dolphins have names for each other and can call to specific individuals by mimicking their unique whistle.",
    "🐋 A human could swim through the veins of a blue whale."
]

class Gen(StatesGroup):
    wait = State()

class tmp_settings(StatesGroup):
    width = State()
    start = State()
    end = State()

# --- Load and Save Voice Settings ---
pending_requests = set()

async def sub_chek(user_id):
    if user_id in pending_requests or await is_subscribed(user_id=user_id):
        return True
    else:
        return False

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def convert_video_to_gif(input_path, output_path, fps=10, resize_width=480, start_time=0, duration=None):
    try:
        # Load the video clip
        video = VideoFileClip(input_path)
        
        # Apply start time and duration if specified
        if duration:
            video = video.subclip(start_time, start_time + duration)
        else:
            video = video.subclip(start_time)
        
        # Resize the video while maintaining aspect ratio
        video = video.resize(width=resize_width)
        
        # Write the GIF with specified FPS
        video.write_gif(output_path, fps=fps, program='ffmpeg')
        
        print(f"GIF successfully created: {output_path}")
        
        # Close the video clip to free memory
        video.close()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if not os.path.exists("downloads"):
    os.mkdir("downloads")

router = Router()

@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest):
    pending_requests.add(update.from_user.id)

@router.message(F.video)
async def video_to_gif(message: Message, state: FSMContext):
    await state.update_data(
        video_id=message.video.file_id,
        user_id=message.from_user.id,
        settings=DEFAULT_SETTINGS.copy()
    )
    rp_kb = kb.main_kb()
    await message.answer("Choose GIF settings or press 'Convert Now' to use these settings:", reply_markup=rp_kb)

@router.callback_query(F.data == "choose_fps")
async def choose_fps(callback: CallbackQuery):
    await callback.message.edit_text("Choose FPS (frames per second):", reply_markup=kb.create_setfps())
    await callback.answer()

@router.callback_query(F.data.in_(["fps5", "fps10", "fps15", "fps20", "fps30"]))
async def change_fps(callback: CallbackQuery, state: FSMContext):
    fps_values = {"fps5": 5, "fps10": 10, "fps15": 15, "fps20": 20, "fps30": 30}
    data = await state.get_data()
    settings = data.get("settings", DEFAULT_SETTINGS.copy())
    settings["fps"] = fps_values[callback.data]
    await state.update_data(settings=settings)
    await callback.answer(f"FPS = {settings['fps']}")

@router.callback_query(F.data == "edit_width")
async def edit_width(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Pls send the width (height is auto)\ne.g. 500, 1000")
    await callback.answer()
    await state.set_state(tmp_settings.width)

@router.message(tmp_settings.width)
async def tmp_width(message: Message, state: FSMContext):
    data = await state.get_data()
    settings = data.get("settings", DEFAULT_SETTINGS.copy())
    settings["width"] = int(message.text)  # Convert to int
    await state.update_data(settings=settings)
    tmp_kb = kb.main_kb(fps=settings["fps"], width=settings["width"], starts=settings["start"], duration=settings["duration"])
    await message.answer("Choose GIF settings or press 'Convert Now' to use these settings:", reply_markup=tmp_kb)
    await state.set_state(None)  # Exit tmp_settings state

@router.callback_query(F.data == "chose_start_time")
async def chose_start_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Pls send the start time (seconds)\ne.g. 1, 5, 10, 110")
    await callback.answer()
    await state.set_state(tmp_settings.start)

@router.message(tmp_settings.start)
async def tmp_start(message: Message, state: FSMContext):
    data = await state.get_data()
    settings = data.get("settings", DEFAULT_SETTINGS.copy())
    settings["start"] = int(message.text)
    await state.update_data(settings=settings)
    tmp_kb = kb.main_kb(fps=settings["fps"], width=settings["width"], starts=settings["start"], duration=settings["duration"])
    await message.answer("Choose GIF settings or press 'Convert Now' to use these settings:", reply_markup=tmp_kb)
    await state.set_state(None)

@router.callback_query(F.data == "duration_adjust")
async def chose_duration(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Pls send the duration (seconds)\ne.g. 5, 10, 110")
    await callback.answer()
    await state.set_state(tmp_settings.end)

@router.message(tmp_settings.end)
async def tmp_end(message: Message, state: FSMContext):
    data = await state.get_data()
    settings = data.get("settings", DEFAULT_SETTINGS.copy())
    settings["duration"] = int(message.text)
    await state.update_data(settings=settings)
    tmp_kb = kb.main_kb(fps=settings["fps"], width=settings["width"], starts=settings["start"], duration=settings["duration"])
    await message.answer("Choose GIF settings or press 'Convert Now' to use these settings:", reply_markup=tmp_kb)
    await state.set_state(None)

@router.callback_query(F.data == "convert_video")
async def convert_now(callback: CallbackQuery, state: FSMContext):
    try:
        x = await callback.message.edit_text(f"Processing...\n{super_facts[randint(0,14)]}")
        data = await state.get_data()
        video_id = data.get("video_id")
        user_id = data.get("user_id")
        settings = data.get("settings", DEFAULT_SETTINGS.copy())

        if not video_id:
            await callback.message.edit_text("No video provided. Please send a video first.")
            return

        # Download and convert the video
        output = f"downloads/{video_id}_{user_id}.gif"
        file_path = f"downloads/{video_id}_{user_id}.mp4"
        await bot.download(video_id, file_path)
        await convert_video_to_gif(
            file_path,
            output,
            fps=settings["fps"],
            resize_width=settings["width"],
            start_time=settings["start"],
            duration=settings["duration"]
        )
        gif = FSInputFile(output, f"{video_id}_{user_id}.gif")
        await callback.message.answer_animation(gif)
        
        # Clean up
        os.remove(output)
        os.remove(file_path)
        await state.clear()  # Clear state only after successful conversion
        await callback.answer("GIF created successfully!")
        await x.delete()
    except Exception as e:
        await callback.message.answer(f"An error occurred: {e}")
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    settings = data.get("settings", DEFAULT_SETTINGS.copy())
    rp_kb = kb.main_kb(fps=settings["fps"], width=settings["width"], starts=settings["start"], duration=settings["duration"])
    await callback.message.edit_text("Choose GIF settings or press 'Convert Now' to use these settings:", reply_markup=rp_kb)
    await callback.answer()

@router.message(Command("test"))
async def test(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Current state: {data}")

@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    await rq.set_user(tg_id=user_id)

    if not await sub_chek(message.from_user.id):
        await message.answer(f"Subscribe first, Подпишитесь: \n{CHANNEL_LINK}", reply_markup=kb.subscribe_channel)
        return
    await message.answer("Welcome serfer🏄‍♂️! \nSend mp4 video and i will cook it to gif😎\ncurrently bot supports only mp4 if you have any better ideas feel free to write to my dm(check bot description for further info)🥂")

@router.message(Command("narrator"))
async def narrator(message: Message, command: CommandObject):
    for user in await rq.get_all_user_ids():
        await bot.send_message(chat_id=user, text=command.args)

@router.callback_query(F.data == "subchek")
async def subchek(callback: CallbackQuery):
    if not await sub_chek(callback.from_user.id):
        await callback.answer("You're not subscribed yet")
        return
    await callback.answer("You are okay to go")

@router.message(Command("send_to_all_users"))
async def start_send_to_all(message: Message, state: FSMContext):
    await state.set_state(AdvMsg.img)
    await message.answer("Send your img🖼️")

@router.message(AdvMsg.img)
async def ads_img(message: Message, state: FSMContext):
    await state.update_data(img=message.photo[-1].file_id if message.photo else None)
    await state.set_state(AdvMsg.txt)
    await message.answer("Send your text🗄️")

@router.message(AdvMsg.txt)
async def ads_txt(message: Message, state: FSMContext):
    await state.update_data(txt=message.text)
    await state.set_state(AdvMsg.inline_link_name)
    await message.answer("Send your inline_link name📛")

@router.message(AdvMsg.inline_link_name)
async def ads_lk_name(message: Message, state: FSMContext):
    await state.update_data(inline_link_name=message.text)
    await state.set_state(AdvMsg.inline_link_link)
    await message.answer("Send your inline_link LINK🔗")

@router.message(AdvMsg.inline_link_link)
async def ads_final(message: Message, state: FSMContext):
    await state.update_data(inline_link_link=message.text)
    data = await state.get_data()
    new_inline_kb = kb.create_markap_kb(name=data['inline_link_name'], url=data['inline_link_link'])
    for user in await rq.get_all_user_ids():
        if data['img']:
            if new_inline_kb:
                await bot.send_photo(chat_id=user, photo=data['img'], caption=data['txt'], reply_markup=new_inline_kb)
            else:
                await bot.send_photo(chat_id=user, photo=data['img'], caption=data['txt'])
    await state.clear()

@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer("Wait, one request at a time \nПодождите, ваш запрос генерируется.")