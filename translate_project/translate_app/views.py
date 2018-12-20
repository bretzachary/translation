from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import translate

def index(request, link = None):
	if link is None:
		translator = translate.r_s()
	else:
		translator = translate.r_s(link)
	text = translator.translate_text()
	context_dict = {'boldmessage': text}

#	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	return render(request, 'translate_app/index.html', context=context_dict)

def input_link_page(request):
	if request.method == 'POST':
		print(request.POST['link'])
		link = request.POST['link']
	
	#	return HttpResponseRedirect(reverse('index'))#, args=[link]))
		return index(request,link)
	return render(request, 'translate_app/input_link_page.html')