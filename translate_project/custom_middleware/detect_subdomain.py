class SubdomainLanguage:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		#host = request.META.get('HTTP_HOST', '')
		host = request.META.get('HTTP_HOST', '').split('.')[0]

		request.subdomain_language = host
		response = self.get_response(request)

		return response

    # def process_request(self, request):
    #   host = request.META.get('HTTP_HOST', '')
    #    request.subdomain_language = host
        #host = host.replace('www.', '').split('.')
        #if len(host) > 2:
        #    request.subdomain = ''.join(host[:-2])
        #else:
        #    request.subdomain = None

        #try:
        #    request.session['subdomain_language'] = request.META['HTTP_HOST'].split('.')[0]
        #except KeyError:
        #    pass

