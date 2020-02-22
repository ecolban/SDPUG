from math import sqrt, exp, pi as π, log
from random import choices, gauss, uniform

import matplotlib.pyplot as plt
import numpy as np

from ..src.timethis import timeblock, timethis


# In Python 3.6: random.choices(samples, weights, k = 1)

def numpy_choices(samples, weights, k=1):
    sum_weights = sum(weights)
    probabilities = [w / sum_weights for w in weights]
    return np.random.choice(samples, k, p=probabilities)


def my_choices_slow(samples, weights, k=1):
    weights_acc = weights[:]
    for i, w in enumerate(weights[1:], 1):
        weights_acc[i] = weights_acc[i - 1] + w

    events = [uniform(0, weights_acc[-1]) for _ in range(k)]
    events.sort()

    i, res = 0, []
    for e in events:
        while weights_acc[i] < e:
            i += 1
        res.append(samples[i])
    return res


def exponential(λ=1.0):
    return -log(uniform(0, 1)) * λ


def my_choices_fast(samples, weights, k=1):
    weights_acc = weights[:]
    for i, w in enumerate(weights[1:], 1):
        weights_acc[i] = weights_acc[i - 1] + w
    w_max = weights_acc[-1]

    events = [exponential() for _ in range(k)]
    for i, e in enumerate(events[1:], 1):
        events[i] = events[i - 1] + e
    e_max = events[-1] + exponential()

    i, res = 0, []
    for e in events:
        while weights_acc[i] * e_max < e * w_max:
            i += 1
        res.append(samples[i])
    return res


def show_uniform_dist(sample_size, bins):
    selection = [uniform(0, sample_size) for _ in range(sample_size)]
    plt.hist(selection, bins)
    plt.show()


def show_uniform_diffs_dist(sample_size, bins):
    uniform_selection = [uniform(0, sample_size) for _ in range(sample_size)]
    uniform_selection.sort()
    diffs_selection = [x - y for x, y in zip(uniform_selection[1:], uniform_selection)]
    plt.hist(diffs_selection, bins)
    plt.show()


def show_exponential_dist(sample_size, bins):
    plt.hist([-log(uniform(0, 1)) for _ in range(sample_size + 1)], bins)
    plt.show()


def show_exponential_sum_dist(sample_size, bins):
    def gen_events():
        e = 0
        for _ in range(sample_size):
            e += -log(uniform(0, 1))
            yield e
    plt.hist([w for w in gen_events()], bins)
    plt.show()


def gaussian_pdf(x, μ=0.0, σ=1.0):
    """The normal distribution probability density function."""
    d = x - μ
    var = σ * σ
    return exp(-d * d / (2 * var)) / sqrt(2 * π * var)


def compare_choices_algos(num_samples, repeats):
    samples = [gauss(5.2, 6.5) for _ in (range(num_samples))]
    weights = [gaussian_pdf(x, μ=2.6, σ=3.5) for x in samples]

    for description, algo in (('Using Python 3.6 choices()', choices),
                              ('Using numpy.random.choice()', numpy_choices),
                              ('Using my_choices_slow()', my_choices_slow),
                              ('Using my_choices_fast()', my_choices_fast)):
        with timeblock(description):
            for _ in range(repeats):
                algo(samples, weights, k=num_samples)


@timethis
def particle_filter_step(samples_pre, *, resampling):
    weights = [gaussian_pdf(x, μ=2.6, σ=3.5) for x in samples_pre]
    print('Prior: mean = %.2f, sigma = %.2f' % mean_and_sigma(samples_pre))
    samples_post = resampling(samples_pre, weights, k=len(samples_pre))
    print('Posterior: mean = %.2f, sigma = %.2f' % mean_and_sigma(samples_post))
    # Update samples states (control and diffusion)


def mean_and_sigma(samples):
    n = len(samples)
    mean = sum(samples) / n
    # variance = sum((x - mean) ** 2 for x in samples) / 2
    variance = sum(x * x for x in samples) / n - mean * mean
    return mean, sqrt(variance)


def theoretically(mu_0, sigma_0, mu_1, sigma_1):
    s0 = sigma_0 * sigma_0
    s1 = sigma_1 * sigma_1
    k = s0 / (s0 + s1)
    return mu_0 + k * (mu_1 - mu_0), sqrt(s0 - k * s0)


def compare_particle_filter_step(num_samples):

    print("\nThe theoretical result")
    print("======================")
    print("μ' = %.2f, σ' = %.2f" % theoretically(5.2, 6.5, 2.6, 3.5))

    samples_pre = [gauss(5.2, 6.5) for _ in (range(num_samples))]

    print("\nRun test using choices in Python 3.6")
    print("====================================")
    particle_filter_step(samples_pre, resampling=choices)

    print("\nRun test using numpy.random.choice")
    print("==================================")
    particle_filter_step(samples_pre, resampling=numpy_choices)

    print("\nRun test using my_choices_slow")
    print("==============================")
    particle_filter_step(samples_pre, resampling=my_choices_slow)

    print("\nRun test using my_choices_fast")
    print("==============================")
    particle_filter_step(samples_pre, resampling=my_choices_fast)
