from ftw.builder import Builder
from ftw.builder import create
from ftw.iframeblock.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu


class TestIFrameBlockContentType(FunctionalTestCase):

    params_list = [
        ('width', '100%'),
        ('class', 'iframeblock loading'),
        ('onload', 'onIframeLoaded(this)'),
        ('src', 'http://www.google.com'),
        ('height', '400'),
        ('scrolling', 'auto'),
        ('data-height-calculation-method', 'bodyOffset'),
    ]

    def setUp(self):
        super(TestIFrameBlockContentType, self).setUp()
        self.grant('Manager')

    @browsing
    def test_block_can_be_added_with_factories_menu(self, browser):
        content_page = create(Builder('sl content page').titled(u'A page'))
        browser.login().visit(content_page)
        factoriesmenu.add('iFrame block')
        browser.fill({
            'URL': u'http://www.google.com',
            'Height': u'400',
        })
        browser.find_button_by_label('Save').click()
        browser.visit(content_page)

        expected = sorted([params[1] for params in self.params_list])
        results = sorted([
            browser.css('iframe').first.attrib[params[0]]
            for params in self.params_list
        ])

        self.assertListEqual(expected, results)
