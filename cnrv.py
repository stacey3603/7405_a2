import numpy as np


def Cov(x, y):
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    sub_x = [i-mean_x for i in x]
    sub_y = [i-mean_y for i in y]
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    std_deviation_x = sum([sub_x[i]**2.0 for i in range(len(sub_x))])
    std_deviation_y = sum([sub_y[i]**2.0 for i in range(len(sub_y))])
    denominator = (std_deviation_x*std_deviation_y)**0.5
    cor = numerator/denominator
    return cor


def CovZ():
    x = np.random.standard_normal(200)
    y = np.random.standard_normal(200)
    z = 0.5*x + np.sqrt(0.75)*y
    result = Cov(x, z)
    return result


def Prove():
    corArray = []
    i = 1
    while i < 10000:
        corArray.append(CovZ())
        i += 1
    print(np.mean(corArray))


Prove()
# result = 0.49851 (result may vary)
# we can see from above, if repeat calculation process, correlation coefficient between X and Z is very close to theoretical value 0.5
