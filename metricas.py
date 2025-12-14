import numpy as np

def information(p):
    """
    Calcula la informacion de p
    """
    return -np.log(p)

def entropy(p: float, eps=1e-12) -> float:
    """
    Calcula la entropia de p
    """
    if p <= eps or p >= 1:
        return 0.0
    else:
        return -p * np.log(p)


if __name__ == "__main__":
    calyrex = 0.274
    urshifu = 0.272
    urshifu_dado_calyrex = 0.96769
    calyrex_dado_urshifu = 1.0000
    print(calyrex * urshifu_dado_calyrex)
    print(f"Informacion por Caly: {information(calyrex * urshifu_dado_calyrex)}")
    print(urshifu * calyrex_dado_urshifu)
    print(f"Informacion por urshi: {information(urshifu * calyrex_dado_urshifu)}")

    print(sum([]))