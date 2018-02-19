import unittest

from loop import Loop


GLOBAL_TEN = 10


class LoopTestCase(unittest.TestCase):

    def test_simple_loop(self):
        iters = []

        class For(Loop):
            x = 0; x < 10; ++x
            iters.append(x)

        self.assertEqual(iters, list(range(10)))

    def test_global_access(self):
        iters = []

        class For(Loop):
            x = 0; x < GLOBAL_TEN; ++x
            iters.append(x)

        self.assertEqual(iters, list(range(10)))

    def test_never_enter_loop(self):
        iters = []

        class For(Loop):
            x = 0; x > 100; ++x
            iters.append(x)

        self.assertEqual(iters, [])

    def test_continue(self):
        iters = []

        class For(Loop):
            x = 0; x < 5; ++x
            if x == 2:
                continue_()
            iters.append(x)

        self.assertEqual(iters, [0, 1, 3, 4])


if __name__ == '__main__':
    unittest.main()
