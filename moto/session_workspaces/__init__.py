from __future__ import unicode_literals
from .models import sess_backend

sess_backends = {"global": sess_backend}
mock_sess = sess_backend.decorator
mock_sess_deprecated = sess_backend.deprecated_decorator
