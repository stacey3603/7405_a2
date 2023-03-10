import numpy as np
from scipy.stats import norm

N = norm.cdf

def BS_MODEL(S, K, t, T, sigma, r):
    d1 = (np.log(S/K) + r*(T-t)) / (sigma*np.sqrt(T-t)) + (sigma/2)*np.sqrt(T-t)
    d2 = d1 - sigma * np.sqrt(T-t)
    callPrice=S * N(d1) - K * np.exp(-r*(T-t))* N(d2)
    putPrice=K*np.exp(-r*(T-t))*N(-d2) - S*N(-d1)
    print("callPrice",callPrice,sep=":")
    print("putPrice",putPrice,sep=":")


BS_MODEL(50,50,0,0.5,0.2,0.01)
BS_MODEL(50,60,0,0.5,0.2,0.01)
BS_MODEL(50,50,0,1,0.2,0.01)
BS_MODEL(50,50,0,0.5,0.3,0.01)
BS_MODEL(50,50,0,0.5,0.2,0.02)

# result:
# 3.1 callPrice:2.9380121169138036 putPrice:2.6886360765479225
# 3.2 callPrice:0.3870694028577839 putPrice:10.08781815441872
# 3.3 callPrice:4.216659345054804  putPrice:3.7191510325132064
# 3.4 callPrice:4.338822781168002  putPrice:4.089446740802121
# 3.5 callPrice:3.060327056727921  putPrice:2.5628187441863233

# The effects of parameter on call put option price:
#     1 strike:
#         call: decrease as strike price increase
#         put:  increase as strike price increase
#     2 maturity:
#         call: increase as maturity increase
#         put:  increase as maturity increase
#     3 volatility:
#         call: increase as volatility increase
#         put:  increase as volatility increase
#     4 risk free rate:
#         call: increase as risk free rate increase
#         put:  decrease as risk free rate increase
 

