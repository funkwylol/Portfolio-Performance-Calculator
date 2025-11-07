import random
portfolio = 100
risk = 0.05
riskreward_ratio = 2

counter = 0

while counter < 20 :
    random_float = random.random();
    if random_float < (0.7) :
        portfolio += (portfolio * (riskreward_ratio * risk))
    else :
        portfolio -= (portfolio * (risk))
    counter += 1

print (portfolio)