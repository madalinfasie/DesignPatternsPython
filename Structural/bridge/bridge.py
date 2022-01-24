"""
You want to create a new banking application to "disrupt" the market.
The application can manage multiple accounts at the same time for each client
and offers the same basic functionalities that a client would expect from
a banking application.
"""
import abc
import enum


class InsufficientFundsError(Exception):
    pass


class TooManyFundsError(Exception):
    pass


class AccountClosedError(Exception):
    pass


class TooMuchDebtError(Exception):
    pass


class AccountState(enum.Enum):
    OPENED = enum.auto()
    CLOSED = enum.auto()


class Account(abc.ABC):
    @abc.abstractmethod
    def balance(self) -> float:
        pass

    @abc.abstractmethod
    def transfer(self, account: 'Account', amount: float) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass

    @abc.abstractmethod
    def borrow(self, amount: float) -> None:
        pass

    @abc.abstractmethod
    def display(self) -> str:
        pass


class PersonalAccount(Account):
    def __init__(self, initial_funds: int = 0):
        self.iban = 'RO23XYZ123456789'
        self.funds = initial_funds
        self.debt = 0
        self.state = AccountState.OPENED
        self._credit_interest = 0.069

    def balance(self) -> float:
        return self.funds

    def transfer(self, account: Account, amount: float) -> None:
        if self.funds < amount:
            raise InsufficientFundsError('Not enough funds in the account')

        if self.state == AccountState.CLOSED:
            raise AccountClosedError('The account is not opened')

        source_funds = self.funds
        destination_funds = account.funds

        try:
            self.funds -= amount
            account.funds += amount
        except Exception as e:
            print(f'Transaction failed with error {e}. Rollback...')
            self.funds = source_funds
            account.funds = destination_funds

    def close(self):
        if self.funds:
            raise TooManyFundsError('The account has to be empty in order to close it.')

        if self.debt:
            raise TooMuchDebtError('The debt must be paid before closing the account')

        self.state = AccountState.CLOSED

    def borrow(self, amount: float) -> None:
        if self.state == AccountState.CLOSED:
            raise AccountClosedError('The account is not opened')

        self.debt += amount + amount * self._credit_interest
        self.funds += amount

    def display(self) -> str:
        return 'Acc. Type: {type}\nAcc. State: {state}\nBalance: {balance:.2f}\nDebt: {debt:.2f}'.format(
            type=self.__class__.__name__,
            state=self.state.name,
            balance=self.balance(),
            debt=self.debt
        )


class DepositAccount(Account):
    def __init__(self) -> None:
        self.iban = 'RO31ABCD987654321'
        self.funds = 0
        self.interest = 0.003
        self.state = AccountState.OPENED

    def balance(self) -> float:
        return self.funds + self.funds * self.interest

    def transfer(self, account: 'Account', amount: float) -> None:
        if self.funds < amount:
            raise InsufficientFundsError('Not enough funds in the account')

        if self.state == AccountState.CLOSED:
            raise AccountClosedError('The account is not opened')

        source_funds = self.funds
        destination_funds = account.funds

        try:
            self.funds -= amount
            account.funds += amount
        except Exception as e:
            print(f'Transaction failed with error {e}. Rollback...')
            self.funds = source_funds
            account.funds = destination_funds

    def close(self):
        if self.funds:
            raise TooManyFundsError('The account has to be empty in order to close it.')

        self.state = AccountState.CLOSED

    def display(self) -> str:
        return 'Acc. Type: {type}\nAcc. State: {state}\nBalance: {balance:.2f}\nInterest rate: {interest:.3f}'.format(
            type=self.__class__.__name__,
            state=self.state.name,
            balance=self.balance(),
            interest=self.interest
        )


class BankingApplication:
    def __init__(self):
        self.accounts = []
        self.current_account = None

    def add_account(self, account) -> None:
        self.accounts.append(account)

    def set_current_account(self, account: Account) -> None:
        if account in self.accounts:
            self.current_account = account

    def list_accounts(self) -> None:
        for account in self.accounts:
            print(account.display())
            print('-' * 50)

    def make_transfer(self, destination_account: Account, amount: float) -> None:
        self.current_account.transfer(destination_account, amount)

    def make_credit(self, amount: float) -> None:
        if isinstance(self.current_account, PersonalAccount):
            self.current_account.borrow(amount)

    def close(self) -> None:
        self.current_account.close()


if __name__ == '__main__':
    personal_account = PersonalAccount(initial_funds=2000)
    economies = DepositAccount()

    app = BankingApplication()

    app.add_account(personal_account)
    app.add_account(economies)
    app.set_current_account(personal_account)

    app.make_credit(5000)
    app.make_transfer(economies, 1000)

    app.list_accounts()

    app.close()



