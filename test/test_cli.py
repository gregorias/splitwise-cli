# -*- coding: utf-8 -*-
import unittest
from typing import Tuple

import click
import splitwise  # type: ignore

from splitwisecli import cli


def expense_user_to_tuple(user: splitwise.user.ExpenseUser) -> Tuple:
    return (user.getId(), user.getPaidShare(), user.getOwedShare())


class ExpenseUserParamTypeTestCase(unittest.TestCase):

    def test_parses_a_valid_string(self):
        expected = splitwise.user.ExpenseUser()
        expected.setId(1)
        expected.setPaidShare('10.0')
        expected.setOwedShare('5.0')

        self.assertEqual(
            expense_user_to_tuple(cli.ExpenseUser().convert(
                "1,10.0,5.0", None, None)), expense_user_to_tuple(expected))

    def test_fails_on_invalid(self):
        expected = splitwise.user.ExpenseUser()
        expected.setId(2)
        expected.setPaidShare('10.0')
        expected.setOwedShare('5.0')

        with self.assertRaises(click.exceptions.BadParameter):
            cli.ExpenseUser().convert("1,10.0", None, None)
