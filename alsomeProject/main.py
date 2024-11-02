import csv
import psutil
import time
from typing import Optional, List, Dict, Union
import ctypes
from ctypes import wintypes
import struct


class MemoryScanner:
    def __init__(self, process_name: str):
        """初始化内存扫描器"""
        self.process_name = process_name
        self.process = None
        self.process_handle = None
        self._initialize_process()

    def _initialize_process(self):
        """初始化进程句柄"""
        for proc in psutil.process_iter():
            try:
                proc_name = proc.name()  # 直接调用 name() 方法而不是使用 info['name']
                if proc_name == self.process_name:
                    self.process = proc
                    # 获取进程句柄
                    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                    PROCESS_ALL_ACCESS = 0x1F0FFF
                    self.process_handle = kernel32.OpenProcess(
                        PROCESS_ALL_ACCESS,
                        False,
                        proc.pid
                    )
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if not self.process:
            raise Exception(f"未找到进程: {self.process_name}")

    def read_memory(self, address: int, size: int) -> bytes:
        """读取指定地址的内存"""
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        success = ctypes.windll.kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        if not success:
            raise WindowsError(ctypes.get_last_error())
        return buffer.raw

    def scan_memory_region(self, value: Union[int, float], data_type: str) -> List[int]:
        """扫描内存区域查找匹配值"""
        found_addresses = []
        size_map = {
            'int': 4,
            'float': 4,
            'double': 8
        }

        try:
            for mapping in self.process.memory_maps():
                try:
                    start_addr = int(mapping.addr.split('-')[0], 16)
                    end_addr = int(mapping.addr.split('-')[1], 16)

                    # 读取内存区块
                    current_addr = start_addr
                    while current_addr < end_addr:
                        try:
                            data = self.read_memory(current_addr, size_map[data_type])

                            # 根据数据类型进行值比较
                            if data_type == 'int':
                                read_value = struct.unpack('i', data)[0]
                            elif data_type == 'float':
                                read_value = struct.unpack('f', data)[0]
                            elif data_type == 'double':
                                read_value = struct.unpack('d', data)[0]

                            if abs(read_value - value) < 0.0001:  # 使用近似比较
                                found_addresses.append(current_addr)

                        except (WindowsError, struct.error):
                            pass
                        current_addr += size_map[data_type]

                except (ValueError, AttributeError):
                    continue
        except psutil.AccessDenied:
            print("警告: 某些内存区域访问被拒绝")

        return found_addresses


class GameScanner:
    def __init__(self, csv_path: str, process_name: str):
        """初始化游戏扫描器"""
        self.game_data = self._load_csv(csv_path)
        self.memory_scanner = MemoryScanner(process_name)

    def _load_csv(self, csv_path: str) -> Dict:
        """加载CSV文件数据"""
        game_data = {}
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                game_data[row['id']] = {
                    'cn_name': row['cn_name'],
                    'en_name': row['en_name'],
                    'damage': float(row['damage']),
                    'health': float(row['health']),
                    'cost': float(row['cost'])
                }
        return game_data

    def scan_by_id(self, item_id: str, scan_type: str = 'health', interval: int = 5, duration: int = 30):
        """根据ID扫描内存"""
        if item_id not in self.game_data:
            raise ValueError(f"未找到ID: {item_id}")

        value_to_scan = self.game_data[item_id][scan_type]
        end_time = time.time() + duration

        print(f"开始扫描 {self.game_data[item_id]['cn_name']} 的 {scan_type}")
        print(f"扫描值: {value_to_scan}")

        previous_addresses = set()
        while time.time() < end_time:
            try:
                current_addresses = set(self.memory_scanner.scan_memory_region(
                    value_to_scan,
                    'float' if scan_type in ['damage', 'health'] else 'int'
                ))

                if previous_addresses:
                    stable_addresses = current_addresses.intersection(previous_addresses)
                    if stable_addresses:
                        print("\n发现稳定地址:")
                        for addr in stable_addresses:
                            print(f"0x{addr:X}")

                previous_addresses = current_addresses
                time.sleep(interval)
            except Exception as e:
                print(f"扫描过程中出错: {str(e)}")
                break


def main():

    scanner = GameScanner('game_data.csv', 'game_process.exe')
    try:
        scanner.scan_by_id('1001', 'health', interval=5, duration=30)
    except Exception as e:
        print(f"wrong scan: {str(e)}")


if __name__ == "__main__":
    main()
