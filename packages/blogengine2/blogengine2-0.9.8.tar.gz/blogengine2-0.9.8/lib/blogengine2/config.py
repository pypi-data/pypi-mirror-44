#from exc import *
#from database import *

# avoid circular imports
#from notmm.utils.django_settings import LazySettings
#settings = LazySettings(autoload=True)
#db = open_database(settings.SCHEVO['DATABASE_NAME'])

# i18n/py3k stuff
gettext_noop = lambda x: str(x)
_ = gettext_noop

# authentication+authorization
try:
    from authkit.authorize.decorators import authorize
    from authkit.permissions import RemoteUser, UserIn
except ImportError:
    raise ImportError("Please install the `libauthkit` package with pip.")

from schevo.error import TransactionFieldsNotChanged

# experimental memcache support
#from notmm.utils.memcache import MemcacheStore
#memcache_store = MemcacheStore(settings)

#settings = SettingsProxy(autoload=True).get_settings()

### public functions
environ_getter = lambda req, s: req.environ[s]

# see http://wiki.pylonshq.com/display/pylonsdocs/Form+Handling
# permanent_store = os.path.join(settings.MEDIA_ROOT, 'uploads')
