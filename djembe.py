import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = 'opimw^i08$bo@8v%)7lodcum6=elvd+elco31q!yhmpdis9#cv'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = ('django.contrib.staticfiles',)
MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	"django.core.context_processors.csrf",
	"django.core.context_processors.static",
	"__main__.extra_context",
	"django.contrib.messages.context_processors.messages"
)
ROOT_URLCONF = '__main__'
WSGI_APPLICATION = '__main__.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),}}
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
TEMPLATE_LOADERS = ('coffin.contrib.loader.AppLoader', 'coffin.contrib.loader.FileSystemLoader',)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
TEMPLATE_DIRS = [os.path.join(BASE_DIR, "templates")]

def extra_context(request):
	from django.conf import settings
	return {"settings": settings}

####################################################################################################################

from django.conf.urls import patterns, url
from django.core.paginator import Paginator


from faker import Faker

class PseudoModelBase(dict):
	def __getitem__(self, key):
		if key == "keys":
			return self.get_keys()
		if key in self:
			return dict.__getitem__(self, key)
		faker = getattr(self.faker, key, None)
		if faker and callable(faker):
			value = faker()
			dict.__setitem__(self, key, value)
			return value
		return "(%s)" % key

	def get_keys(self):
		keys = set()
		for val in dir(self.faker):
			if not (val.startswith("_") or val.startswith("py")):
				try:
					if callable(getattr(self.faker, val)):
						keys.add(val)
				except:
					pass
		return sorted(keys)


def pseudo_model_factory(seed):
	faker = Faker()
	faker.seed(seed)
	return type('PseudoModel_%d' % seed, (PseudoModelBase,), {"faker": faker})

class LazyList(list):
	def __init__(self, length, func):
		self._length = length
		self._func = func
		self._initialized = False
		list.__init__(self)

	def _check(self):
		if not self._initialized:
			self[:] = [self._func() for x in xrange(self._length)]
			self._initialized = True

	def __len__(self):
		self._check()
		return list.__len__(self)

	def __nonzero__(self):
		self._check()
		return list.__nonzero__(self)

	def __iter__(self):
		self._check()
		return list.__iter__(self)
	
	def __getitem__(self, key):
		self._check()
		return list.__getitem__(self, key)

def view(request, path):
	from django.shortcuts import render
	path = (path or "index").strip("/")

	seed = hash(path)

	return render(request, [path + ".html", path + ".jinja"], {
		"object":			pseudo_model_factory(seed << 1)(),
		"ten_objects":		LazyList(10, pseudo_model_factory(seed << 2)),
		"fifty_objects":	LazyList(50, pseudo_model_factory(seed << 3)),
		"paginator":		Paginator(LazyList(5000, pseudo_model_factory(seed << 4)), 30)
	})

urlpatterns = patterns('',
	url(r'^(?P<path>[^.]*)$', view, name='view'),
)

_application = None

def application(environ, start_response):
	global _application
	if not _application:
		from django.core.wsgi import get_wsgi_application
		_application = get_wsgi_application()
	return _application(environ, start_response)

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
