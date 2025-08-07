import os
import random

def generate_unity_compatible_binary(file_path, size=8192):
    """
    生成可被Unity识别为TextAsset且仍以Hex视图打开的二进制文件
    关键：使用.bytes扩展名，同时保持非文本特征
    """
    # 1. 保持反文本字节集（同之前的强二进制方案）
    anti_text_bytes = []
    anti_text_bytes.extend(range(1, 10))  # 0x01-0x09
    anti_text_bytes.extend(range(11, 32)) # 0x0B-0x1F
    anti_text_bytes.append(127)           # DEL字符
    anti_text_bytes.extend(range(0xC0, 0xFF + 1))  # 高字节
    
    # 2. 生成二进制数据（不含任何文本特征）
    binary_data = bytearray()
    for _ in range(size):
        while True:
            byte = random.choice(anti_text_bytes)
            # 避免连续相同字节
            if len(binary_data) >= 3 and byte == binary_data[-1] == binary_data[-2] == binary_data[-3]:
                continue
            # 禁止换行/回车
            if byte in (0x0D, 0x0A):
                continue
            break
        binary_data.append(byte)
    
    # 3. 关键：使用.bytes扩展名（Unity会识别为TextAsset）
    if not file_path.endswith(".bytes"):
        file_path = os.path.splitext(file_path)[0] + ".bytes"
    
    # 写入文件
    with open(file_path, 'wb') as f:
        f.write(binary_data)
    
    print(f"已生成Unity兼容的二进制文件：{file_path}，大小：{size}字节")

# 使用示例
if __name__ == "__main__":
    # 必须使用.bytes扩展名
    generate_unity_compatible_binary("unity_binary.bytes", size=16384)