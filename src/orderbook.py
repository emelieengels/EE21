from datetime import datetime
import random
import optparse
import logging

def timestamp():
    return datetime.now()

#logging.basicConfig()

#log = logging.getLogger('EmsOrderbook')
#log.info('Starting orderbook')
#try:
    #emsmodule.DoIt()
#except Exception as e:
    #log.exception('There was a problem.')
#log.info('Ending app')

logging.basicConfig(filename="emelieslogs.log")
#logging.debug('This is a debug message')
logging.info('Program is starting')
#logging.warning('This is a warning message')
#logging.error('This is an error message')
#logging.critical('This is a critical message')

def createOrder():
    return Order(random.choice('BS'), random.randint(1, 10), random.randint(115, 130), timestamp())

class Order(object):
    def __init__(self, side, qty, price, timestamp):
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
            logging.error('This order exist already')
        self.Orders[order.Timestamp] = order

    def DelOrder(self, order):
        if order.Timestamp not in self.Orders:
            raise Exception('order does not exist with timestamp %s' % str(order.Timestamp))
            logging.error('This order does not exist')
        del self.Orders[order.Timestamp]

    def IsEmpty(self):
        if self.Orders == {}:
            print('this dictionary is empty:')
            return True
        else:
            print('this dictionary is empty:')
            return False

    def GetNumberOrder(self):
        print('number of oders in this pricelevel is: ', len(self.Orders.keys()))


class OrderbookSide(object):

    def __init__(self, side):
        self.Side = side
        self.Pricelevels = {}  #Price : PriceLevel

    def __str__(self):
        txt = '\nOrderbook Side ' + self.Side
        for pricelevel in self.Pricelevels.keys():
            txt += "\n"
            txt += str(self.Pricelevels[pricelevel])
        return txt

    def AddOrder(self, order): #ob preis auf oder absteigt liegt hier drin!
        if order.Price not in self.Pricelevels:
            priceLevel = Pricelevel(order.Price)
            self.Pricelevels[order.Price] = priceLevel
            temp = {}
            priceLevels = sorted(self.Pricelevels.keys(), reverse=True) #buyside high to low
            for pl in priceLevels:
                temp[pl] = self.Pricelevels[pl]
            self.Pricelevels = temp
            logging.info('Pricelevels have been added')
        else:
            priceLevel = self.Pricelevels[order.Price] #key von pricelevel dict is order.Price
        priceLevel.AddOrder(order)
        logging.info('Order has been added')

    def DelOrder(self, order):
        if order.Price in self.Pricelevels:
            priceLevel = self.Pricelevels[order.Price]
            del self.Pricelevels[order.Price] #key von price level: del[] keys der pricelevel zum rauslöschen, ein dictionary eintrag löschen- del[keyname der löschung]
            logging.info('Pricelevel has been deleted')
        else:
            raise Exception('Price level does not exist : %s' % str(order.Price))
            logging.error('This pl does not exist')
        priceLevel.DelOrder(order)
        logging.info('Order has been deleted')
        #print(priceLevel.IsEmpty())
        #print(priceLevel.GetNumberOrder())


class Orderbook(object):

    def __init__(self):
        self.BuySide = OrderbookSide('B')
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

if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options] marke zdr farbe") #example of how to use optparse
    parser.add_option("-o", "--ordercount", dest="ordercountnumber", default = 0, type = "int", help = "specify ordercount")
    options, args = parser.parse_args()
    print('options:', options)
    print('args:', args)
    print(options.ordercountnumber)

    orderbook = Orderbook()
    logging.info('Orderbook has been created')

    try:
        order1 = createOrder()
        #order2 = createOrder()
        order2 = Order('B', 2, 120, timestamp())
        order2a = Order('B', 3, 121, timestamp())
        order2b = Order('B', 4, 121, timestamp())
        order3 = createOrder()
        order4 = createOrder()
        order5 = createOrder()
        order6 = createOrder()
        orderbook.AddOrder(order1)
        orderbook.AddOrder(order2)
        orderbook.AddOrder(order2a)
        orderbook.AddOrder(order2b)
        orderbook.AddOrder(order3)
        orderbook.AddOrder(order4)
        orderbook.AddOrder(order5)
        orderbook.AddOrder(order6)
        orderbook.DelOrder(order2)
        print(orderbook)
    except Exception as info:
        raise

    logging.info('Program is ending')
