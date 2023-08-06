# -*- coding: utf-8 -*-
#

import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()

version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

__main_version__ = "%s.%s.x" % (version_info[0], version_info[1])

del pkgutil

from .api import *
from .indicators import *

from .data.zealink_data_backend import ZealinkDataBackend
from .context import ExecutionContext as funcat_execution_context
import datetime
funcat_execution_context(date=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d"),
                         order_book_id="000001.sh",
                         data_backend=ZealinkDataBackend())._push()
