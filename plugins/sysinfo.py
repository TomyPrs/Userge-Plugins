""" Fetch System information."""

import sys
import platform
import psutil

from pyrogram import __version__ as pyrover
from datetime import datetime
from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from spamwatch import __version__ as __sw__
from userge import userge, Message


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@userge.on_cmd(
    "sysinfo",
    about={"header": "Fetching Hardware and system info", "usage": "{tr}sysinfo"},
)
async def sys_info(message: Message):
    """ Fetching all hardware and system info. """
    await message.edit("`Fetching system Information please wait..`")
    uname = platform.uname()
    sysinfo = "**System Information**\n"
    sysinfo += f"`System   : {uname.system}`\n"
    sysinfo += f"`Release  : {userge.SYSTEM_VERSION}`\n"
    sysinfo += f"`Version  : {uname.version}`\n"
    sysinfo += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    sysinfo += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpu = "**CPU Info**\n"
    cpu += "`Physical cores   : " + str(psutil.cpu_count(logical=False)) + "`\n"
    cpu += "`Total cores      : " + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cfreq = psutil.cpu_freq()
    cpu += f"`Max Frequency    : {cfreq.max:.2f}Mhz`\n"
    cpu += f"`Min Frequency    : {cfreq.min:.2f}Mhz`\n"
    cpu += f"`Current Frequency: {cfreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpu += f"`Core {i}  : {percentage}%`\n"
    cpu += f"`Usage All Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    meminfo = "**Memory Usage**\n"
    meminfo += f"`Total     : {get_size(svmem.total)}`\n"
    meminfo += f"`Available : {get_size(svmem.available)}`\n"
    meminfo += f"`Used      : {get_size(svmem.used)}`\n"
    meminfo += f"`Percentage: {svmem.percent}%`\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        diskinfo = f"`File system type:` {partition.fstype}`\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        diskinfo = "**Usage**\n"
        diskinfo += f"`Total Size: {get_size(partition_usage.total)}`\n"
        diskinfo += f"`Used      : {get_size(partition_usage.used)}`\n"
        diskinfo += f"`Free      : {get_size(partition_usage.free)}`\n"
        diskinfo += f"`Percentage: {partition_usage.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    uinfo = "**Userge System Info**\n"
    uinfo += f"`Userge uptime    : {userge.uptime}`\n"
    uinfo += f"`Pyrogram version : {pyrover}`\n"
    uinfo += f"`Python version   : {userge.DEVICE_MODEL}`\n"
    res = f"{str(sysinfo)}\n"
    res += f"{str(cpu)}\n"
    res += f"{str(meminfo)}\n"
    res += f"{str(diskinfo)}\n"
    res += f"{str(bw)}\n"
    res += f"{uinfo}"
    await message.edit(res, parse_mode="markdown")
