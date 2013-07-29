from unittest import TestCase

import docutils.frontend
import docutils.parsers.rst
import docutils.utils

from hieroglyph.tests.util import with_sphinx
from hieroglyph.tests import util

from hieroglyph import directives


class SlideConfTests(TestCase):

    def _make_document(self, source, contents):

        parser = docutils.parsers.rst.Parser()
        document = docutils.utils.new_document(
            source,
            docutils.frontend.OptionParser(
                components=(docutils.parsers.rst.Parser,)
            ).get_default_values(),
        )

        parser.parse(contents, document)

        return document

    @with_sphinx()
    def test_filter_doctree(self, sphinx_app):
        """Only slide related elements will be retained when filtering."""

        test_content = """

.. slideconf::
   :autoslides: False

Heading
=======

.. slide:: Heading

   Blarf

Second Level
------------

* Point 1
* Point 2

"""

        document = self._make_document(
            'slideconf_test',
            test_content,
        )

        directives.filter_doctree_for_slides(document)

        # only two elements remain -- the slideconf and slide element
        self.assertEqual(len(document.children), 2)

    @with_sphinx(
        buildername='slides',
        srcdir=util.test_root.parent/'no-autoslides',
    )
    def test_trailing_content_removed(self, sphinx_app):

        sphinx_app.build()

        self.assertFalse(
            'TESTING_SENTINEL' in
            file(sphinx_app.builddir/'slides'/'index.html').read(),
            'The sentinel paragraph should have been filtered.',
        )