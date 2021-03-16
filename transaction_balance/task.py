from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


class CompoundTransactionAction(Enum):
    Deposit = 'deposit'
    Withdrawal = 'withdrawal'
    Transfer = 'transfer'


@dataclass
class CompoundTransaction:
    datetime: datetime
    action: CompoundTransactionAction
    eth_value: Optional[float]
    erc20_value: float


@dataclass
class Price:
    datetime: datetime
    price: float


time_now = datetime.utcnow()
time1 = time_now - timedelta(days=30)
time2 = time_now - timedelta(days=10)
time3 = time_now - timedelta(days=1)

eth_to_token: Dict[datetime, Price] = {
    time1: Price(time1, 100),
    time2: Price(time2, 80),
    time3: Price(time3, 60),
    time_now: Price(time_now, 50),
}

# Deposit 1 ETH => receive 100 tokens
deposit = CompoundTransaction(time1, CompoundTransactionAction.Deposit, 1, 100)

# Return 40 tokens => receive 0.5 ETH back
withdrawal = CompoundTransaction(time2, CompoundTransactionAction.Withdrawal, 0.5, 40)

transfer = CompoundTransaction(time3, CompoundTransactionAction.Transfer, None, 50)


def count(transactions: List[CompoundTransaction], today_course: Price) -> float:
    eth = 0
    tokens = 0
    for t in transactions:
        if t.action == CompoundTransactionAction.Deposit:
            eth -= t.eth_value
            tokens += t.erc20_value
        elif t.action == CompoundTransactionAction.Withdrawal:
            eth += t.eth_value
            tokens -= t.erc20_value
        elif t.action == CompoundTransactionAction.Transfer:
            tokens += t.erc20_value
            if t.erc20_value < 0:
                eth -= t.erc20_value / eth_to_token[t.datetime].price

    eth += tokens / today_course.price
    return eth


print(count([deposit, withdrawal, transfer], eth_to_token[time_now]))
