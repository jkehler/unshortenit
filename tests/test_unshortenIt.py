from unittest import TestCase
import unshortenit


class TestUnshortenIt(TestCase):

    def test_adfly(self):
        self.assertEqual(unshortenit.unshorten('http://adf.ly/WzXu2'),
                         ('http://www39.zippyshare.com/v/69303767/file.html', 200))
        self.assertEqual(unshortenit.unshorten('http://adf.ly/1icWR'),
                         ('http://adf.ly/1icWR', 'No ysmm variable found'))
        self.assertEqual(unshortenit.unshorten('http://links.devitrianto.com/yy', type='adfly'),
                         ('http://www.sendspace.com/file/a2z6ji', 200))
        self.assertEqual(unshortenit.unshorten('http://adf.ly/bJ8mm'),
                         ('http://www.mediafire.com/download/cixal2y0auya19m/com.ratrodstudio.skateparty2.zip', 200))


#     def test_linkbucks(self):
#         self.assertEqual(unshortenit.unshorten('http://4647ed8c.linkbucks.com/'),
#                          ('http://www.filedownloads.org/1rpnb9dudo7o/My_Backup_Pro_v3.2.5zz.zip.html', 200))
#
    def test_adfocus(self):
        result = unshortenit.unshorten('http://adfoc.us/340347863622')
        self.assertEqual(
            result,
            ('http://www7.zippyshare.com/v/24727439/file.html', 404)
        )

    # Unexistent domain
    # def test_lnxlu(self):
    #     self.assertEqual(unshortenit.unshorten('http://lnx.lu/1CKw'), ('http://www.reddit.com/', 200))

    def test_shst(self):
        self.assertEqual(unshortenit.unshorten('http://sh.st/INTI'), ('https://adf.ly/b2H0Y', 200))

    def test_generic(self):
        self.assertEqual(unshortenit.unshorten('http://ul.to'), ('http://uploaded.net/', 200))
        self.assertEqual(unshortenit.unshorten('http://t.co/fsbtLWPUIJ'),
                         ('http://www.igen.fr/app-store/drift-mania-street-outlaws-du-drift-son-paroxysme-108452', 200))

    def test_invalid(self):
        test_links = [
            'meloinvento',
            'htp:/kk',
            'wwww.kk.es',
            'httpp://www.kk.es'
        ]

        for link in test_links:
            obtained_result = unshortenit.unshorten(link)
            self.assertEqual(obtained_result, (link, unshortenit.INVALID_URL_ERROR_CODE))

    def test_hrefli(self):
        test_links = [
            ('https://href.li/?http://example.com/', ('http://example.com/', 200)),
            ('https://href.li/?http://stackoverflow.com/', ('http://stackoverflow.com/', 200)),
        ]

        for link, correct_result in test_links:
            obtained_result = unshortenit.unshorten(link)
            self.assertEqual(obtained_result, correct_result)

    def test_anonymz(self):
        test_links = [
            ('https://anonymz.com/?http://example.com/', ('http://example.com/', 200)),
            ('https://anonymz.com/?http://stackoverflow.com/', ('http://stackoverflow.com/', 200)),
        ]

        for link, correct_result in test_links:
            obtained_result = unshortenit.unshorten(link)
            self.assertEqual(obtained_result, correct_result)

