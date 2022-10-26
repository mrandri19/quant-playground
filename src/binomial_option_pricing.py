from math import sqrt


class BinomialTree:
    def __init__(self, depth) -> None:
        self.depth = depth
        self.arr = [[None for _ in range(depth)] for _ in range(depth)]

    def __repr__(self) -> str:
        s = []
        for a in self.arr:
            for e in a:
                if e is None:
                    s.append("    ")
                else:
                    s.append(f"{e:6.2f} ")
            s.append("\n")
        return "".join(s)


def compute_stock_geometric_random_walk(tree, u, v, S):
    tree.arr[0][0] = S

    for i in range(1, tree.depth):
        for j in range(i):
            tree.arr[i][j] = tree.arr[i - 1][j] * v
            tree.arr[i][j + 1] = tree.arr[i - 1][j] * u


def compute_payoff_at_expiry(
    stock_tree: BinomialTree, option_tree: BinomialTree, payoff
):
    assert stock_tree.depth == option_tree.depth
    d = stock_tree.depth

    for i in range(d):
        s = stock_tree.arr[d - 1][i]
        option_tree.arr[d - 1][i] = payoff(s)


def compute_values(option_tree: BinomialTree, r, sigma, delta_t):
    for i in range(option_tree.depth - 2, -1, -1):
        for j in range(i + 1):
            # TODO(Andrea): use the exact formula
            p_prime = 0.5 + (r - 0.5 * sigma**2) * sqrt(delta_t) / (2 * sigma)
            v_plus = option_tree.arr[i + 1][j + 1]
            v_minus = option_tree.arr[i + 1][j]
            v = p_prime * v_plus + (1 - p_prime) * v_minus
            option_tree.arr[i][j] = v


if __name__ == "__main__":
    depth = 4 + 1
    delta_t = 1 / 12
    r = 0.1
    sigma = 0.2
    E = 100
    S = 100

    u = 1 + sigma * sqrt(delta_t) + 0.5 * (sigma**2) * delta_t
    v = 1 - sigma * sqrt(delta_t) + 0.5 * (sigma**2) * delta_t

    stock_tree = BinomialTree(depth)
    # TODO(Andrea): use the formula in terms of drift and volatility, not the value
    compute_stock_geometric_random_walk(stock_tree, u, v, S)
    print("Stock tree")
    print("----------")
    print(stock_tree)

    option_tree = BinomialTree(depth)
    compute_payoff_at_expiry(stock_tree, option_tree, lambda s: max(s - E, 0))
    compute_values(option_tree, r, sigma, delta_t)
    print("Option tree")
    print("-----------")
    print(option_tree)

    print(f"Time delta: {delta_t:6.2f}")
    print(f"Interest rate: {r:6.2f}")
    print(f"Volatility: {sigma:6.2f}")
    print(f"Strike: {E:6.2f}")
    print(f"The option value at present time: {option_tree.arr[0][0]:6.2f}")
