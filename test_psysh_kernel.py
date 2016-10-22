"""Example use of jupyter_kernel_test, with tests for IPython."""

import unittest
import jupyter_kernel_test as jkt


class PsyshKernelTests(jkt.KernelTests):
    kernel_name = "psysh"

    language_name = "php"

    code_hello_world = "echo('hello, world');"

    completion_samples = [
        {
            'text': 'is_d',
            'matches': {'is_dir', 'is_double'},
        },
    ]

    code_page_something = "is_dir(__DIR__);"

if __name__ == '__main__':
    unittest.main()
