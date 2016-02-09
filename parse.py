#!/usr/bin/python
import feedparser
import datetime
import codecs
import gettext
import newspaper
from tldextract import tldextract
from newspaper import Article

#pull recent Instapaper links and create RTF summary file - replace URL with your 'unread' RSS feed

d = feedparser.parse("https://www.instapaper.com/rss/000000/key")
timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

today = datetime.datetime.now()
week_ago = today -datetime.timedelta(days=7)
rtf = "{\\rtf1\\ansi\\ansicpg1252\\deff0\\deftab720{\\fonttbl{\\f0\\fswiss MS Sans Serif;}{\\f1\\froman\\fcharset2 Symbol;}{\\f2\\fmodern\\fprq1 Courier New;}{\\f3\\froman Times New Roman;}}{\\colortbl\\red0\\green0\\blue0;\\red0\\green0\\blue255;\\red255\\green0\\blue0;}\\deflang1033\\horzdoc{\\*\\fchars }{\\*\\lchars}"

#select only stories in past 7 days and create list for comparison in next step
filtered = []
for post in d.entries:
 pubdate = datetime.datetime.strptime(post.published,'%a, %d %b %Y %H:%M:%S GMT')
 if pubdate >= week_ago:
  filtered.append(post.title)
selections = filtered

#compare selected set to full RSS feed and extract headline, description, link. Run text through NLP and extract summary.
news = []
for selection in selections:
	for post in d.entries:
			if selection in post.title:
				current_article = Article(url=post.link, language='en')
				current_article.download()
				current_article.parse()
				current_article.nlp()
				#bad hack to add a space between sentences.
				summary = current_article.summary.replace('.','. ')
				title = post.title
				news.append('\\b ' + title + '\\b0\\par ' + summary + '\\par ' + '{\\field{\\*\\fldinst HYPERLINK '+ post.link + '}{\\fldrslt ' + post.link + '}}')
    
newsletter =  "\\par\\par".join(news)

#Opens and writes file to local drive with 'cp1252' encoding for the RTF file.
f = codecs.open('/Users/user/documents/Newsletter/newsletter'+ timestamp + '.rtf', 'w', encoding="cp1252")
f.write(rtf)
f.write(newsletter + "\par")
f.write("}")
f.close()
