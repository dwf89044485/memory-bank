#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

LOCAL_FILES = [
    "/data/workspace/.codebuddy/rules/brief.mdc",
    "/data/workspace/.codebuddy/rules/decisions.mdc"
]

REMOTE_HOST = "root@josephdeng-any20.devcloud.woa.com"
REMOTE_PORT = "36000"
REMOTE_DIR = "/data/workspace/项目进度/memory-bank/"

def run_cmd(cmd, check=True):
    """执行命令并返回结果"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ 命令执行失败: {cmd}")
        print(f"错误: {result.stderr}")
        return False
    return True

def sync_files():
    """同步文件到总控服务器"""
    
    # Step 1: 创建目标目录
    print("\n=========================================")
    print("  同步 Memory-Bank 到总控")
    print("=========================================\n")
    
    mkdir_cmd = f'ssh -p {REMOTE_PORT} {REMOTE_HOST} "mkdir -p {REMOTE_DIR}"'
    if not run_cmd(mkdir_cmd):
        return False
    
    # Step 2: 推送文件
    success_count = 0
    for local_file in LOCAL_FILES:
        if Path(local_file).exists():
            scp_cmd = f'scp -P {REMOTE_PORT} {local_file} {REMOTE_HOST}:{REMOTE_DIR}'
            if run_cmd(scp_cmd):
                filename = Path(local_file).name
                print(f"✅ {filename} 已推送")
                success_count += 1
        else:
            filename = Path(local_file).name
            print(f"⚠️ {filename} 不存在，跳过")
    
    # Step 3: 显示结果
    print()
    print("=========================================")
    print("✅ Memory-Bank 同步完成")
    print("=========================================\n")
    print(f"推送位置：{REMOTE_HOST}:{REMOTE_PORT}{REMOTE_DIR}")
    
    return success_count > 0

if __name__ == "__main__":
    success = sync_files()
    sys.exit(0 if success else 1)
