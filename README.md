# check-if-power-law

This is an example showing how we can validate the hypothesis that a distribution follows the power-law. For more details from the theoretical aspects, please refer to the paper "Power-law distributions in empirical data." by Clauset et al. or our slides attached in this github repo.

## Organization
1. The python code is in `powerlaw.ipynb`. 
2. The specific steps are explained in the slides `Plotting_Power_laws_and_the_Degree_Exponent.pdf`.
3. The output figures are in `powerlaw_report.pdf`. We also consider the log-logistic distribution.
4. The parallelized synthetic data generation code can be found at `powerlaw_synthetic_parallel.py`. 

## Figures 
![alt text](https://github.com/xiaoylu/check-if-power-law/blob/master/figures/scatter.png "Distribtuion of the real data.")

The slope in double logarithm scale is the exponent of the power-law. KS distance measure the "distance" of the real data and obtained model. $K_min=2$:
![alt text](https://github.com/xiaoylu/check-if-power-law/blob/master/figures/fit.png "Fit the data")

Using the obtained model, we generate synthetic sequences, which are used to evaluate the goodness of fit.
![alt text](https://github.com/xiaoylu/check-if-power-law/blob/master/figures/synthetic.png "synthetic sequences")

The p-value is exactly the portion of synthetic sequences whose KS distance is larger than the real data's. When p-value is large enough, >10% in most cases, we can say the Power-law is a plausible fit to the real data.
![alt text](https://github.com/xiaoylu/check-if-power-law/blob/master/figures/pvalue.png "pvalue")




