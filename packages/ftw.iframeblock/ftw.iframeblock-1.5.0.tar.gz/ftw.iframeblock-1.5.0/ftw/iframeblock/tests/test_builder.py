from ftw.builder import Builder
from ftw.builder import create
from ftw.iframeblock.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testing import IS_PLONE_5


class TestIFrameBlockBuilder(FunctionalTestCase):

    def setUp(self):
        super(TestIFrameBlockBuilder, self).setUp()
        self.grant('Manager')

    @browsing
    def test_add_iframeblock(self, browser):
        block_title = u'My iFrame block'
        content_page = create(Builder('sl content page'))
        create(Builder('iframe block')
               .titled(block_title)
               .within(content_page))

        browser.login().visit(content_page)

        self.assertTrue(len(browser.css('.sl-block')), 'Expect one block')
