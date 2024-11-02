import ctypes
from ctypes import wintypes
import psutil
import win32api
import win32process
import win32con
import struct
import os


def modify_position_04(file_path, value):
    """修改存档文件04位置的值（范围0-40）"""
    if not 0 <= value <= 40:
        print("错误：请输入0-40之间的数值")
        return

    # 创建备份
    backup_path = file_path + '.backup'
    if not os.path.exists(backup_path):
        with open(file_path, 'rb') as orig:
            with open(backup_path, 'wb') as backup:
                backup.write(orig.read())
        print(f"已创建备份文件: {backup_path}")

    # 读取并修改文件
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())

    if len(data) > 4:
        data[4] = value  # 位置 0x04

        with open(file_path, 'wb') as f:
            f.write(data)
        print(f"修改成功: 位置 0x04 已修改为 {hex(value)} ({value})")
    else:
        print("错误：文件太短，无法修改指定位置")


def modify_position_08_09(file_path):
    """修改存档文件08-09位置的值为FF"""
    # 创建备份
    backup_path = file_path + '.backup'
    if not os.path.exists(backup_path):
        with open(file_path, 'rb') as orig:
            with open(backup_path, 'wb') as backup:
                backup.write(orig.read())
        print(f"已创建备份文件: {backup_path}")

    # 读取并修改文件
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())

    if len(data) > 9:
        data[8] = 0xFF  # 位置 0x08
        data[9] = 0xFF  # 位置 0x09

        with open(file_path, 'wb') as f:
            f.write(data)
        print("修改成功: 位置 0x08 和 0x09 已修改为 0xFF")
    else:
        print("错误：文件太短，无法修改指定位置")

class MemoryTools:
    def __init__(self, process_name):
        """初始化内存工具类"""
        self.process_name = process_name
        self.process_info = None
        self.handle = None
        self.initialize()

    def initialize(self):
        """初始化进程信息和句柄"""
        try:
            # 查找进程
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'].lower() == self.process_name.lower():
                    pid = proc.info['pid']

                    # 获取进程句柄
                    self.handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)

                    # 获取所有模块
                    modules = win32process.EnumProcessModules(self.handle)
                    module_info = []

                    for module in modules:
                        try:
                            module_path = win32process.GetModuleFileNameEx(self.handle, module)
                            module_name = module_path.split('\\')[-1]

                            # 获取模块信息
                            module_info.append({
                                'name': module_name,
                                'path': module_path,
                                'base_address': module
                            })
                        except Exception as e:
                            print(f"获取模块 {module} 信息时出错: {e}")
                            continue

                    # 设置进程信息
                    self.process_info = {
                        'pid': pid,
                        'base_address': module_info[0]['base_address'],
                        'modules': module_info
                    }
                    return

            raise Exception(f"未找到进程: {self.process_name}")

        except Exception as e:
            print(f"初始化错误: {e}")
            if self.handle:
                win32api.CloseHandle(self.handle)
            raise

    def read_memory(self, address, size):
        """读取内存"""
        try:
            return win32process.ReadProcessMemory(self.handle, address, size)
        except Exception as e:
            print(f"读取内存错误: {e}")
            return None

    def write_memory(self, address, data):
        """写入内存"""
        try:
            win32process.WriteProcessMemory(self.handle, address, data, len(data))
            return True
        except Exception as e:
            print(f"写入内存错误: {e}")
            return False

    def search_value(self, value, value_type="int", start_address=None, end_address=None):
        """
        搜索特定值
        value_type 可以是: "int", "float", "double", "string", "bytes"
        """
        try:
            # 如果没有指定起始地址，使用基地址
            if start_address is None:
                start_address = self.process_info['base_address']

            # 获取系统信息以确定搜索范围
            class SYSTEM_INFO(ctypes.Structure):
                _fields_ = [
                    ("wProcessorArchitecture", wintypes.WORD),
                    ("wReserved", wintypes.WORD),
                    ("dwPageSize", wintypes.DWORD),
                    ("lpMinimumApplicationAddress", ctypes.c_void_p),
                    ("lpMaximumApplicationAddress", ctypes.c_void_p),
                    ("dwActiveProcessorMask", ctypes.c_void_p),
                    ("dwNumberOfProcessors", wintypes.DWORD),
                    ("dwProcessorType", wintypes.DWORD),
                    ("dwAllocationGranularity", wintypes.DWORD),
                    ("wProcessorLevel", wintypes.WORD),
                    ("wProcessorRevision", wintypes.WORD)
                ]

            si = SYSTEM_INFO()
            ctypes.windll.kernel32.GetSystemInfo(ctypes.byref(si))

            if end_address is None:
                end_address = si.lpMaximumApplicationAddress

            # 准备搜索的值
            if value_type == "int":
                search_bytes = struct.pack("i", value)
            elif value_type == "float":
                search_bytes = struct.pack("f", value)
            elif value_type == "double":
                search_bytes = struct.pack("d", value)
            elif value_type == "string":
                search_bytes = value.encode('utf-8')
            elif value_type == "bytes":
                search_bytes = value
            else:
                raise ValueError("不支持的值类型")

            # 存储找到的地址
            found_addresses = []

            # 定义内存信息结构
            class MEMORY_BASIC_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("BaseAddress", ctypes.c_void_p),
                    ("AllocationBase", ctypes.c_void_p),
                    ("AllocationProtect", wintypes.DWORD),
                    ("RegionSize", ctypes.c_size_t),
                    ("State", wintypes.DWORD),
                    ("Protect", wintypes.DWORD),
                    ("Type", wintypes.DWORD)
                ]

            current_address = ctypes.c_void_p(start_address)
            mbi = MEMORY_BASIC_INFORMATION()

            # 搜索内存
            while ctypes.cast(current_address, ctypes.c_void_p).value < ctypes.cast(end_address, ctypes.c_void_p).value:
                if ctypes.windll.kernel32.VirtualQueryEx(
                        int(self.handle),
                        current_address,
                        ctypes.byref(mbi),
                        ctypes.sizeof(mbi)
                ) > 0:
                    # 检查内存是否可读
                    if mbi.State == 0x1000 and mbi.Protect & 0xFF == 0x04:
                        try:
                            # 读取内存区域
                            memory_data = self.read_memory(
                                ctypes.cast(mbi.BaseAddress, ctypes.c_void_p).value,
                                mbi.RegionSize
                            )

                            if memory_data:
                                # 搜索值
                                offset = 0
                                while True:
                                    offset = memory_data.find(search_bytes, offset)
                                    if offset == -1:
                                        break
                                    found_addresses.append(
                                        ctypes.cast(mbi.BaseAddress, ctypes.c_void_p).value + offset
                                    )
                                    offset += 1

                        except Exception as e:
                            print(f"搜索地址 {hex(ctypes.cast(current_address, ctypes.c_void_p).value)} 时出错: {e}")

                    # 移动到下一个内存区域
                    current_address = ctypes.c_void_p(
                        ctypes.cast(current_address, ctypes.c_void_p).value + mbi.RegionSize
                    )
                else:
                    break

            return found_addresses

        except Exception as e:
            print(f"搜索值时出错: {e}")
            return []

    def get_module_base(self, module_name):
        """获取指定模块的基地址"""
        for module in self.process_info['modules']:
            if module['name'].lower() == module_name.lower():
                return module['base_address']
        return None

    def get_relative_address(self, address):
        """计算相对于基地址的偏移"""
        return address - self.process_info['base_address']

    def print_process_info(self):
        """打印进程信息"""
        print(f"\n进程信息 - {self.process_name}")
        print("-" * 50)
        print(f"进程ID: {self.process_info['pid']}")
        print(f"基地址: {hex(self.process_info['base_address'])}")
        print(f"\n加载的模块:")
        print("-" * 50)
        for module in self.process_info['modules']:
            print(f"模块名: {module['name']}")
            print(f"地址: {hex(module['base_address'])}")
            print("-" * 30)

    def __del__(self):
        """清理资源"""
        if self.handle:
            win32api.CloseHandle(self.handle)




# 创建工具实例
mem_tools = MemoryTools("Plants.vs.Zombies.exe")
#
# 打印进程信息
mem_tools.print_process_info()

# 搜索整数值
addresses = mem_tools.search_value(12345, "int")
print("\n找到的地址:")
for addr in addresses:
    print(hex(addr))

# 搜索字符串
string_addresses = mem_tools.search_value("Hello World", "string")
print("\n找到的字符串地址:")
for addr in string_addresses:
    print(hex(addr))

# 获取模块基地址
kernel32_base = mem_tools.get_module_base("kernel32.dll")
if kernel32_base:
    print(f"\nkernel32.dll 基地址: {hex(kernel32_base)}")

# 写入内存示例
if addresses:
    new_value = struct.pack("i", 54321)
    mem_tools.write_memory(addresses[0], new_value)

# Use the function change coin data to Ox FF FF0000
# 文件路径
file_path = r"C:\ProgramData\PopCap Games\PlantsVsZombies\userdata\user1.dat"

# 使用示例
# 1. 修改04位置的值（输入0-40之间的数字）
modify_position_04(file_path, 26)

# 2. 修改08-09位置的值为FF
modify_position_08_09(file_path)