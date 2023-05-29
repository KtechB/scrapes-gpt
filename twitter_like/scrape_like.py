#%%
from bs4 import BeautifulSoup

# HTMLファイルを開く
with open('./data_0508.html') as f:
    html = f.read()

# BeautifulSoupオブジェクトを生成
soup = BeautifulSoup(html, 'html.parser')

# <article>タグを取得
article_tags = soup.find_all('article')
print(article_tags)

# <article>タグ以下のテキストを取得
# texts = [article.get_text() for article in article_tags]

# print(texts)
# %%
soup.
