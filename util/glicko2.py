import math

SCALE = 173.7178
RATE = 1500
RD = 100
VOLATALITY = 0.06
TAU = 0.5
EPSILON = 0.000001
DISPLAY_RD = 50
WIN = 1
LOSE = 0


class Rate:
    def __init__(self, rating=RATE, rd=RD, volatality=VOLATALITY):
        self.rating = int(rating)
        self.rd = rd
        self.volatality = volatality

    def __repr__(self):
        return "rating: {0:d} rd: {1} volatality: {2} mu: {3:.4f} phi: {4:.4f}".format(
            self.rating, self.rd, self.volatality, self.mu, self.phi
        )

    def copy(self):
        return Rate(self.rating, self.rd, self.volatality)

    @property
    def mu(self):
        return (self.rating - RATE) / SCALE

    @property
    def phi(self):
        return self.rd / SCALE

    def add_match(self, opponents):
        v = 1 / sum([o[0].v_element(self.mu) for o in opponents])
        delta = v * sum([o[0].delta_element(self.mu, o[1]) for o in opponents])
        alpha = math.log(self.volatality ** 2)

        delta_2 = delta ** 2
        phi_2 = self.phi ** 2

        def f(x):
            pvex = phi_2 + v + math.exp(x)
            left = math.exp(x) * (delta_2 - pvex) / (2 * pvex ** 2)
            right = (x - alpha) / (TAU ** 2)
            return left - right

        a = alpha
        if delta_2 > phi_2 + v:
            b = math.log(delta_2 - phi_2 - v)
        else:
            k = 1
            while f(alpha - k * math.sqrt(TAU ** 2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(TAU ** 2)
        f_a, f_b = f(a), f(b)

        while abs(b - a) > EPSILON:
            c = a + (a - b) * f_a / (f_b - f_a)
            f_c = f(c)
            a, f_a = (b, f_b) if f_c * f_b < 0 else (a, f_a / 2)
            b, f_b = c, f_c

        self.volatality = math.exp(1) ** (a / 2)
        phi_star = math.sqrt(phi_2 + self.volatality ** 2)
        phi_dash = 1 / math.sqrt(1 / phi_star ** 2 + 1 / v)
        new_mu = self.mu + phi_dash ** 2 * (delta / v)

        self.rating = int(new_mu * SCALE + RATE)
        self.rd = int(phi_dash * SCALE)

    @property
    def g(self):
        return 1 / math.sqrt(1 + (3 * self.phi ** 2) / (math.pi ** 2))

    def e(self, mu):
        return 1 / (1 + math.exp(-self.g * (mu - self.mu)))

    def v_element(self, mu):
        return self.g ** 2 * self.e(mu) * (1 - self.e(mu))

    def delta_element(self, mu, score):
        return self.g * (score - self.e(mu))

    @property
    def range(self):
        return self.rating - self.rd * 2, self.rating + self.rd * 2
