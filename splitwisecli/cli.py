# -*- coding: utf-8 -*-
import sys

import click
import click_spinner  # type: ignore
import splitwise  # type: ignore

__all__ = ['ExpenseUser']


class ExpenseUser(click.ParamType):
    name = "ExpenseUser"

    def convert(self, value, param, ctx):
        if isinstance(value, splitwise.user.ExpenseUser):
            return value

        try:
            maybe_id, paid_share, owed_share = value.split(",")
            user = splitwise.user.ExpenseUser()
            user.setId(int(maybe_id))
            user.setPaidShare(paid_share)
            user.setOwedShare(owed_share)
            return user

        except ValueError:
            fail_msg = ("{} is not in the valid format " +
                        "ID,PAID_SHARE,OWED_SHARE.").format(value)
            self.fail(fail_msg, param, ctx)


@click.command()
@click.option('--api_key', required=True, help="The personal API key.")
@click.option('--cost',
              required=True,
              help="A string representation of a decimal value, " +
              "limited to 2 decimal places")
@click.option('--description', required=True)
@click.option('--currency_code', required=True, help="A currency code")
@click.argument('users',
                required=True,
                type=ExpenseUser(),
                nargs=-1,
                metavar='USERS')
def create_expense(api_key, cost, description, currency_code, users):
    with click_spinner.Spinner():
        s = splitwise.Splitwise(None, None, api_key=api_key)
        expense = splitwise.Expense()
        expense.cost = cost
        expense.setDescription(description)
        expense.currency_code = currency_code
        expense.group_id = 0
        for user in users:
            expense.addUser(user)
        expense, errors = s.createExpense(expense)
    if errors:
        raise click.ClickException(str(errors.getErrors()))


def main():
    """The console script for splitwise-cli."""
    create_expense()
    return


if __name__ == "__main__":
    sys.exit(main())
