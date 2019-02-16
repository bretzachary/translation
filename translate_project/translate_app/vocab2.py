
from .models import ArticleWords
import json
from ngrams import *
from random import sample

# could instead maybe use a signal for this
def update_articlewords(article):
	words_container = []
	articlewords = ArticleWords.objects.get_or_create(article=article)[0]

	text = json.decoder.JSONDecoder().decode(article.translated_text)

	for para in text:
		words_container.append(para)
	words_container=' '.join(words_container)
	unique_words_in_article = set(find_ngrams(words_container,1))
	unique_words_forjson = ' '.join(unique_words_in_article)

	articlewords.all_words = json.dumps(unique_words_forjson)



	with open('_800_most_common_words.txt', encoding='utf-8') as doc:
		_800_common_words = set([line.strip() for line in doc]) #taking set because of a few duplicates

	uwa = unique_words_in_article
	#uwa = set(find_ngrams(uwa,1))
	uwa = set(uwa & _800_common_words)

	print('Vocab2:')
	print(str(type(uwa)))
	print(str(type(list(uwa))))
	print('list:')
	print(list(uwa))

	articlewords.most_common_words = json.dumps(list(uwa))

	articlewords.save()
