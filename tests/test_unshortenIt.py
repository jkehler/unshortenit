from unittest import TestCase
import unshortenit


class TestUnshortenIt(TestCase):

    def test_adfly(self):
        if unshortenit.adfly_support:
            self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                             ('http://www39.zippyshare.com/v/69303767/file.html', 200))
            self.assertEqual(unshortenit.unshorten('http://adf.ly/1icWR'),
                             ('http://adf.ly/1icWR', 'No ysmm variable found'))
        else:
            self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                             ('http://adf.ly/WzXu2', 'adf.ly not supported. Install PyV8 to add support.'))

    def test_linkbucks(self):
        self.assertEqual(unshortenit.unshorten('http://4647ed8c.linkbucks.com/'),
                         ('http://www.filedownloads.org/1rpnb9dudo7o/My_Backup_Pro_v3.2.5zz.zip.html', 200))

    def test_adfocus(self):
        self.assertEqual(unshortenit.unshorten('http://adfoc.us/304385708634'), ('http://naughtywebcams.us', 200))

    def test_lnxlu(self):
        self.assertEqual(unshortenit.unshorten('http://lnx.lu/1CKw'), ('http://www.reddit.com/', 200))

    def test_generic(self):
        self.assertEqual(unshortenit.unshorten('http://ul.to'), ('http://uploaded.net/', 200))
