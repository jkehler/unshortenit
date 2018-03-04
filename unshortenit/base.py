from .unshortener import Unshortener
from .modules import AdfLy, AdFocus, ShorteSt, MetaRefresh

unshortener = Unshortener()
unshortener.register_modules([
    AdfLy(),
    AdFocus(),
    ShorteSt(),
    MetaRefresh()
])
