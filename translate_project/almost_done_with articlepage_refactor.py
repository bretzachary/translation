import json
from translate_app.models import Article, Image
from translate_app.views import photo_placement

class Test(): pass
article = Article.objects.get(pk=4)
images = Image.objects.filter(article=article)

text = json.decoder.JSONDecoder().decode(article.text)
translated_text = json.decoder.JSONDecoder().decode(article.translated_text)

text_plus_translation = list(zip(text,translated_text))
paragraph_container=[]
for i in text_plus_translation:
	test = Test()
	test.text = i[0]
	test.trans =i[1]
	paragraph_container.append(test)
print(len(paragraph_container))
paragraphs=paragraph_container

def photo_placement(images,paragraphs):
	i = len(images)
	p = len(paragraphs)

	skip_factor = int(p/i)

	#should
	img_plus_paras_list = []
	counter = 0
	for img in images:

		img_plus_paras = Test()
		img_plus_paras.img = img
		img_plus_paras.para_container = []

		for sf in range(skip_factor):
			para = paragraphs[counter:counter+1]
			img_plus_paras.para_container.append(para)
			counter+=1
	
		img_plus_paras_list.append(img_plus_paras)

	last_para_container = []
	last_paragraphs = p%i
	last_para_counter = -(last_paragraphs)
	for each in range(last_paragraphs):
		last_paras = (paragraphs[last_para_counter])
		last_para_container.append(last_paras)
		last_para_counter +=1
		#print('RRRRRRRRRRRRRRRRRRRRRRRR' + last_paras)

	img_plus_paras_list.append(last_para_container)

	return img_plus_paras_list

test = photo_placement(images, paragraphs)

for thing in test[:-1]:
	print("RRRRRRRRRRRRRR" + str(thing.img.picture))
	for each in thing.para_container:
	
		for e in each:
			print(e.text)

for p in test[-1]:
	print(p.text)


#
#
#
#test[-1] is the list of final paragraphs (after last photo)
#dont' forget to throw in the end of the article