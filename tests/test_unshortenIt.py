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
        # self.assertEqual(unshortenit.unshorten_only('http://adf.ly/bJ8mm'),
        #                  ('http://www.mediafire.com/download/cixal2y0auya19m/com.ratrodstudio.skateparty2.zip', 200))

    def test_adfly_2(self):
        self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                         ('http://www39.zippyshare.com/v/69303767/file.html', 200))
        self.assertEqual(unshortenit.unshorten('http://adf.ly/1icWR'),
                         ('http://adf.ly/1icWR', 'No ysmm variable found'))
        self.assertEqual(unshortenit.unshorten('http://links.devitrianto.com/yy', type='adfly'),
                         ('https://www.sendspace.com/file/a2z6ji', 200))   # sendspace HEAD responses force HTTPS

    def test_shst(self):
        # If you HEAD 'https://adf.ly/b2H0Y', it returns 'http://ay.gy/b2H0Y' for... some reason
        # Also, a shortener url to another shortener? Really?
        self.assertEqual(unshortenit.unshorten('http://sh.st/INTI'), ('http://ay.gy/b2H0Y', 200))

    def test_generic(self):
        self.assertEqual(unshortenit.unshorten('http://ul.to'), ('http://uploaded.net/', 200))
        self.assertEqual(unshortenit.unshorten('http://t.co/fsbtLWPUIJ'),
                         ('http://www.igen.fr/app-store/drift-mania-street-outlaws-du-drift-son-paroxysme-108452', 200))

        # Link is now 404
        self.assertEqual(unshortenit.unshorten('http://p.ost.im/d7DPHP'),
                         ('http://p.ost.im/d7DPHP', 'list index out of range'))

    def test_google_unwrap(self):
        self.assertEqual(unshortenit.unshorten('https://www.google.com/url?url=https://en.wikipedia.org/wiki/Google&rct=j&q=&esrc=s&sa=U&ved=0ahUKEwijvuKNxdXKAhVT0GMKHQSDAp8QFgg3MAs&sig2=nsR8hgyoNqY87WcWVtt9Hw&usg=AFQjCNFUmLH6w9LpY157wHV4SowfxvZ4Ig'),
            ('https://en.wikipedia.org/wiki/Google', 200))

    ##################################################################
    ##################################################################
    ##################################################################

    # def test_linkbucks(self):
    #     self.assertEqual(unshortenit.unshorten('http://www.linkbucks.com/RA1R'),
    #                      ('https://nepustation.wordpress.com/cheat-majutsu-de-unmei-wo-nejifuseru/forth-episode-kunas-song/', 200))
    #     self.assertEqual(unshortenit.unshorten('http://www.linkbucks.com/lrC9'),
    #                      ('http://rebirthonlineworld.com/support-manager/support-chapter-1/', 200))

    ##################################################################
    ##################################################################
    ##################################################################

    def test_adfocus(self):
        result = unshortenit.unshorten('http://adfoc.us/340347863622')
        self.assertEqual(
            result,
            ('http://www7.zippyshare.com/v/24727439/file.html', 200)
        )

    def test_invalid(self):
        test_links = [
            'meloinvento',
            'htp:/kk',
            'wwww.kk.es',
            'httpp://www.kk.es'
        ]

        for link in test_links:
            uri, res = unshortenit.unshorten(link)
            self.assertEqual(uri, link)
            self.assertNotEqual(res, 200)

    def test_hrefli(self):
        test_links = [
            ('https://href.li/?http://example.com/', ('http://example.com/', 200)),
            ('https://href.li/?http://stackoverflow.com/', ('http://stackoverflow.com/', 301)),
        ]

        for link, correct_result in test_links:
            obtained_result = unshortenit.unshorten(link)
            self.assertEqual(obtained_result, correct_result)

    def test_anonymz(self):
        test_links = [
            ('https://anonymz.com/?http://example.com/', ('http://example.com/', 200)),
            ('https://anonymz.com/?http://stackoverflow.com/', ('http://stackoverflow.com/', 301)),
        ]

        for link, correct_result in test_links:
            obtained_result = unshortenit.unshorten(link)
            self.assertEqual(obtained_result, correct_result)

