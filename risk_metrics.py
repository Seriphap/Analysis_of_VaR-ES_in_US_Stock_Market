import numpy as np

def calculate_var_es(returns, confidence_level):
    if returns is None or len(returns) == 0:
        return None, None

    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))

    if index < 1:
        return None, None

    var = -sorted_returns[index]
    es = -sorted_returns[:index].mean()
    return var, es

