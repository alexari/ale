import unittest

from unittest import mock
from product import HTMLViewer

class TestHTMLViewer(unittest.TestCase):

    def testCount(self):
        model = mock.MagicMock()
        model.count.return_value = "32"
        self.assertEqual(HTMLViewer(model).count(), "<div>Počet produktů: 32</div>")

    def testProducts(self):
        model = mock.MagicMock()
        model.products.return_value = ["Valid produkt"]
        self.assertEqual(HTMLViewer(model).products(), "<ul><li>Valid produkt</li></ul>")

    def testParts(self):
        model = mock.MagicMock()
        model.parts.return_value = [['Valid product', ('Valid part 1', 'Valid part 2')]]
        self.assertEqual(HTMLViewer(model).parts(), "<h3>Valid product:</h3><ul><li>Valid part 1</li><li>Valid part 2</li></ul>")


if __name__ == "__main__":
    unittest.main()