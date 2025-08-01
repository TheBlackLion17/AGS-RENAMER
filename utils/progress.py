# utils/progress.py

import time
from pyrogram.types import Message

async def progress_for_pyrogram(current, total, message: Message, start):
    now = time.time()
    diff = now - start

    if round(diff % 10) == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion

        progress = "[{0}{1}] {2}%".format(
            ''.join(["■" for i in range(int(percentage / 10))]),
            ''.join(["░" for i in range(10 - int(percentage / 10))]),
            round(percentage, 2)
        )

        temp_text = f"""
📦 **Progress**: `{progress}`
✅ **Done**: `{humanbytes(current)}`
📁 **Total**: `{humanbytes(total)}`
⚡ **Speed**: `{humanbytes(speed)}/s`
⏱️ **ETA**: `{time_formatter(estimated_total_time)}`
"""
        try:
            await message.edit_text(temp_text)
        except:
            pass

def humanbytes(size):
    # Return size in human-readable format
    if not size:
        return ""
    power = 1024
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}B"

def time_formatter(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    time = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s" if seconds else "")
    )
    return time
