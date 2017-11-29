from pymprog import *


class OptimizeService:

    def calc(self, minerals, ores, ore_prices):
        result = []


        # minerals = [10000, 800, 125]
        # ores = [
        #     [1000,   0,  50],
        #     [ 500, 100,   0],
        # ]
        # ore_prices = [ 55000, 3500 ]
        # x1 = 2.5
        # x2 = 15.0

        ore_cnt = len(ores)
        mnr_cnt = len(minerals)

        p = model('Aes')
        p.verbose(False)

        x = p.var('x', ore_cnt)

        p.minimize( sum( x[i]*ore_prices[i] for i in range(ore_cnt) ) )

        for im in range(mnr_cnt):
            sum( ores[io][im] * x[io] for io in range(ore_cnt) ) >= minerals[im]

        p.solve()

        p.sensitivity()

        for i in range(ore_cnt):
            result.append(x[i].primal)

        p.end()

        return result