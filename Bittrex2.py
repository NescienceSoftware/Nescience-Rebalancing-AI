import time
import datetime
import bittrex
import math
import json
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Bittrex")


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

    with open('bittrex/config.json') as json_file:
        config = json.load(json_file)
        configcheck = config['configcheck']

    if configcheck != 'configured':
        assets = {}
        API_KEY = input('API KEY:')
        API_SECRET = input('API SECRET:')
        assetnum = input('Number of Assets in the Portfolio:')
        assetnum = int(assetnum)
        stablecoin = input('Would you like to trade against BTC or USDT? :')
        stablecoin = stablecoin.upper()
        for x in range(0, assetnum):
            x = str(x + 1)
            assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
            assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

        threshold = input("Algorithm Threshold= ")
        threshold = float(threshold)
        threshold = (.01 * threshold)
        if stablecoin == 'BTC':
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)
        if stablecoin == 'USDT':
            symbol = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                symbol["symbol_asset{0}".format(x)] = stablecoin + '-' + str(assets["asset{0}".format(x)])
        configcheck = 'configured'
        configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                         'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
        with open('bittrex/config.json', 'w') as outfile:
            json.dump(configuration, outfile)

    else:
        reconfig = input('Would you like to reconfigure?  ')
        if reconfig == 'yes':
            assets = {}
            API_KEY = input('API KEY:')
            API_SECRET = input('API SECRET:')
            assetnum = input('Number of Assets in the Portfolio:')
            assetnum = int(assetnum)
            stablecoin = input('Would you like to trade against BTC or USDT? :')
            stablecoin = stablecoin.upper()
            for x in range(0, assetnum):
                x = str(x + 1)
                assets["asset{0}".format(x)] = input('asset' + " " + x + ':')
                assets["asset{0}".format(x)] = assets["asset{0}".format(x)].upper()

            threshold = input("Algorithm Threshold= ")
            threshold = float(threshold)
            threshold = (.01 * threshold)
            if stablecoin == 'BTC':
                symbol = {}
                for x in range(0, assetnum):
                    x = str(x + 1)
                    symbol["symbol_asset{0}".format(x)] = str(assets["asset{0}".format(x)] + '-' + stablecoin)
            if stablecoin == 'USDT':
                symbol = {}
                for x in range(0, assetnum):
                    x = str(x + 1)
                    symbol["symbol_asset{0}".format(x)] = stablecoin + '-' + str(assets["asset{0}".format(x)])

            api_key = API_KEY.encode()
            api_secret = API_SECRET.encode()

            account = bittrex.AccountAPI(bittrex.API_V1_1, api_key, api_secret)

            old_cash = account.get_balance(stablecoin)[1]["Balance"]
            old_cash = 0 if old_cash is None else old_cash
            # Get Balances of each previously entered asset
            new_balance = {}
            for x in range(0, assetnum):
                x = str(x + 1)
                new_balance["balance_asset{0}".format(x)] = account.get_balance(assets[str('asset' + x)])[1]["Balance"]
                new_balance["balance_asset{0}".format(x)] = 0 if new_balance["balance_asset{0}".format(x)] is None else new_balance[
                    "balance_asset{0}".format(x)]

            old = {}

            for x in range(0, assetnum):
                x = str(x + 1)
                old['old_asset{0}'.format(x)] = new_balance['balance_asset{0}'.format(x)]

            olddata = {'old': old, 'old_cash': old_cash}

            with open('bittrex/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            configcheck = 'configured'

            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
            with open('bittrex/config.json', 'w') as outfile:
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
                symbol["symbol_asset{0}".format(x)] = str(config['symbol']["symbol_asset{0}".format(x)])

            configcheck = 'configured'
            configuration = {'assets': assets, 'threshold': threshold, 'configcheck': configcheck, 'assetnum': assetnum,
                             'stablecoin': stablecoin, 'symbol': symbol, 'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
            with open('bittrex/config.json', 'w') as outfile:
                json.dump(configuration, outfile)


def balances():
    # Pull  balance for each selected asset
    global cash_balance

    # Balance USD
    cash_balance = account.get_balance(stablecoin)[1]["Balance"]
    cash_balance = 0 if cash_balance is None else cash_balance
    # Get Balances of each previously entered asset
    balance = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        balance["balance_asset{0}".format(x)] = account.get_balance(assets[str('asset' + x)])[1]["Balance"]
        balance["balance_asset{0}".format(x)] = 0 if balance["balance_asset{0}".format(x)] is None else balance["balance_asset{0}".format(x)]
    # save balances to json
    balance.update({'cash_balance': cash_balance})
    with open('bittrex/balance.json', 'w') as outfile:
        json.dump(balance, outfile)


def prices():
    global price
    # Grabs prices from Bittrex
    price = {}
    for x in range(0, assetnum):
        x = str(x + 1)
        price["price_asset{0}".format(x)] = public.get_ticker(symbol["symbol_asset{0}".format(x)])[1]['Last']

    # saves to json
    with open('bittrex/prices.json', 'w') as outfile:
        json.dump(price, outfile)


def usd_value():
    # Calculates USD value of positions
    global usd
    global total_usd

    with open('bittrex/balance.json') as json_file:
        balance = json.load(json_file)

    with open('bittrex/prices.json') as json_file:
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


def sell_order(asset, sell_asset, current_price):

    value = current_price * sell_asset
    if value >= 10:
        currencies = public.get_markets()[1]
        for c in currencies:
            if c['MarketName'] == str(asset):
                minimum = float(c['MinTradeSize'])
        if minimum <= .001:
            sell_asset = truncate(sell_asset, 4)
            if minimum <= .01:
                sell_asset = truncate(sell_asset, 3)
            else:
                if minimum <= .1:
                    sell_asset = truncate(sell_asset, 2)
                else:
                    if minimum <= 1:
                        sell_asset = truncate(sell_asset, 1)
                    else:
                        if minimum == 1:
                            sell_asset = round(sell_asset)
        print("Selling" + " " + str(sell_asset) + " " + "of" + " " + str(asset))
        current_price = float(current_price * .5)
        sell_asset = float(sell_asset)
        market.sell_limit(asset, quantity=sell_asset, rate=current_price)


def buy_order(asset, buy_asset, current_price):

    buy_asset = truncate(buy_asset, 4)
    value = current_price * buy_asset
    if value >= 10:
        currencies = public.get_markets()[1]
        for c in currencies:
            if c['MarketName'] == str(asset):
                minimum = float(c['MinTradeSize'])
        if minimum <= .001:
            buy_asset = truncate(buy_asset, 4)
            if minimum <= .01:
                buy_asset = truncate(buy_asset, 3)
            else:
                if minimum <= .1:
                    buy_asset = truncate(buy_asset, 2)
                else:
                    if minimum <= 1:
                        buy_asset = truncate(buy_asset, 1)
                    else:
                        if minimum == 1:
                            buy_asset = round(buy_asset)
        print("Buying" + " " + str(buy_asset) + " " + "of" + " " + str(asset))
        current_price = float(current_price * 1.01)
        buy_asset = float(buy_asset * .98)
        market.buy_limit(asset, quantity=buy_asset, rate=current_price)

    # MAIN


setup()

with open('bittrex/config.json') as json_file:
    config = json.load(json_file)

api_key = config['API_KEY']
api_secret = config['API_SECRET']
api_key = api_key.encode()
api_secret = api_secret.encode()

account = bittrex.AccountAPI(bittrex.API_V1_1, api_key, api_secret)

market = bittrex.MarketAPI(bittrex.API_V1_1, api_key, api_secret)

public = bittrex.PublicAPI(bittrex.API_V1_1)

allocation = (.99 / assetnum)

with open('bittrex/initial.json') as json_file:
    initial = json.load(json_file)
    initialcheck = initial['initialcheck']
with open('bittrex/balance.json') as json_file:
    balance = json.load(json_file)
with open('bittrex/prices.json') as json_file:
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

    with open('bittrex/count.json', 'w') as outfile:
        json.dump(data2, outfile)

    with open('bittrex/initial.json', 'w') as outfile:
        json.dump(data, outfile)

else:
    with open('bittrex/count.json') as json_file:
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
            for y in range(0, assetnum):
                y = str(y + 1)
                usd_value()
                dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                sell["sell_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(price['price_asset{0}'.format(y)])
                sell["sell_asset{0}".format(y)] = float(sell["sell_asset{0}".format(y)])

            # Sell order API call
                if sell["sell_asset{0}".format(y)] > 0:
                    sell_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)], price["price_asset{0}".format(y)])

            for y in range(0, assetnum):
                y = str(y + 1)
                if sell["sell_asset{0}".format(y)] < 0:
                    sell["sell_asset{0}".format(y)] = (-1 * sell["sell_asset{0}".format(y)])
                    buy_order(symbol["symbol_asset{0}".format(y)], sell["sell_asset{0}".format(y)], price["price_asset{0}".format(y)])

    # Buy order trade trigger
    negative_threshold = (-1 * config['threshold'])
    for x in range(0, assetnum):
        x = str(x + 1)
        balances()
        usd_value()
        deviation()
        if dev["dev_asset{0}".format(x)] < negative_threshold:

            # Calculate # of shares to buy
            dif = {}
            buy = {}
            goal_allocation = total_usd * allocation
            for y in range(0, assetnum):
                y = str(y + 1)
                usd_value()
                dif["dif_asset{0}".format(y)] = usd["usd_asset{0}".format(y)] - goal_allocation
                buy["buy_asset{0}".format(y)] = float(dif["dif_asset{0}".format(y)]) / float(price['price_asset{0}'.format(y)])
                buy["buy_asset{0}".format(y)] = float(-1 * buy["buy_asset{0}".format(y)])

            # Buy order API call
                if buy["buy_asset{0}".format(y)] < 0:
                    buy["buy_asset{0}".format(y)] = (-1 * buy["buy_asset{0}".format(y)])
                    sell_order(symbol["symbol_asset{0}".format(y)], buy["buy_asset{0}".format(y)], price["price_asset{0}".format(y)])

            for y in range(0, assetnum):
                y = str(y + 1)
                if buy["buy_asset{0}".format(y)] > 0:
                    buy_order(symbol["symbol_asset{0}".format(y)], buy["buy_asset{0}".format(y)], price["price_asset{0}".format(y)])

    balances()
    prices()
    usd_value()

    # Record data every half day
    multiples = [n for n in range(1, 99999) if n % 5040 == 0]
    if count in multiples:
        # Checks for previous runs and calculates gain over initial allocation
        with open('bittrex/performance.json') as json_file:
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

            with open('bittrex/old.json', 'w') as outfile:
                json.dump(olddata, outfile)

            with open('bittrex/performance.json', 'w') as outfile:
                json.dump(data, outfile)
            # if not the initial setup, load previous iterations and calculate differences and profit
        else:
            with open('bittrex/performance.json') as json_file:
                performance = json.load(json_file)
            with open('bittrex/old.json') as json_file:
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

                with open('bittrex/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)

                with open('bittrex/performance.json', 'w') as outfile:
                    json.dump(data, outfile)

            else:
                data = {'compare': compare, 'profit': profit, 'initialcheck2': initialcheck2}

                olddata = {'old': old, 'old_cash': old_cash}

                with open('bittrex/old.json', 'w') as outfile:
                    json.dump(olddata, outfile)
                with open('bittrex/performance.json', 'w') as outfile:
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
                        price_asset = float(public.get_ticker(str(highest_asset))[1]['Last'])
                        asset_amount = float(donation_amount / price_asset)
                        print('Donating' + ' ' + donation_amount + 'of' + ' ' + str(
                            performance['profit']['overall']) + " " + "dollars" + " " + "profit")
                        sell_order(highest_asset, asset_amount, price_asset)

                        # Buy Eth
                        eth_symbol = str('ETH' + "-" + stablecoin)
                        price_eth = float(public.get_ticker(eth_symbol)[1]['Last'])
                        eth_amount = float((donation_amount / price_eth) * .95)
                        buy_order(eth_symbol, eth_amount, price_eth)

                        # Withdraw Eth
                        eth_withdraw = eth_amount * .95
                        print("Withdrawing" + " " + str(eth_withdraw) + "ETH" + " " + "as the donation to Nescience")
                        account.withdraw("ETH", eth_amount, "0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C")
                        # Set overall profit back to 0
                        overall_update = 0
                        profit.update({'overall': overall_update})
                        data.update({'profit': profit})
                        with open('bittrex/performance.json', 'w') as outfile:
                            json.dump(data, outfile)

    count = count + 1
    if count == 95760:
        count = 0
    data3 = {'count': count}
    with open('bittrex/count.json', 'w') as outfile:
        json.dump(data3, outfile)
    time.sleep(60)
