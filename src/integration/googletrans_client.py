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
