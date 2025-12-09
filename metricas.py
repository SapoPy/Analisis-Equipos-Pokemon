import numpy as np

def information(p):
    return -np.log2(p)

def entropy(p):
    return p * information(p)


calyrex = 0.274
urshifu = 0.272
urshifu_dado_calyrex = 0.96769
calyrex_dado_urshifu = 1.0000
print(calyrex * urshifu_dado_calyrex)
print(f"Informacion por Caly: {information(calyrex * urshifu_dado_calyrex)}")
print(urshifu * calyrex_dado_urshifu)
print(f"Informacion por urshi: {information(urshifu * calyrex_dado_urshifu)}")

print(sum([]))