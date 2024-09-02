import unittest


class InformativeTestCase(unittest.TestCase):
    def shortDescription(self):
        doc = self._testMethodDoc
        return (
            '\n'.join([row.strip() for row in doc.split('\n')])
            if doc
            else None
        )

    def assertTrue(self, expr, msg=None):
        if msg is None:
            msg = self.shortDescription()
        super().assertTrue(expr, msg=msg)

    def assertEqual(self, first, second, msg=None):
        if msg is None:
            msg = self.shortDescription()
        super().assertEqual(first, second, msg=msg)
