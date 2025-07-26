import os
import zipfile
import asyncio

import pandas as pd
from googletrans import Translator
from newspaper import Article
from newspaper.configuration import Configuration


def fetch_and_translate(url, max_len=4500):
    try:
        # 配置 Article 抓取器
        config = Configuration()
        config.browser_user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        )

        article = Article(url, config=config, language='en')
        article.download()
        article.parse()

        text = article.text.strip()
        if not text:
            raise ValueError("文章内容为空")

        # 初始化翻译器
        translator = Translator(service_urls=['translate.google.com.hk'])

        # 分段翻译
        translated_chunks = []
        for i in range(0, len(text), max_len):
            chunk = text[i:i + max_len]
            try:
                translated = translator.translate(chunk, src='en', dest='zh-cn')
                translated_chunks.append(translated.text)
            except Exception as e:
                print(f"⚠️ 翻译段落失败: {e}")
                translated_chunks.append("[翻译失败段落]")

        result = ''.join(translated_chunks)
        print(f"抓取和翻译成功: {result}")
        return result

    except Exception as e:
        print(f"❌ 抓取或翻译失败: {e}")
        return None


def extract_company_sentiment(company, gdelt_dir="./data/gdelt"):
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
            df['text'] = df['url'].apply(lambda x: fetch_and_translate(x))
            rows.append(df[["date", "tone", "text"]])
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    if rows:
        all_df = pd.concat(rows)
        sentiment_df = all_df.groupby("date")["tone"].mean().reset_index()
        sentiment_df.columns = ["Date", "ToneScore"]
        return sentiment_df
    return pd.DataFrame(columns=["Date", "ToneScore"])


if __name__ == '__main__':
    company_name = "Nvidia"  # 替换为你感兴趣的公司名称
    sentiment_data = extract_company_sentiment(company_name, gdelt_dir="./data/gdelt")
    if not sentiment_data.empty:
        print(f"Sentiment data for {company_name}:")
        print(sentiment_data.head())
    else:
        print(f"No sentiment data found for {company_name}.")
