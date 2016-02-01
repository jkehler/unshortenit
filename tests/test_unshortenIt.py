from unittest import TestCase
import unshortenit


class TestUnshortenIt(TestCase):

    def test_adfly(self):
        self.assertEqual(unshortenit.unshorten_only('http://adf.ly/WzXu2'),
                         ('http://www39.zippyshare.com/v/69303767/file.html', 200))
        self.assertEqual(unshortenit.unshorten_only('http://adf.ly/1icWR'),
                         ('http://adf.ly/1icWR', 'No ysmm variable found'))
        self.assertEqual(unshortenit.unshorten_only('http://links.devitrianto.com/yy', type='adfly'),
                         ('http://www.sendspace.com/file/a2z6ji', 200))

        # File has been DMCA removed, so if we allow the 301 HEAD request to resolve, it returns a different URL.
        # Also - sidenote: Pirated files in your unit tests? Really?
        self.assertEqual(unshortenit.unshorten_only('http://adf.ly/bJ8mm'),
                         ('http://www.mediafire.com/download/cixal2y0auya19m/com.ratrodstudio.skateparty2.zip', 200))



    def test_adfly_2(self):
        self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                         ('http://www39.zippyshare.com/v/69303767/file.html', 200))
        self.assertEqual(unshortenit.unshorten('http://adf.ly/1icWR'),
                         ('http://adf.ly/1icWR', 'No ysmm variable found'))
        self.assertEqual(unshortenit.unshorten('http://links.devitrianto.com/yy', type='adfly'),
                         ('https://www.sendspace.com/file/a2z6ji', 200))   # sendspace HEAD responses force HTTPS

    # def test_linkbucks(self):
    #     self.assertEqual(unshortenit.unshorten('http://4647ed8c.linkbucks.com/'),
    #                      ('http://www.filedownloads.org/1rpnb9dudo7o/My_Backup_Pro_v3.2.5zz.zip.html', 200))

    # def test_adfocus(self):
    #     self.assertEqual(unshortenit.unshorten('http://adfoc.us/340347863622'), ('http://www7.zippyshare.com/', 404))

    # def test_lnxlu(self):
    #     self.assertEqual(unshortenit.unshorten('http://lnx.lu/1CKw'), ('http://www.reddit.com/', 200))

    def test_shst(self):
        # If you HEAD 'https://adf.ly/b2H0Y', it returns 'http://ay.gy/b2H0Y' for... some reason
        self.assertEqual(unshortenit.unshorten('http://sh.st/INTI'), ('http://ay.gy/b2H0Y', 200))

    def test_generic(self):
        self.assertEqual(unshortenit.unshorten('http://ul.to'), ('http://uploaded.net/', 200))
        self.assertEqual(unshortenit.unshorten('http://t.co/fsbtLWPUIJ'),
                         ('http://www.igen.fr/app-store/drift-mania-street-outlaws-du-drift-son-paroxysme-108452', 200))
        self.assertEqual(unshortenit.unshorten('http://p.ost.im/d7DPHP'),
                         ('http://crazymikesapps.com/drift-mania-street-outlaws-video-review/', 200))

    def test_google_unwrap(self):
        self.assertEqual(unshortenit.unshorten('https://www.google.com/url?url=https://en.wikipedia.org/wiki/Google&rct=j&q=&esrc=s&sa=U&ved=0ahUKEwijvuKNxdXKAhVT0GMKHQSDAp8QFgg3MAs&sig2=nsR8hgyoNqY87WcWVtt9Hw&usg=AFQjCNFUmLH6w9LpY157wHV4SowfxvZ4Ig'),
            ('https://en.wikipedia.org/wiki/Google', 200))