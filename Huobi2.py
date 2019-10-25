from time import sleep
from sys import exit
import time
import datetime
import math
import json
import ccxt
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Huobi")


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def setup():
    # Prompt user for asset selection
    global assets
    global threshold
    global configcheck
    global config
    global assetnum
    global stablecoin
    global symbol

    with open('huobi/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('What stablecoin or pair would you like to use:')
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        threshold = input("Algorithm Threshold= ")
        threshold = float(threshold)
        threshold = (.01 * threshold)
        symbol = {}
        for x in range(0, assetnum):
            x = str(x + 1)
            symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

        configcheck = 'configured'
        configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                         'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
        with open('huobi/config.json', 'w') as outfile:
            json.dump(configuration, outfile)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('What stablecoin or pair would you like to use:')
            stablecoin = stablecoin.upper()
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

            client = ccxt.huobipro({'apiKey': API_KEY, 'secret': API_SECRET})

            try:
                old_cash = client.fetch_balance()[stablecoin]['total']
            except ccxt.DDoSProtection as e:
                print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.RequestTimeout as e:
                print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.ExchangeNotAvailable as e:
                print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except ccxt.AuthenticationError as e:
                print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except AttributeError:
                old_cash = float(client.fetch_balance()[stablecoin]['total'])
            except KeyError:
                old_cash = 0.0
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                try:
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.DDoSProtection as e:
                    print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.RequestTimeout as e:
                    print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.ExchangeNotAvailable as e:
                    print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except ccxt.AuthenticationError as e:
                    print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except AttributeError:
                    new_balance['balance_asset{0}'.format(x)] = float(
                        client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
                except KeyError:
                    new_balance['balance_asset{0}'.format(x)] = 0.0

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]

            olddata = {'old': old, 'old_cash': old_cash}

            with open('huobi/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
            with open('huobi/config.json', 'w') as outfile:
                json.dump(configuration, outfile)

        else:
            assetnum = config['assetnum']
            assetnum = int(assetnum)
            assets = {}
            API_KEY = config['API_KEY']
            API_SECRET = config['API_SECRET']
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = config['assets']["asset{0}".format(x)]
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            threshold = config['threshold']
            stablecoin = config['stablecoin']
            stablecoin = stablecoin.upper()
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '/' + stablecoin)

            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
            with open('huobi/config.json', 'w') as outfile:
                json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance
    global e
    # Cash Balance
    try:
        cash_balance = client.fetch_balance()[stablecoin]['total']
    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        cash_balance = float(client.fetch_balance()[stablecoin]['total'])
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        cash_balance = float(client.fetch_balance()[stablecoin]['total'])
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        cash_balance = float(client.fetch_balance()[stablecoin]['total'])
    except ccxt.AuthenticationError as e:
        print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
        cash_balance = float(client.fetch_balance()[stablecoin]['total'])
    except AttributeError as e:
        cash_balance = float(client.fetch_balance()[stablecoin]['total'])
    except KeyError as e:
        cash_balance = 0.0
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        try:
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except ccxt.DDoSProtection as e:
            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except ccxt.RequestTimeout as e:
            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except ccxt.ExchangeNotAvailable as e:
            print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except ccxt.AuthenticationError as e:
            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except AttributeError as e:
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
        except KeyError as e:
            balance['balance_asset{0}'.format(x)] = 0.0
        except ConnectionError as e:
            balance['balance_asset{0}'.format(x)] = float(client.fetch_balance()[assets['asset{0}'.format(x)]]['total'])
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('huobi/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    global e
    # Grabs prices from Coinbase Pro
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        try:
            price["price_asset{0}".format(x)] = float(client.fetch_ticker(symbol["symbol_asset{0}".format(x)])['last'])
        except ccxt.base.errors.RequestTimeout as e:
            time.sleep(1)
            price["price_asset{0}".format(x)] = float(client.fetch_ticker(symbol["symbol_asset{0}".format(x)])['last'])
        except ccxt.ExchangeError as e:
            print(type(e).__name__, e.args, 'Exchange Error (missing API keys, ignoring)')
            time.sleep(1)
            price["price_asset{0}".format(x)] = float(client.fetch_ticker(symbol["symbol_asset{0}".format(x)])['last'])
        except ccxt.base.errors.NetworkError as e:
            time.sleep(1)
            price["price_asset{0}".format(x)] = float(client.fetch_ticker(symbol["symbol_asset{0}".format(x)])['last'])
    # saves to json
    with open('huobi/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('huobi/balance.json') as json_file:
        balance = json.load(json_file)

    with open('huobi/prices.json') as json_file:
        price = json.load(json_file)

    usd = {}

    for x in range(0, assetnum):
        x = str(x + 1)
        usd["usd_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)] * price["price_asset{0}".format(x)])

    usd_assets = 0
    for x in range(0, assetnum):
        x = str(x + 1)
        usd_assets = usd_assets + usd["usd_asset{0}".format(x)]

    total_usd = (usd_assets + cash_balance)


def deviation():
    # Calculates current % of portfolio and deviation from baseline
    global dev
    # % of portfolio, current%
    current = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        current["current_asset{0}".format(x)] = float(usd["usd_asset{0}".format(x)] / total_usd)
    # deviation from allocation, as a function of the allocation (allowing for infinite portfolio size scaling)
    dev = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        dev["dev_asset{0}".format(x)] = (current["current_asset"+x] - allocation)
        dev["dev_asset{0}".format(x)] = (dev["dev_asset{0}".format(x)] / allocation)
        dev["dev_asset{0}".format(x)] = float(dev["dev_asset{0}".format(x)])


def sell_order(pair, sell_asset, current_price):

    sell_asset = float(sell_asset)

    hmm = client.fetch_markets()
    for h in hmm:
        if h['symbol'] == pair:
            minimum = float(h['limits']['amount']['min'])

    if sell_asset >= minimum:
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + pair)
        client.create_order(symbol=pair, type='market', side='sell', amount=sell_asset, price=current_price)
        time.sleep(.1)


def buy_order(pair, buy_asset, current_price):

    buy_asset = float(buy_asset)

    hmm = client.fetch_markets()
    for h in hmm:
        if h['symbol'] == pair:
            minimum = float(h['limits']['amount']['min'])

    if buy_asset >= minimum:
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + pair)
        client.create_order(symbol=pair, type='market', side='buy', amount=buy_asset, price=current_price)
        time.sleep(.1)

    # MAIN


setup()

with open('huobi/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']

client = ccxt.huobipro({'apiKey': api_key, 'secret': api_secret})

allocation = (.99 / assetnum)

with open('huobi/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']
with open('huobi/balance.json') as json_file:
    balance = json.load(json_file)
with open('huobi/prices.json') as json_file:
    price = json.load(json_file)

if initialcheck != 'done':
    initial = {}
    balances()
    for x in range(0, assetnum):
        x = str(x + 1)
        initial["initial_balance_asset{0}".format(x)] = float(balance["balance_asset{0}".format(x)])
    initialcheck = 'done'
    count = 0
    data = {'initial': initial,
            'initialcheck': initialcheck}
    data2 = {'count': count}

    with open('huobi/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('huobi/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('huobi/count.json') as json_file:
        counts = json.load(json_file)
    count = int(counts['count'])

while count < 99999:

    balances()

    prices()

    usd_value()

    deviation()

    # print date and asset deviations

    print(datetime.datetime.now().time())

    for x in range(0, assetnum):
        x = str(x + 1)
        print(
            "Asset: " + assets["asset{0}".format(x)] + " :::: " + "Current Variation: " + str(
                dev["dev_asset{0}".format(x)] * 100) + "%")

    # Sell order trade trigger
    for x in range(0, assetnum):
        x = str(x + 1)
        balances()
        usd_value()
        deviation()
        if dev["dev_asset{0}".format(x)] > config['threshold']:
            # Calculate # of shares to sell
            dif = {}
            sell = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                usd_value()
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                sell["sell_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(price['price_asset{0}'.format(x)])
                sell["sell_asset{0}".format(x)] = float(sell["sell_asset{0}".format(x)])

            # Sell order API call
                if sell["sell_asset{0}".format(x)] > 0:
                        sell_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                   price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if sell["sell_asset{0}".format(x)] < 0:
                        sell["sell_asset{0}".format(x)] = (-1 * sell["sell_asset{0}".format(x)])
                        buy_order(config['symbol']["symbol_asset{0}".format(x)], sell["sell_asset{0}".format(x)],
                                   price['price_asset{0}'.format(x)])

    # Buy order trade trigger
    negative_threshold = (-1 * config['threshold'])
    for x in range(0, assetnum):
        x = str(x + 1)
        balances()
        usd_value()
        deviation()
        if dev["dev_asset{0}".format(x)] <= negative_threshold:

            # Calculate # of shares to buy
            dif = {}
            buy = {}
            goal_allocation = total_usd * allocation
            for x in range(0, assetnum):
                x = str(x + 1)
                usd_value()
                dif["dif_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - goal_allocation
                buy["buy_asset{0}".format(x)] = float(dif["dif_asset{0}".format(x)]) / float(price['price_asset{0}'.format(x)])
                buy["buy_asset{0}".format(x)] = float(-1 * buy["buy_asset{0}".format(x)])

            # Buy order API call
                if buy["buy_asset{0}".format(x)] < 0:
                        buy["buy_asset{0}".format(x)] = ( -1 * buy["buy_asset{0}".format(x)])
                        sell_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                                  price['price_asset{0}'.format(x)])
            for x in range(0, assetnum):
                x = str(x + 1)
                if buy["buy_asset{0}".format(x)] > 0:
                        buy_order(config['symbol']["symbol_asset{0}".format(x)], buy["buy_asset{0}".format(x)],
                                  price['price_asset{0}'.format(x)])

    balances()
    deviation()
    prices()
    usd_value()

    # Record data every half day
    multiples = [n for n in range(1, 99999) if n % 5040 == 0]
    if count in multiples:
        # Checks for previous runs and calculates gain over initial allocation
        with open('huobi/performance.json') as json_file:
            performance = json.load(json_file)
            initialcheck2 = performance['initialcheck2']

        if initialcheck2 != 'done':
            global old
            global compare
            global profit

            compare = {}
            old = {}
            profit = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                # calculate today's value of initial balances
                compare["compare_asset{0}".format(x)] = (
                            initial['initial']["initial_balance_asset{0}".format(x)] *
                            price["price_asset{0}".format(x)])

                # save current balances for future reference
                old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

                # calculate profit of current usd value vs initial balance usd value
                compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                profit["profit_asset{0}".format(x)] = usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)]
            old_cash = cash_balance

            # calculate profits of the small cash pool
            profit_cash = old_cash - cash_balance
            profit["current"] = 0

            # calculate current profits of the overall portfolio
            for x in range(0, assetnum):
                x = str(x + 1)
                profit["current"] = profit["current"] + profit["profit_asset{0}".format(x)]
            profit["current"] = profit["current"] + profit_cash

            # If portfolio > previous iteration, add to overall profit
            profit["overall"] = 0

            if profit["current"] >= 0:
                profit["overall"] = profit["current"] + profit["overall"]

            initialcheck2 = 'done'

            data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

            olddata = {'old': old, 'old_cash': old_cash}

            with open('huobi/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            with open('huobi/performance.json', 'w') as outfile:
                json.dump(data, outfile)
            # if not the initial setup, load previous iterations and calculate differences and profit
        else:
            with open('huobi/performance.json') as json_file:
                performance = json.load(json_file)
            with open('huobi/old.json') as json_file:
                oldload = json.load(json_file)
            compare = {}
            old = {}
            profit = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                # call old asset balance from Performance and set as new old asset dict
                old["old_asset{0}".format(x)] = oldload['old']["old_asset{0}".format(x)]

                # calculate today's value of previous balances
                compare["compare_asset{0}".format(x)] = (
                            old["old_asset{0}".format(x)] * price["price_asset{0}".format(x)])

                # calculate profit of current usd value vs previous iteration balance usd value
                compare["compare_asset{0}".format(x)] = float(compare["compare_asset{0}".format(x)])
                profit["profit_asset{0}".format(x)] = (usd["usd_asset{0}".format(x)] - compare["compare_asset{0}".format(x)])

            old_cash = float(oldload['old_cash'])

            # calculate profit over previous cash pool
            profit_cash = cash_balance - old_cash

            # overwrite previous iteration balances save current balances for future reference
            for x in range(0, assetnum):
                x = str(x + 1)
                old["old_asset{0}".format(x)] = balance["balance_asset{0}".format(x)]

            # calculate current profits of the overall portfolio
            profit['current'] = 0
            for x in range(0, assetnum):
                x = str(x + 1)
                profit['current'] = profit['current'] + profit["profit_asset{0}".format(x)]
            profit['current'] = profit['current'] + profit_cash
            old_cash = cash_balance

            # If portfolio > previous iteration, add to overall profit
            profit['overall'] = performance['profit']['overall']
            initialcheck2 = 'done'
            if profit['current'] >= 0:
                profit['overall'] = profit['current'] + profit['overall']

                data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                olddata = {'old': old, 'old_cash': old_cash}

                with open('huobi/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('huobi/performance.json', 'w') as outfile:
                    json.dump(data, outfile)

            else:
                data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                olddata = {'old': old, 'old_cash': old_cash}

                with open('huobi/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)
                with open('huobi/performance.json', 'w') as outfile:
                    json.dump(data, outfile)

            # If profit due to the algorithm exceeds $100, donate X% to Nescience
            if performance['profit']['overall'] > 200:
                # Sort Deviation for highest asset deviation and sell donation amount before buying equivalent ETH

                hmm = list(sum(sorted(dev.items(), key=lambda x: x[1], reverse=True), ()))[0]

                for a in assets:
                    if a == str(hmm):
                        print('Initiating Donation.')
                        donation_amount = (performance['profit']['overall'] * .10)

                        # Sell Highest Deviation
                        highest_asset = str(assets[str(hmm)] + stablecoin)

                        try:
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                            time.sleep(2)
                        except ccxt.DDoSProtection as e:
                            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                            time.sleep(2)
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                        except ccxt.RequestTimeout as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                        except ccxt.ExchangeNotAvailable as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args,
                                  'Exchange Not Available due to downtime or maintenance (ignoring)')
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                        except ccxt.AuthenticationError as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])
                        except AttributeError as e:
                            time.sleep(1)
                            price_asset = float(client.fetch_ticker(str(highest_asset))['last'])

                        time.sleep(1)

                        asset_amount = float(donation_amount / price_asset)
                        print('Donating' + ' ' + donation_amount + 'of' + ' ' + str(
                            performance['profit']['overall']) + " " + "dollars" + " " + "profit")
                        sell_order(highest_asset, asset_amount, price_asset)

                        # Buy Eth
                        eth_symbol = str('ETH' + "-" + stablecoin)

                        try:
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                            time.sleep(2)
                        except ccxt.DDoSProtection as e:
                            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
                            time.sleep(2)
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                        except ccxt.RequestTimeout as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                        except ccxt.ExchangeNotAvailable as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args,
                                  'Exchange Not Available due to downtime or maintenance (ignoring)')
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                        except ccxt.AuthenticationError as e:
                            time.sleep(1)
                            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                        except AttributeError as e:
                            time.sleep(1)
                            price_eth = float(client.fetch_ticker(str(eth_symbol))['last'])
                        time.sleep(1)

                        eth_amount = float((donation_amount / price_eth) * .95)
                        buy_order(eth_symbol, eth_amount, price_eth)

                        # Withdraw Eth
                        eth_withdraw = eth_amount * .95
                        print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as the donation to Nescience")
                        client.withdraw("ETH", eth_amount, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")

    count = count + 1
    if count == 95760:
        count = 0
    data3 = {'count': count}
    with open('huobi/count.json', 'w') as outfile:
        json.dump(data3, outfile)
    time.sleep(60)
