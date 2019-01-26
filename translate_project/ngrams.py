#in the repl there is a good link for lang processing resource/code

import json
import re
from translate_app.models import Article

#re.sub("[,.-']",' ', ss]
corpus = []

arts= Article.objects.all()
for art in arts:
	translated_text = json.decoder.JSONDecoder().decode(art.translated_text)
	for text in translated_text:
			corpus.append(text)
string_corpus = ' '.join(corpus)

def find_ngrams(s, n):
	s=s.lower()
	s=re.sub(r"[,.-/']",' ',s)
	tokens = [token for token in s.split(" ") if token !=""]
	ngrams= zip(*[tokens[i:] for i in range(n)])
	return [" ".join(ngram) for ngram in ngrams]

s = find_ngrams(string_corpus, 1)
from collections import Counter
s_counter = Counter(s)
s_counter.most_common(800)