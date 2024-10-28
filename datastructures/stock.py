from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Stock:
    symbol: str
    name: str
    low: int
    high: int
    def __repr__(self):
        return f'Symbol: {self.symbol}, Name: {self.name}, Low: {self.low}, High: {self.high}'