# coding=utf-8

import re
import time
import logging
import traceback

logger = logging.getLogger(__name__)


clean_whitespace_re = re.compile(r'\s+')


class PunctuationMixin(object):
    """
    provider mixin

    fixes show ids for stuff like "Mr. Petterson", as our matcher already sees it as "Mr Petterson" but addic7ed doesn't
    """

    def clean_punctuation(self, s):
        return s.replace(".", "").replace(":", "").replace("'", "").replace("&", "").replace("-", "")

    def clean_whitespace(self, s):
        return clean_whitespace_re.sub("", s)

    def full_clean(self, s):
        return self.clean_whitespace(self.clean_punctuation(s))


class ProviderRetryMixin(object):
    def retry(self, f, amount=2, exc=Exception, retry_timeout=10):
        i = 0
        while i <= amount:
            try:
                return f()
            except exc:
                formatted_exc = traceback.format_exc()
                i += 1
                if i == amount:
                    raise

            logger.debug(u"Retrying %s, try: %i/%i, exception: %s" % (self.__class__.__name__, i, amount, formatted_exc))
            time.sleep(retry_timeout)
