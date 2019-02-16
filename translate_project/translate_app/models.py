from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

def user_directory_path(instance, filename):
	return 'articles/{}/images/filename'.format(instance.article.slug)

class Article(models.Model):
	
	url = models.URLField()
	section = models.CharField(max_length=128, null=True)
	publisher = models.CharField(max_length=128, default='nytimes')
	title = models.CharField(max_length=512, unique=True)
	subtitle = models.CharField(max_length=512, null=True)
	slug = models.SlugField(max_length=512)
	author = models.CharField(max_length=128, null=True)
	date = models.DateField(auto_now=True)
	text = models.TextField()
	translated_text = models.TextField(null=True)
	
	readers = models.ManyToManyField(User,through='ArticleViews', blank=True, null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Article, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

class Image(models.Model):
	article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
	picture = models.ImageField(upload_to=user_directory_path, blank=True)
	caption = models.CharField(max_length=512, null=True)

	def __str__(self):
		return self.article.title

class Tag(models.Model):
	article = models.ManyToManyField(Article)
	tag = models.CharField(max_length=128)

	def __str__(self):
		return self.tag

class ArticleViews(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
	date_viewed = models.DateField(auto_now=True)

class ArticleWords(models.Model):
	article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True)
	all_words = models.TextField()
	most_common_words = models.TextField()
	tfidf_words = models.TextField()

class RegistrationCode(models.Model):
	code = models.CharField(max_length=128)

	def __str__(self):
		return self.code

#class Section(models.Model):
#	article = models.ManyToManyField(Article)
#	section = models.CharField(max_length=128)
#
#	def __str__(self):
#		return self.section

