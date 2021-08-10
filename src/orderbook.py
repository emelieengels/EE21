from datetime import datetime
import random
import optparse
import logging

# option parser wird benutzt wenn orderbook.py von der terminal zeile aus aufgerufen wird, und bestimmte optionen hier in optparse definiert wurden
#program options
#add option eingeben, instrument name, action = store, dest, help
#adde logging für dieses file
#wenn ich zeit hab: pandas mit python benutzen
# hallo

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
    parser = optparse.OptionParser("usage: %prog [options] arg1") #example of how to use optparse
    parser.add_option("-o", "--ordercount", dest="ordercountnumber", default = None, type = "string", help = "specify ordercount")
    options, _ = parser.parse_args()
    print(len(_))
    #if len(args) != 1:
        #parser.error("incorrect number of arguments")
    #ordercountnumber = options.ordercountnumber


    orderbook = Orderbook()

    #order1 = Order('S', 10, 120, timestamp())
    #order2 = Order('B', 9, 121, timestamp())
    #order3 = Order('B', 8, 122, timestamp())
    #order4 = Order('S', 7, 123, timestamp())
    #order5 = Order('B', 6, 124, timestamp())
    #order6 = Order('S', 5, 125, timestamp())
    #order7 = Order('S', 4, 126, timestamp())
    #order8 = Order('S', 3, 120, timestamp())
    #order9 = Order('B', 2, 121, timestamp())
    #order10 = Order('S', 1, 120, timestamp())
    #order11 = Order('S', 1, 120, timestamp())

    #for i in range(5):
        #value1 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130) , timestamp())
        #print(value1)


    order1 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130) , timestamp())
    order2 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order3 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order4 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order5 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order6 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order7 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order8 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order9 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())
    order10 = Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())

    try:
        #orderbook.AddOrder(value)
        #print(orderbook)

        #orderbook.AddOrder(order9)
        #orderbook.AddOrder(order7)
        #orderbook.AddOrder(order1)
        #orderbook.AddOrder(order2)
        #orderbook.AddOrder(order3)
        #orderbook.AddOrder(order4)
        #orderbook.AddOrder(order5)
        order121 = createOrder()
        #orderbook.AddOrder(order6)
        #orderbook.AddOrder(order8)
        #orderbook.AddOrder(order10)
        orderbook.AddOrder(order121)
        print(orderbook)


        #orderbook.DelOrder(order8)
        #orderbook.DelOrder(order1)
        #orderbook.DelOrder(order10)
        #print(orderbook)
    except Exception as info:
        raise
