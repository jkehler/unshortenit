from unittest import TestCase
import unshortenit


class TestUnshortenIt(TestCase):

    def test_adfly(self):
        if unshortenit.adfly_support:
            self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                             ('http://www39.zippyshare.com/v/69303767/file.html', 200))
            self.assertEqual(unshortenit.unshorten('http://adf.ly/1icWR'),
                             ('http://adf.ly/1icWR', 'No ysmm variable found'))
            self.assertEqual(unshortenit.unshorten('http://links.devitrianto.com/yy', type='adfly'),
                             ('http://www.sendspace.com/file/a2z6ji', 200))
        else:
            self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                             ('http://adf.ly/WzXu2', 'adf.ly not supported. Install PyV8 to add support.'))

    def test_linkbucks(self):
        self.assertEqual(unshortenit.unshorten('http://4647ed8c.linkbucks.com/'),
                         ('http://www.filedownloads.org/1rpnb9dudo7o/My_Backup_Pro_v3.2.5zz.zip.html', 200))

    def test_adfocus(self):
        self.assertEqual(unshortenit.unshorten('http://adfoc.us/340347863622'), ('http://www7.zippyshare.com/', 404))

    def test_lnxlu(self):
        self.assertEqual(unshortenit.unshorten('http://lnx.lu/1CKw'), ('http://www.reddit.com/', 200))

    def test_generic(self):
        self.assertEqual(unshortenit.unshorten('http://ul.to'), ('http://uploaded.net/', 200))
        self.assertEqual(unshortenit.unshorten('http://t.co/fsbtLWPUIJ'),
                         ('http://www.igen.fr/app-store/drift-mania-street-outlaws-du-drift-son-paroxysme-108452', 200))
        self.assertEqual(unshortenit.unshorten('http://p.ost.im/d7DPHP'),
                         ('http://crazymikesapps.com/drift-mania-street-outlaws-video-review/', 200))
