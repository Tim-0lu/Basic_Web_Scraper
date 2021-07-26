import string
import requests
import os
from bs4 import BeautifulSoup

url = "https://www.nature.com/nature/articles"
core_url="https://www.nature.com"
r = requests.get(url)
page_num = int(input())
article_type = input()

def grab_page(link):
  print(link)
  r = requests.get(link)
  if r:
    soup = BeautifulSoup(r.content, "html.parser")
    body = soup.find('div', {"class":"c-article-body u-clearfix"})
    if body:
      return body.text
    else:
      body = soup.find('div', {"class":"article-item__body"})
      return body.text

def save_to_file(fname, title, body, i):
  with open(os.path.join(f'Page_{i}', fname), "wb") as f:
    f.write(body)

i = 1
while i <= page_num:
  os.mkdir(f"Page_{i}")
  parameters = {'searchType':'journalSearch','sort':'PubDate', 'page':i}
  r = requests.get(url, params=parameters)
  if r:
      soup = BeautifulSoup(r.content, "html.parser")
      # print(type(soup))

      articles = soup.find_all("article")
      a = soup.find_all("article", {
          "class": ["u-full-height", "c-card", "c-card--flush"]})
      for tags in a:
        children = tags.findChildren()
        for c in children:
          if c.name == "span":
            if "data-test" in c.attrs:
              if (c.span.text == article_type):
                title = str(tags.h3.text)
                title = title.strip()
                title = title.translate(str.maketrans('', '', string.punctuation))
                title = title.replace(" ", "_")
                a_link = core_url + tags.a['href']
                fname = title+".txt"
                body = grab_page(a_link)
                body = body.encode("utf-8")
                title = title.encode("utf-8")
                save_to_file(fname, title, body, i)
  else:
      print(f"The URL returned {r.status_code}")
  i += 1
print("Saved all articles.")
