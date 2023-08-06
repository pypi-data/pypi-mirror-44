##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTLAR PURPOSE.
#
##############################################################################
"""Testing all XML Locale functionality.
"""
import logging
import os
import subprocess
import unittest
import sys
import z3c.rml.tests
from z3c.rml import rml2pdf

try:
    import Image
except ImportError:
    from PIL import Image

LOG_FILE = os.path.join(os.path.dirname(__file__), 'render.log')


def gs_command(path):
    return ('gs', '-q', '-sNOPAUSE', '-sDEVICE=png256',
            '-sOutputFile=%s[Page-%%d].png' % path[:-4],
            path, '-c', 'quit')


class RMLRenderingTestCase(unittest.TestCase):

    def __init__(self, inPath, outPath):
        self._inPath = inPath
        self._outPath = outPath
        unittest.TestCase.__init__(self)

    def setUp(self):
        import z3c.rml.tests.module
        sys.modules['module'] = z3c.rml.tests.module
        sys.modules['mymodule'] = z3c.rml.tests.module

    def tearDown(self):
        del sys.modules['module']
        del sys.modules['mymodule']

        from z3c.rml.document import LOGGER_NAME
        for handler in logging.getLogger(LOGGER_NAME).handlers:
            if handler.baseFilename == LOG_FILE:
                handler.close()

        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    def runTest(self):
        rml2pdf.go(self._inPath, self._outPath)


class ComparePDFTestCase(unittest.TestCase):

    level = 2

    def __init__(self, basePath, testPath):
        self._basePath = basePath
        self._testPath = testPath
        unittest.TestCase.__init__(self)

    def assertSameImage(self, baseImage, testImage):
        base_file = open(baseImage, 'rb')
        test_file = open(testImage, 'rb')
        base_image = Image.open(base_file)
        base = base_image.getdata()
        test_image = Image.open(test_file)
        test = test_image.getdata()
        err_count = 0

        for i in range(len(base)):
            if (base[i] - test[i]) != 0:
                err_count += 1

                if False:
                    from base64 import b64encode
                    import PIL
                    differ = PIL.ImageChops.subtract(base_image, test_image)
                    # differ.show()
                    # output the result as base64 for travis debugging
                    print(b64encode(differ.tobytes()))
                    # flip the above condition to activate this code
                    print()
                    print(os.system("gs --version"))

                    base_file.seek(0)
                    print(baseImage)
                    print(b64encode(base_file.read()))
                    print(self._basePath)
                    with open(self._basePath, 'rb') as base_pdf:
                        print(b64encode(base_pdf.read()))

                    test_file.seek(0)
                    print(testImage)
                    print(b64encode(test_file.read()))
                    print(self._testPath)
                    with open(self._testPath, 'rb') as test_pdf:
                        print(b64encode(test_pdf.read()))

                self.fail(
                    'Image is not the same: %s' % os.path.basename(baseImage))
        base_file.close()
        test_file.close()

    def runTest(self):
        # Convert the base PDF to image(s)
        status = subprocess.Popen(gs_command(self._basePath)).wait()
        if status:
            return
        # Convert the test PDF to image(s)
        status = subprocess.Popen(gs_command(self._testPath)).wait()
        if status:
            return
        # Go through all pages and ensure their equality
        n = 1
        while True:
            baseImage = self._basePath[:-4] + '[Page-%i].png' %n
            testImage = self._testPath[:-4] + '[Page-%i].png' %n
            if os.path.exists(baseImage) and os.path.exists(testImage):
                self.assertSameImage(baseImage, testImage)
            else:
                break
            n += 1


class CompareFileTestCase(unittest.TestCase):

    def __init__(self, testPath, contains):
        self._testPath = testPath
        self._contains = contains
        unittest.TestCase.__init__(self)

    def runTest(self):
        f = open(self._testPath, 'rb')
        try:
            contents = f.read()

            if self._contains not in contents:
                self.fail(
                    'PDF file does not contain: %s' % self._contains
                )
        finally:
            f.close()


def test_suite():
    if False:
        # Debug info
        import pkg_resources
        print("Environment\n===========")
        print("reportlab:")
        print(pkg_resources.get_distribution('reportlab').version)
        print("ghostscript:")
        os.system("gs --version")

    suite = unittest.TestSuite()
    here = os.path.dirname(z3c.rml.tests.__file__)
    inputDir = os.path.join(here, 'input')
    outputDir = os.path.join(here, 'output')
    expectDir = os.path.join(here, 'expected')
    for filename in os.listdir(inputDir):
        if not filename.endswith(".rml"):
            continue

        inPath = os.path.join(inputDir, filename)
        outPath = os.path.join(outputDir, filename[:-4] + '.pdf')
        expectPath = os.path.join(expectDir, filename[:-4] + '.pdf')

        # ** Test RML to PDF rendering **
        # Create new type, so that we can get test matching
        TestCase = type(filename[:-4], (RMLRenderingTestCase,), {})
        case = TestCase(inPath, outPath)
        suite.addTest(case)
        # ** Test PDF rendering correctness **
        TestCase = type('compare-'+filename[:-4], (ComparePDFTestCase,), {})
        case = TestCase(expectPath, outPath)
        suite.addTest(case)

        if filename == 'printScaling.rml':
            TestCase = type('compare-file-'+filename[:-4],
                            (CompareFileTestCase,), {})
            case = TestCase(outPath, b'/PrintScaling /None')
            suite.addTest(case)

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
