import os
import zipfile
from datetime import datetime, timedelta
import src.integration.googletrans_client as googletrans_client
import pandas as pd
import requests
import src.utils.project_util as project_util


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


def download_gdelt_csvs(start_date, end_date, save_dir):
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


def get_company_sentiment(company, start_date, end_date):
    gdelt_dir = f"{project_util.get_root_path()}/src/integration/temp/gdelt"
    download_gdelt_csvs(start_date=start_date, end_date=end_date, save_dir=gdelt_dir)
    rows = []
    for file in os.listdir(gdelt_dir):
        if not file.endswith(".zip"):
            continue
        zf = zipfile.ZipFile(os.path.join(gdelt_dir, file))
        names = zf.namelist()[0]

        try:
            df = pd.read_csv(zf.open(names), sep="\t", header=None, dtype=str)
            df = pd.DataFrame({
                "date": pd.to_datetime(df[1], format="%Y%m%d"),
                "actor1": df[6],
                "actor2": df[16],
                "tone": pd.to_numeric(df[34], errors="coerce"),
                "url": df[57]
            })
            df = df[
                df["actor1"].str.contains(company, na=False, case=False) | df["actor2"].str.contains(company, na=False,
                                                                                                     case=False)]
            # df["text"] = df['url'].apply(lambda x: googletrans_client.fetch_and_translate(x))
            rows.append(df[["date", "tone"]])
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    if rows:
        all_df = pd.concat(rows)
        sentiment_df = all_df.groupby("date")["tone"].mean().reset_index()
        sentiment_df.columns = ["Date", "ToneScore"]
        return sentiment_df
    return pd.DataFrame(columns=["Date", "ToneScore"])


sentiment_df = get_company_sentiment(company="Nvidia", start_date='2025-07-20', end_date='2025-07-30')
print(sentiment_df.head(10))
