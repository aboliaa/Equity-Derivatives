import os

from const import *
import matplotlib.pyplot as plt

class Graph(object):
    def __init__(self, path):
        self.path = path

    def plot_report1(self, data):

        call_strike_prices = {}
        call_open_interests = {}
        put_strike_prices = {}
        put_open_interests = {}
        
        for d in data:
            if d['opt_type'] == CE:
                if d['exp_dt'] not in call_strike_prices:
                    call_strike_prices[d['exp_dt']] = []
                if d['exp_dt'] not in call_open_interests:
                    call_open_interests[d['exp_dt']] = []
                call_strike_prices[d['exp_dt']].append(d['strike_pr'])
                call_open_interests[d['exp_dt']].append(d['open_int'])
            elif d['opt_type'] == PE:
                if d['exp_dt'] not in put_strike_prices:
                    put_strike_prices[d['exp_dt']] = []
                if d['exp_dt'] not in put_open_interests:
                    put_open_interests[d['exp_dt']] = []
                put_strike_prices[d['exp_dt']].append(d['strike_pr'])
                put_open_interests[d['exp_dt']].append(d['open_int'])
            
        expiry_series = call_strike_prices.keys()
        expiry_series.sort()

        # Ignore expiry series after 3
        expiry_series = expiry_series[:3]

        i = 1
        for e in expiry_series:
            plt.clf()
            strike_pr = call_strike_prices[e]
            open_int = call_open_interests[e]
            
            # TODO: Move this into seperate function
            x = strike_pr
            bins = int((x[-1] - x[0])/(x[1] - x[0]))
            plt.hist(strike_pr, bins=bins, weights=open_int, facecolor='green', 
                    label='CALLs', alpha=0.5)

            strike_pr = put_strike_prices[e]
            open_int = put_open_interests[e]

            x = strike_pr
            bins = int((x[-1] - x[0])/(x[1] - x[0]))
            plt.hist(strike_pr, bins=bins, weights=open_int, facecolor='blue', 
                    label='PUTs', alpha=0.5)
        
            plt.xlabel('Strike price')
            plt.ylabel('Open Interest')
            plt.title('Distribution of PUTs and CALLs')
            plt.legend(loc='upper right')

            # Tweak spacing to prevent clipping of ylabel
            #plt.tight_layout()
            #plt.subplots_adjust(left=0.15)
            plt.savefig(os.path.join(self.path, "report1_%s.png" %str(i)))
            i += 1

    def plot_report2(self, data):
        dates = []
        settlement_prices = []
        sum_of_OI = []

        for d in sorted(data.iteritems()):
            dates.append(d[0])
            settlement_prices.append(d[1]['settlement_price'])
            sum_of_OI.append(d[1]['summation_of_OI'])

        plt.clf()

        fig, x1 = plt.subplots()
        sp = x1.plot(settlement_prices, label='Settlement price')
        x1.set_ylabel('Settlement Price')
        plt.setp(sp, color='r', linewidth=1.0, marker='o', label='Settlement price')

        x2 = x1.twinx()
        oi = x2.bar(range(len(dates)), sum_of_OI, width=0.4, align='center', 
                    alpha=0.5, label='Summation of OI')
        x2.set_ylabel('Summation of OI')
        plt.setp(oi, color='b', linewidth=1.0)

        plt.xticks(range(len(dates)), dates, rotation='vertical')
        plt.xlabel('Date')
        plt.title('Settlement price v/s Open interest')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, "report2.png"))

    def plot_report3(self, data):
        dates = []
        settlement_prices = []
        PCR_OI = []
        PCR_trade = []

        for d in sorted(data.iteritems()):
            dates.append(d[0])
            settlement_prices.append(d[1]['settlement_price'])
            PCR_OI.append(d[1]['PCR_OI'])
            PCR_trade.append(d[1]['PCR_trade'])

        plt.clf()

        fig, x1 = plt.subplots()
        oi = x1.plot(PCR_OI, label='PCR of OI')
        x1.set_ylabel('PCR of OI')
        plt.setp(oi, color='r', linewidth=1.0)


        # sp = x1.plot(settlement_prices, label='Settlement price')
        # x1.set_ylabel('Settlement Price')
        # plt.setp(sp, color='r', linewidth=1.0, marker='o', label='Settlement price')

        x2 = x1.twinx()
        trade = x2.plot(PCR_trade, label='PCR of trade')
        x2.set_ylabel('PCR of trade')
        plt.setp(trade, color='b', linewidth=1.0)
        
        x3 = x1.twinx()
        # Move the last y-axis spine over to the right by 20% of the width of the axes
        x3.spines['right'].set_position(('axes', 1.2))
        # To make the border of the right-most axis visible, we need to turn the frame
        # on. This hides the other plots, however, so we need to turn its fill off.
        x3.set_frame_on(True)
        x3.patch.set_visible(False)

        sp = x3.plot(settlement_prices, label='PCR of trade')
        x3.set_ylabel('Settlement prices')
        plt.setp(sp, color='g', linewidth=1.0)

        plt.xticks(range(len(dates)), dates, rotation='vertical')
        plt.xlabel('Date')
        plt.title('Settlement price v/s PCR')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.path, "report3.png"))
