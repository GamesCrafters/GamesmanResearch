from scipy.special import comb

total = 0
for L in range(5):
    C_sum = 0
    for C in range(L + 1):
        S_sum = 0
        for S in range(4 - C + 1):
            R_sum = 0
            for R in range(3):
                B_sum = 0
                for B in range(3):
                    B_sum += comb(9 - L + C - R, B, True)
                R_sum += comb(9 - L + C, R, True) * B_sum
            S_sum += comb(9 - L, S, True) * R_sum
        C_sum += comb(L, C) * S_sum
    total += comb(9, L) * C_sum

print(total - 756)
