import os
from datetime import datetime, timedelta

import requests


def download_large_file(url, save_path, chunk_size=1024):
    try:
        for i in range(3):  # 重试3次
            try:
                # 启用流式下载
                response = requests.get(url, stream=True, timeout=120)
                # 检查响应状态
                response.raise_for_status()
                # 打开目标文件并逐块写入
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # 过滤掉空块
                            f.write(chunk)
                print(f"文件已成功下载到: {save_path}")
                break  # 如果成功，跳出重试循环
            except requests.exceptions.RequestException as e:
                print(f"下载失败，正在重试... ({i + 1}/3) 错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")


def download_gdelt_csvs(start_date, end_date, save_dir="./data/gdelt"):
    base_url = "http://data.gdeltproject.org/events/"
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    while current <= end:
        filename = current.strftime("%Y%m%d") + ".export.CSV.zip"
        url = base_url + filename
        filepath = os.path.join(save_dir, filename)
        if not os.path.exists(filepath):
            print("Downloading %s" % filename)
            download_large_file(url, filepath)
        else:
            print(f"File {filename} already exists")
        current += timedelta(days=1)


if __name__ == '__main__':
    start_date = "2025-01-01"
    end_date = "2025-01-10"
    download_gdelt_csvs(start_date, end_date)
    print("Download completed.")
