from datastructures.intervaltree import IntervalTree
from datastructures.stock import Stock
import csv

if __name__ == "__main__":
    # tree = IntervalTree()
    # tree.insert(100, 150, Stock('AAPL', 'Apple Inc.', 100, 150))
    # tree.insert(200, 250, Stock('GOOG', 'Alphabet Inc.', 200, 250))
    # tree.insert(150, 175, Stock('MSFT', 'Microsoft Corp.', 150, 175))
    # tree.insert(100, 160, Stock('TSLA', 'Tesla Inc.', 100, 160))

    # print('Point:')
    # print(tree.search(120, fancy=True))
    # print('\nRange:')
    # print(tree.search(120, 160, True))
    # print('\nTop 2:')
    # print(tree.top_k(2, True))
    # print('\nTop 3:')
    # print(tree.top_k(3, True))
    # print('\nBottom 2:')
    # print(tree.bottom_k(2, True))
    # print('\nBottom 3:')
    # print(tree.bottom_k(3, True))

    tree = IntervalTree()
    #with open('HW5\sample_stock_prices.csv') as csvfile:
    with open('HW5\synthetic_stock_data.csv') as csvfile:
        stocks = csv.reader(csvfile)
        for stock in stocks:
            stock = stock[:-1] # remove dates
            new_stock = Stock(*stock)
            low = stock[2]
            high = stock[3]
            new_node = tree.insert(int(low), int(high), new_stock)
    print(len(tree.search(155)))
    print(len(tree.search(155, 200)))
    print(tree.bottom_k(10, fancy=True))
    print(tree.top_k(10, fancy=True))