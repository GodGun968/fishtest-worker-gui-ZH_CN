import os
import struct
import subprocess
import sys

GUARD_CF = 0x4000


def clear_guard_cf(path):
    with open(path, "r+b") as handle:
        dos = handle.read(64)
        if dos[:2] != b"MZ":
            raise ValueError("不是有效的 PE 文件")
        pe_offset = struct.unpack_from("<I", dos, 0x3C)[0]
        handle.seek(pe_offset)
        if handle.read(4) != b"PE\x00\x00":
            raise ValueError("无效的 PE 签名")
        handle.read(20)
        magic = struct.unpack("<H", handle.read(2))[0]
        if magic not in (0x10B, 0x20B):
            raise ValueError(f"未知 PE 可选头: {magic:#x}")
        handle.seek(pe_offset + 24 + 70)
        dll_characteristics = struct.unpack("<H", handle.read(2))[0]
        if dll_characteristics & GUARD_CF:
            handle.seek(pe_offset + 24 + 70)
            handle.write(struct.pack("<H", dll_characteristics & ~GUARD_CF))
            return True
    return False


def run_upx(path):
    commands = (
        ["upx", "--best", "--lzma", path],
        ["upx", "--best", "--lzma", "--force", path],
        ["upx", "-9", "--force", path],
    )
    last_error = None
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        output = (result.stdout or "") + (result.stderr or "")
        print(output.strip())
        if result.returncode == 0:
            return
        last_error = output.strip() or f"退出码 {result.returncode}"
        if "already packed" in output.lower():
            return
    raise RuntimeError(f"UPX 压缩失败: {last_error}")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: python tools/pack_exe.py <exe>")
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        raise SystemExit(f"找不到文件: {path}")

    before = os.path.getsize(path)
    if clear_guard_cf(path):
        print("已关闭 PE Control Flow Guard，以便 UPX 压缩")
    run_upx(path)
    after = os.path.getsize(path)
    print(f"UPX 前: {before:,} 字节")
    print(f"UPX 后: {after:,} 字节")
    if after >= before:
        raise SystemExit("压缩后体积未减小")
    saved = (before - after) / before * 100
    print(f"已减小 {saved:.1f}%")


if __name__ == "__main__":
    main()
