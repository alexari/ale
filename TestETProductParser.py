import os
import unittest
import zipfile

from unittest import mock
from lxml import etree as ET
from product import ETProductParser

XMLTEST = """
<export_full>
    <items>
        <item name="Valid item">
            <parts>
                <part>
                    <item name="Valid part item" />
                </part>
            </parts>
        </item>
    </items>
</export_full>
"""

XMLTEST_URL = "file:///tmp/export_full.zip"
XMLTEST_ZIP = "/tmp/export_full.zip"
XMLTEST_FILENAME = "export_full.xml"
XMLTEST_XML = "/tmp/export_full.xml"

class TestETProductParser(unittest.TestCase):

    def setUp(self):
        with open(XMLTEST_XML, 'w') as f:
            f.write(XMLTEST)
        with zipfile.ZipFile(XMLTEST_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(XMLTEST_XML, arcname=XMLTEST_FILENAME)

    def tearDown(self):
        os.unlink(XMLTEST_XML)

    def testCount(self):
        model = ETProductParser(XMLTEST_URL, XMLTEST_FILENAME)
        model.load()
        self.assertEqual(model.count(), 1)

    def testProducts(self):
        model = ETProductParser(XMLTEST_URL, XMLTEST_FILENAME)
        model.load()
        self.assertEqual(model.products(), ['Valid item'])

    def testParts(self):
        model = ETProductParser(XMLTEST_URL, XMLTEST_FILENAME)
        model.load()
        self.assertEqual(model.parts(), [('Valid item', ['Valid part item'])])


if __name__ == "__main__":
    unittest.main()