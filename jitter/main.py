from intensity_prob import IntensityDistribution
from Data.tests_generated.beta_distibution import sample


def main():
    distribution = IntensityDistribution(sample.intensity)
    distribution.plot()
    # print(distribution.sigma)


if __name__ == '__main__':
    main()
