from datetime import datetime
import random
import optparse
import logging

logging.basicConfig(filename="logfilename.log")#, level=logging.DEBUG)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

def timestamp():
    return datetime.now()

def createOrder():
    return Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130) , timestamp())

class Order(object):
    def __init__(self, side, qty, price, timestamp):  # -> object:
        self.Side = side
        self.Qty = qty
        self.Price = price
        self.Timestamp = timestamp

    def __str__(self):
        return "%s: %s %s@%s" % (str(self.Timestamp), str(self.Side), str(self.Qty), str(self.Price))


class Pricelevel(object):
    def __init__(self, price):
        self.Price = price
        self.Orders = {}  # Timestamp : Order

    def __str__(self):
        txt = 'PriceLevel ' + str(self.Price)
        for timestamp in sorted(self.Orders.keys()):
            txt += "\n"
            txt += str(self.Orders[timestamp])
        return txt

    def AddOrder(self, order):
        if order.Timestamp in self.Orders:
            raise Exception("order exist already with timestamp %s" % str(order.Timestamp))
        self.Orders[order.Timestamp] = order
        # self.Orders = sorted(self.Orders)

    def DelOrder(self, order):
        if order.Timestamp not in self.Orders:
            raise Exception('order does not exist with timestamp %s' % str(order.Timestamp))
        del self.Orders[order.Timestamp]

    def DelPricelevel(self, order):
        if order.Timestamp not in self.Orders:
            raise Exception('Pricelevel does not exist with timestamp %s' % str(order.Timestamp))
        del self.Pricelevel[order.Timestamp]

    #def UpdateOrder(self, order):


class OrderbookSide(object):

    def __init__(self, side):
        self.Side = side
        self.Pricelevels = {}  # Price : PriceLevel

    def __str__(self):
        txt = '\nOrderbook Side ' + self.Side
        for pricelevel in self.Pricelevels.keys():
            txt += "\n"
            txt += str(self.Pricelevels[pricelevel])
        return txt

    def AddOrder(self, order):
        if order.Price not in self.Pricelevels:
            priceLevel = Pricelevel(order.Price)
            self.Pricelevels[order.Price] = priceLevel
            temp = {}
            priceLevels = sorted(self.Pricelevels.keys(), reverse=True)
            for pl in priceLevels:
                temp[pl] = self.Pricelevels[pl]
            self.Pricelevels = temp
            #sorted(self.Pricelevels, reverse=True)
        else:
            priceLevel = self.Pricelevels[order.Price]
        priceLevel.AddOrder(order)

    def DelOrder(self, order):
        if order.Price in self.Pricelevels:
            priceLevel = self.Pricelevels[order.Price]
            priceLevel.DelOrder(order)
        else:
            raise Exception('Price level does not exist : %s' % str(order.Price))
            #priceLevel = self.Pricelevels[order.Price]

    def DelPricelevel(self, order):
        if order.Price not in self.Pricelevels:
            priceLevel = self.Pricelevels[order.Price]
            priceLevel.DelPricelevel(order)
        else:
            pass

    #def UpdateOrder(self, order):


class Orderbook(object):

    def __init__(self):
        self.BuySide = OrderbookSide('B')
        #self.BuySide = sorted(self.BuySide.Pricelevels.keys(), reverse=True)
        self.SellSide = OrderbookSide('S')

    def __str__(self):
        txt = '\n\n>>>>>>>>>>Orderbook\n'
        txt += str(self.BuySide)
        txt += "\n"
        txt += str(self.SellSide)
        txt += '\n<<<<<<<<<<'
        return txt

    def AddOrder(self, order):
        if order.Side == 'B':
            #sorted(self.BuySide, reverse=True)
            self.BuySide.AddOrder(order)
        elif order.Side == 'S':
            self.SellSide.AddOrder(order)
        else:
            raise Exception("illegal Side: %s" % order.Side)

    def DelOrder(self, order):
        if order.Side == 'B':
            self.BuySide.DelOrder(order)
        elif order.Side == 'S':
            self.SellSide.DelOrder(order)
        else:
            raise Exception('illegal Side: %s' % order.Side)

    def DelPricelevel(self, order):
        if order.Side == 'B':
            self.BuySide.DelPricelevel(order)
        elif order.Side == 'S':
            self.SellSide.DelPricelevel(order)
        else:
            raise Exception('illegal Side: %s' % order.Side)

    def UpdateOrder(self, order):
        if order.Side == 'B':
            self.BuySide.UpdateOrder(order)
        elif order.Side == 'S':
            self.SellSide.UpdateOrder(order)
        else:
            raise Exception('illegal Side: %s' % order.Side)

    def PrintMe(self):
        for order in self.orders:
            print(order.__str__())  # transforms layout of outcome of orderbook in line and with spaces, ToString is defined in the python file order.py, which is still being used in this orderbook


if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options] marke zdr farbe") #example of how to use optparse
    parser.add_option("-o", "--ordercount", dest="ordercountnumber", default = 0, type = "int", help = "specify ordercount")
    options, args = parser.parse_args()
    #options.ordercountnumber = None
    print('options:', options)
    print('args:', args)
    #if len(args) != 3:
        #parser.error("incorrect number of arguments")
    print(options.ordercountnumber)

    orderbook = Orderbook()

    try:
        order1 = createOrder()
        order2 = createOrder()
        print(order2)
        order3 = createOrder()
        order4 = createOrder()
        order5 = createOrder()
        order6 = createOrder()
        orderbook.AddOrder(order1)
        orderbook.AddOrder(order2)
        orderbook.AddOrder(order3)
        orderbook.AddOrder(order4)
        orderbook.AddOrder(order5)
        orderbook.AddOrder(order6)
        orderbook.DelOrder(order2)
        #print(orderbook)

        #orderbook.DelOrder(order1)
        #print(orderbook)
    except Exception as info:
        raise
