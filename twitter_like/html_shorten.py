#%%
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from bs4.formatter import Formatter
#%%
from dataclasses import dataclass
import feedparser
import requests
import tiktoken


def count_token(text: str):
    enc = tiktoken.get_encoding("gpt2")
    return len(enc.encode(text))


@dataclass
class Entry:
    title: str
    link: str
    summary: str


def fetch_feed(url: str) -> list[Entry]:
    d: dict = feedparser.parse(url)
    # %%

    entries: list[Entry] = []
    for i, e in enumerate(d["entries"]):
        entries.append(Entry(e.get("title", ""), e.get("link"), e.get("summary", "")))
    return entries


def get_html(url: str):
    response = requests.get(url)
    return response.text

#%%

# HTMLを解析する
html = "<html><body><div class='container'><h1>Hello, world!</h1><p>aa</p><p>bb</p></div></body></html>"
soup = BeautifulSoup(html, 'html.parser')

hierarchy = soup.prettify()
# 属性を取得する
attrs = {}
for tag in soup.find_all():
    attrs[str(tag)] = tag.attrs

# 結果を表示する
print(hierarchy)
print(attrs)
#%%
from bs4 import BeautifulSoup
long_text= "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
html = f"<html><body><div class='container'><h1>Hello, world!</h1><p>{long_text}</p><p>bb</p></div></body></html>"
def extract_structure(html):
    soup = BeautifulSoup(html, 'html.parser')
    structure = []

    def traverse(node, depth=0):
        if node.name:
            info = {
                'depth': depth,
                'tag': node.name,
                'class': node.get('class'),
                'id': node.get('id'),
            }
            structure.append(info)
            for child in node.children:
                traverse(child, depth + 1)

    traverse(soup)
    return structure

html = html
structure = extract_structure(html)

print(structure)
for s in structure:
    print(f"Depth: {s['depth']}, Tag: {s['tag']}, Class: {s['class']}, ID: {s['id']}")


#%%
# decompose

from bs4 import BeautifulSoup

long_text= "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
html = f"<html><body><div class='container' href='https://google.com'><h1>Hello, world!</h1><p>{long_text}</p><p>bb</p></div></body></html>"
def remove_elements(html, tag_names, attrs={}):
    soup = BeautifulSoup(html, 'html.parser')
    for tag_name in tag_names:
        for tag in soup.findAll(tag_name, attrs):
            tag.decompose()

    return str(soup)

def shorten_html(html:str, max_length:int):
    soup = BeautifulSoup(html, 'html.parser')

    def shorten_text(node, max_length):
        if isinstance(node, NavigableString):
            if len(node) > max_length:
                # print(node.get_text().strip())
                node.replace_with(node[:max_length] + '...' + f"length: {len(node)}")
        else:
            for child in node.children:
                shorten_text(child,max_length)

    shorten_text(soup,max_length)

    return str(soup)
def keep_only_certain_attributes(html, keep_attrs):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all(True):  # Trueを指定して全てのタグを対象にする
        tag.attrs = {key: value for key, value in tag.attrs.items() if key in keep_attrs}

    return str(soup)
def apply_formatter(html):
    soup = BeautifulSoup(html, 'html.parser')
    return str(soup.prettify())

def remove_head(html):
    soup = BeautifulSoup(html, 'html.parser')

    # head要素を見つけて取り除く
    if soup.head:
        soup.head.decompose()

    return str(soup)

def remove_comment(html):
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return str(soup)


#%%

import os
print(os.getcwd())
with open("./data_0508.html", 'r') as f:
    html = "".join(f.readlines())
html =  get_html("https://ai.googleblog.com/2023/04/google-at-iclr-2023.html")

tag_names = ["head", "style", "noscript", "meta",'img', 'input', 'br', 'hr', 'link',  'area', 'base' ]  # 除去したいタグ名
attrs = {}  # 除去したいタグの属性
keep_attrs = ["class", ""]
html = remove_head(html)
html = remove_elements(html, tag_names, attrs)
html = keep_only_certain_attributes(html, keep_attrs)
html = shorten_html(html,max_length=30 )

print(apply_formatter(html), len(html))


# %%
# extract main texts


html =  get_html("https://ai.googleblog.com/2023/05/foundation-models-for-reasoning-on.html")

def extract_text_from_elements(html):
    tags = ["p", "h1", "h2", "h3", "h4", "h5","h6"]
    prefix_dict={"h1":"# ", "h2":"## ", "h3":"###", "h4":"####", "h5":"#####", "h6":"######"}
    soup = BeautifulSoup(html, 'html.parser')
    texts = []
    elements = soup.find_all(tags)
    for element in elements:
        text = element.get_text(strip=True)

        tag = element.name 
        print(tag)
        prefix = prefix_dict.get(tag, "")
        if len(text)>0:
            texts.append(prefix+text)
    return texts

def extract_article_if_exist(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all("article")
    if len(articles)>1:
        return  "\n".join(([str(a) for a in articles]))
    else:
        return html
        
tag_names = ["head", "style", "noscript", "meta",'input','hr', 'link',  'area', 'base',"header","footer","nav" ]  # 除去したいタグ名
html = remove_elements(html, tag_names, attrs)
html = extract_article_if_exist(html)

texts = extract_text_from_elements(html)
# %%
main_texts = "\n".join(texts)
# %%

count_token(main_texts)
# %%
