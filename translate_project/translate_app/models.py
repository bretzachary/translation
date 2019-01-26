from django.contrib.auth.models import User
from django.db import models

def user_directory_path(instance, filename):
	return 'articles/{}/images/filename'.format(instance.article.slug)

# Create your models here.
class Article(models.Model):
	publisher = models.CharField(max_length=128, default='nytimes')
	url = models.URLField()
	title = models.CharField(max_length=512, unique=True)
	slug = models.SlugField(max_length=512)
	date = models.DateField(auto_now=True)
#	author = models.CharField()
	text = models.TextField()
	translated_text = models.TextField()
#	images = models.IntegerField(default=0)
	section = models.CharField(max_length=128, null=True)
	readers = models.ManyToManyField(User,through='ArticleViews', blank=True, null=True)

	def __str__(self):
		return self.title

class Image(models.Model):
	article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)
	picture = models.ImageField(upload_to=user_directory_path, blank=True)
#	filename = models.
	caption = models.CharField(max_length=512, null=True)
#	article_number = models.IntegerField(default=0)

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





#class Section(models.Model):
#	article = models.ManyToManyField(Article)
#	section = models.CharField(max_length=128)
#
#	def __str__(self):
#		return self.section

