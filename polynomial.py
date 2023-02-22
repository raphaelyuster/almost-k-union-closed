# compute the factorial of j
def fact(j):
    r = 1
    for i in range(j):
        r = r * (i + 1)
    return r


# computes the coefficient of the term corresponding to h^{(j)}(x^k) in r_k^{(t)}
def cr(k, t, j):
    if j > t:
        return 0
    if j == 0:
        if t == 0:
            return 1
        return 0
    return cr(k, t - 1, j) * (j * k - t + 1) + cr(k, t - 1, j - 1) * k


# multiply a polynomial by a scalar
def mult_scalar_polynomial(l1, c):
    l2 = [0 for _ in range(len(l1))]
    for i in range(len(l1)):
        l2[i] = l1[i] * c
    return l2


# divide a polynomial by a scalar
def div_scalar_polynomial(l1, c):
    l2 = [0 for _ in range(len(l1))]
    for i in range(len(l1)):
        l2[i] = l1[i] // c
    return l2


# add two polynomials whose coefficients are given in lists
def add_polynomials(l1, l2):
    l3 = [0 for _ in range(max(len(l1), len(l2)))]
    for i in range(max(len(l1), len(l2))):
        if i < len(l1):
            l3[i] = l3[i] + l1[i]
        if i < len(l2):
            l3[i] = l3[i] + l2[i]
    return l3


# multiply two polynomials whose coefficients are given in lists
def multiply_polynomials(l1, l2):
    l3 = [0 for _ in range(len(l1) + len(l2) - 1)]
    for i in range(len(l1)):
        for j in range(len(l2)):
            l3[i + j] = l3[i + j] + l1[i] * l2[j]
    return l3


# compute a term of rho(k,x). Returns a polynomial as a list of coefficients
def rho(k, j):
    poly1 = [0 for _ in range(k + 1)]
    poly1[0] = -1
    poly1[k] = 1
    # poly1 is (x^k-1).

    poly2 = [0 for _ in range(1)]
    poly2[0] = 1
    for i in range(k):
        poly2 = multiply_polynomials(poly2, poly1)
    # poly2 is (x^k-1)^k

    poly3 = [0 for _ in range(1)]
    poly3[0] = 1
    for i in range(k - j - 1):
        poly3 = multiply_polynomials(poly3, poly1)
    # poly3 is (x^k-1)^(k-j-1)

    poly4 = [0 for _ in range(k * j + k + 1)]
    poly4[k * j + k] = 1
    poly5 = multiply_polynomials(poly4, poly3)
    # poly5 is (x^k-1)^{k-j-1}*x^{kj+k}

    poly6 = add_polynomials(poly5, mult_scalar_polynomial(poly2, -1))

    f = fact(j)
    if j % 2 == 1:
        f = -f

    return mult_scalar_polynomial(poly6, f * cr(k, k + 1, j + 2))


# compute rho(x)
def rho_x(k):
    poly = [0 for _ in range(k * k)]
    for j in range(k):
        poly = add_polynomials(poly, rho(k, j))
    poly = div_scalar_polynomial(poly, fact(k - 1))
    return poly


# compute a term of sigma(k,x). Returns a polynomial as a list of coefficients
def sigma(k, j):
    poly1 = [0 for _ in range(k + 1)]
    poly1[0] = -1
    poly1[k] = 1
    # poly1 is (x^k-1)

    poly2 = [0 for _ in range(1)]
    poly2[0] = 1
    for i in range(k):
        poly2 = multiply_polynomials(poly2, poly1)
    # poly2 is (x^k-1)^k

    poly3 = [0 for _ in range(j + 2)]
    poly3[j + 1] = 1
    # poly3 is x^{j+1}

    poly4 = [0 for _ in range(2)]
    poly4[0] = -1
    poly4[1] = 1
    poly5 = [0 for _ in range(1)]
    poly5[0] = 1
    for i in range(k - j - 1):
        poly5 = multiply_polynomials(poly5, poly4)
    # poly5 is (x-1)^{k-j-1}
    poly5 = multiply_polynomials(poly5, poly3)
    # poly5 is (x-1)^{k-j-1}*x^{j+1}

    poly6 = [1 for _ in range(k)]
    poly7 = [0 for _ in range(1)]
    poly7[0] = 1
    for i in range(k):
        poly7 = multiply_polynomials(poly7, poly6)

    poly7 = multiply_polynomials(poly7, poly5)
    poly8 = add_polynomials(poly7, mult_scalar_polynomial(poly2, -1))

    f1 = fact(k - 1)
    f2 = fact(k + 1)
    f3 = fact(j + 2)
    f4 = fact(k + 1 - j - 2)
    f = f1 * f2 // (f3 * f4)
    if j % 2 == 1:
        f = -f
    return mult_scalar_polynomial(poly8, f)


# compute sigma(x)
def sigma_x(k):
    poly = [0 for _ in range(k * k)]
    for j in range(k):
        poly = add_polynomials(poly, sigma(k, j))
    poly = div_scalar_polynomial(poly, fact(k - 1))
    return poly


# print the polynomial p_k(x)
def print_p(k):
    r = rho_x(k)
    s = sigma_x(k)
    print(r)
    print(s)
    for i in range(len(r) - 1):
        if i > 0 and (s[i] != 0 or r[i] != 0):
            print("+", end="")
        if r[i] != 0 and s[i] != 0:
            if s[i] > 0:
                print("(" + str(r[i]) + "a" + str(-s[i]) + ")" + "x^" + str(i), end="")
            else:
                print("(" + str(r[i]) + "a" + "+" + str(-s[i]) + ")" + "x^" + str(i), end="")
        elif r[i] != 0:
            print("(" + str(r[i]) + "a" + ")" + "x^" + str(i), end="")
        elif s[i] != 0:
            if s[i] > 0:
                print("(" + str(-s[i]) + ")" + "x^" + str(i), end="")
            else:
                print("(" + str(-s[i]) + ")" + "x^" + str(i), end="")


# tests #
print_p(4)  # this prints p_4(x)
