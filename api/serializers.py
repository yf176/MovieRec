import math

def W(Tmax, Tui):
    term1 = 68.2 * math.exp(-0.0445 * Tmax * Tui / 60)
    term2 = 33.2 * math.exp(-0.12 * 0.0001 * Tmax * Tui / 60)
    return term1 + term2

# Example usage:
Tmax = 100
Tui = 50
t = 10

result = W(Tmax, Tui)
print("W(t) =", result)
