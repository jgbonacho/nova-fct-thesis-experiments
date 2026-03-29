# Report 1 - Question: Does the relative contribution to data scatter provide a good hyperparameter for the definition of the stop rules under variations in the structure/architecture parameters of LFR synthetic networks?

---

## LFR Network Parameterization

- $\overline{d}$ = 20
- $d_{max}$ = 50
- $c_{min}$ = 20
- $c_{max}$ = 100
- $t1$ = -2
- $t2$ = -1
- $n$ (2 groups) (*3 groups):
  - L: [500, 700] (*[1000, 3000])
  - M: [800, 1000] (*[4000, 6000])
  - #H: [2000, 4000] (*[7000, 10000])
- $\mu$ (2 groups) (*3 groups):
  - L: [0.1, 0.3]
  - M: [0.4, 0.6]
  - #H: [0.7, 0.8]
- $o_{n}$ / $n$ (2 groups) (*3 groups):
  - L: [0.1, 0.2]
  - M: [0.3, 0.4]
  - #H: [0.5, 0.6]
- $o_{m}$ (2 groups) (*3 groups):
  - L: [2, 3]
  - M: [4, 5]
  - #H: [6, 8]

## Network Families

| Network Family    | $n$         | $\mu$      | $o_{n}$/$n$ | $o_{m}$ |
|-------------------|-------------|------------|-------------|---------|
| 01_nL_uL_onnL_omL | [500, 700]  | [0.1, 0.3] | [0.1, 0.2]  | [2, 3]  |
| 02_nL_uL_onnL_omM | [500, 700]  | [0.1, 0.3] | [0.1, 0.2]  | [4, 5]  |
| 03_nL_uL_onnM_omL | [500, 700]  | [0.1, 0.3] | [0.3, 0.4]  | [2, 3]  |
| 04_nL_uL_onnM_omM | [500, 700]  | [0.1, 0.3] | [0.3, 0.4]  | [4, 5]  |
| 05_nL_uM_onnL_omL | [500, 700]  | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |
| 06_nL_uM_onnL_omM | [500, 700]  | [0.4, 0.6] | [0.1, 0.2]  | [4, 5]  |
| 07_nL_uM_onnM_omL | [500, 700]  | [0.4, 0.6] | [0.3, 0.4]  | [2, 3]  |
| 08_nL_uM_onnM_omM | [500, 700]  | [0.4, 0.6] | [0.3, 0.4]  | [4, 5]  |
| 09_nM_uL_onnL_omL | [800, 1000] | [0.1, 0.3] | [0.1, 0.2]  | [2, 3]  |
| 10_nM_uL_onnL_omM | [800, 1000] | [0.1, 0.3] | [0.1, 0.2]  | [4, 5]  |
| 11_nM_uL_onnM_omL | [800, 1000] | [0.1, 0.3] | [0.3, 0.4]  | [2, 3]  |
| 12_nM_uL_onnM_omM | [800, 1000] | [0.1, 0.3] | [0.3, 0.4]  | [4, 5]  |
| 13_nM_uM_onnL_omL | [800, 1000] | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |
| 14_nM_uM_onnL_omM | [800, 1000] | [0.4, 0.6] | [0.1, 0.2]  | [4, 5]  |
| 15_nM_uM_onnM_omL | [800, 1000] | [0.4, 0.6] | [0.3, 0.4]  | [2, 3]  |
| 16_nM_uM_onnM_omM | [800, 1000] | [0.4, 0.6] | [0.3, 0.4]  | [4, 5]  |

## Networks for Each Network Family

- $\overline{d}$: fixed
  - (20)
- $d_{max}$: fixed
  - (50)
- $c_{min}$: fixed
  - (20)
- $c_{max}$: fixed
  - (100)
- $t1$: fixed
  - (2.0)
- $t2$: fixed
  - (1.0)
- $n$: step 100 (*step 1000)
  - L: (500 600 700)
  - M: (800 900 1000)
- $\mu$: step 0.1
  - L: (0.1 0.2 0.3)
  - M: (0.4 0.5 0.6)
- $o_{n}$/$n$: step 0.1
  - L: (10 20)
  - M: (30 40)
- $o_{m}$: step 1
  - L: (2 3)
  - M: (4 5)
- Instances: 2 (*10)

---

## Scripts

### Script 1

- Stage 1 (obtain candidate thresholds)
  1. Choose the execution configuration: i) LAPIN-off or ii) LAPIN-on; and i) extraction of K desired clusters or ii) extraction of clusters until the end;
  2. For each network in each network family, execute FADDIS using the default input matrix and the selected configuration;
     Exceptionally, when the configuration is LAPIN-off and extraction of K desired clusters, the script extracts K + 1 clusters due to the conditional removal of the first extracted cluster, which may behave as a global/background component;
  3. Register the raw contribution values in the order in which they are extracted;
  4. Normalize the contributions by dividing each contribution value by the "universe", i.e., the sum of all contributions from all networks in all families. The normalized values are stored with 6 decimal places;
  5. Draw one line plot for each network, showing the normalized contribution by extraction number and highlighting the contribution at K;
  6. Create a table of statistics with statistical metrics for each network family, using 6 decimal places;
  7. Draw one histogram for each network family, showing the frequency distribution of the normalized contributions;
  8. Draw a line plot of the normalized contributions for each network family, with one line for each statistical metric;
  9. Draw a box plot of the normalized contributions for each network family;
  10. Create a table of candidate thresholds based on the statistical metrics;

- Stage 2 (Choose one of the candidate thresholds)
  1. Load the candidate thresholds obtained in Stage 1;
  2. For each network family, repeatedly generate bootstrap subsamples of networks by pseudo-random resampling with replacement;
  3. In each bootstrap repetition:
      - Gather the raw contributions of the sampled networks;
      - Normalize the sampled contributions by dividing each contribution value by the "universe", i.e., the sum of the contributions in that bootstrap subsample;
      - Compute the thresholds for the network family using the same statistical metrics adopted in Stage 1;
      - For each statistical metric, compare the candidate threshold with the threshold computed for the bootstrap subsample using the squared error;
  4. After the defined number of bootstrap repetitions, compute the mean squared error (MSE) of each metric;
  5. Create a table of bootstrap statistics;
  6. For each network family, select the threshold metric with the lowest MSE, that is, the one that shows the greatest stability and robustness under bootstrap resampling;
  7. Create a table with the selected threshold for each network family.

### Script 2

- Stage 1 (test thresholds)
  1. Adopt the same execution configuration used in Script 1: i) LAPIN-off or ii) LAPIN-on;
  2. Execute FADDIS on the same networks as in Script 1, using the threshold as `epsilon` (FADDIS's individual cluster contribution);
  3. Apply a defuzzification step with the default `gamma` of 0.5;
  4. Compute the extrinsic evaluation measures for each network;
  5. Draw line plots for each network family showing the evaluation metrics by network.

---

## Experience 1 (LAPIN-off + Extraction of K desired clusters)

### Contributions Line Plots

[Open Folder](../results\experience1_cluster\results_2026-03-29_16-06-42-670441)

### Statistics

| Network Family    | #Networks | Mean    | Std     | Median  | 75%      | 90%      | 95%      | Min | Max      |
|-------------------|-----------|---------|---------|---------|----------|----------|----------|-----|----------|
| 01_nL_uL_onnL_omL | 72        | 9.5e-05 | 7.8e-05 | 7.7e-05 | 0.000115 | 0.000166 | 0.000282 | 0.0 | 0.000454 |
| 02_nL_uL_onnL_omM | 72        | 8.4e-05 | 7.4e-05 | 7e-05   | 0.000104 | 0.000149 | 0.000272 | 0.0 | 0.000427 |
| 03_nL_uL_onnM_omL | 72        | 5.7e-05 | 7.3e-05 | 3.9e-05 | 6.7e-05  | 0.000105 | 0.00027  | 0.0 | 0.000411 |
| 04_nL_uL_onnM_omM | 72        | 3.9e-05 | 6.6e-05 | 2e-05   | 4.7e-05  | 7.9e-05  | 0.000114 | 0.0 | 0.000411 |
| 05_nL_uM_onnL_omL | 72        | 4.2e-05 | 7.9e-05 | 1.9e-05 | 3.8e-05  | 6.4e-05  | 0.00028  | 0.0 | 0.00041  |
| 06_nL_uM_onnL_omM | 72        | 3.6e-05 | 7.3e-05 | 1.6e-05 | 3.4e-05  | 5.8e-05  | 0.000271 | 0.0 | 0.000409 |
| 07_nL_uM_onnM_omL | 72        | 3e-05   | 7.4e-05 | 8e-06   | 2.2e-05  | 4.4e-05  | 0.00027  | 0.0 | 0.000415 |
| 08_nL_uM_onnM_omM | 72        | 2.1e-05 | 6.6e-05 | 3e-06   | 1.4e-05  | 3e-05    | 4.7e-05  | 0.0 | 0.000415 |
| 09_nM_uL_onnL_omL | 72        | 6.1e-05 | 4.7e-05 | 5.3e-05 | 7.8e-05  | 0.000108 | 0.000143 | 0.0 | 0.00028  |
| 10_nM_uL_onnL_omM | 72        | 5.2e-05 | 4.5e-05 | 4.4e-05 | 7e-05    | 9.8e-05  | 0.00012  | 0.0 | 0.000271 |
| 11_nM_uL_onnM_omL | 72        | 3.3e-05 | 4.3e-05 | 2.1e-05 | 4.4e-05  | 6.8e-05  | 9.1e-05  | 0.0 | 0.000264 |
| 12_nM_uL_onnM_omM | 72        | 2.2e-05 | 4e-05   | 8e-06   | 2.8e-05  | 5.5e-05  | 7.3e-05  | 0.0 | 0.000264 |
| 13_nM_uM_onnL_omL | 72        | 2.3e-05 | 4.5e-05 | 1.1e-05 | 2.5e-05  | 4.3e-05  | 6.1e-05  | 0.0 | 0.000256 |
| 14_nM_uM_onnL_omM | 72        | 1.9e-05 | 4.2e-05 | 8e-06   | 2.1e-05  | 3.5e-05  | 5e-05    | 0.0 | 0.000255 |
| 15_nM_uM_onnM_omL | 72        | 1.6e-05 | 4.2e-05 | 4e-06   | 1.3e-05  | 2.8e-05  | 4.3e-05  | 0.0 | 0.000256 |
| 16_nM_uM_onnM_omM | 72        | 1.3e-05 | 4e-05   | 2e-06   | 9e-06    | 2.2e-05  | 3.3e-05  | 0.0 | 0.000256 |

- #Total Networks: 1152

### Histograms

[Open Folder](../results\experience1_cluster\results_2026-03-29_16-06-42-670441)

### Line plot

![](../results\experience1_cluster\results_2026-03-29_16-06-42-670441/line_plot.png)

### Box plot

![](../results\experience1_cluster\results_2026-03-29_16-06-42-670441/boxplot.png)

### Candidate Thresholds

| Network Family    | Mean-Std | Mean    | Mean+Std | Median  | 75%      | 90%      | 95%      |
|-------------------|----------|---------|----------|---------|----------|----------|----------|
| 01_nL_uL_onnL_omL | 1.7e-05  | 9.5e-05 | 0.000173 | 7.7e-05 | 0.000115 | 0.000166 | 0.000282 |
| 02_nL_uL_onnL_omM | 1e-05    | 8.4e-05 | 0.000158 | 7e-05   | 0.000104 | 0.000149 | 0.000272 |
| 03_nL_uL_onnM_omL | -1.6e-05 | 5.7e-05 | 0.00013  | 3.9e-05 | 6.7e-05  | 0.000105 | 0.00027  |
| 04_nL_uL_onnM_omM | -2.7e-05 | 3.9e-05 | 0.000105 | 2e-05   | 4.7e-05  | 7.9e-05  | 0.000114 |
| 05_nL_uM_onnL_omL | -3.7e-05 | 4.2e-05 | 0.000121 | 1.9e-05 | 3.8e-05  | 6.4e-05  | 0.00028  |
| 06_nL_uM_onnL_omM | -3.7e-05 | 3.6e-05 | 0.000109 | 1.6e-05 | 3.4e-05  | 5.8e-05  | 0.000271 |
| 07_nL_uM_onnM_omL | -4.4e-05 | 3e-05   | 0.000104 | 8e-06   | 2.2e-05  | 4.4e-05  | 0.00027  |
| 08_nL_uM_onnM_omM | -4.5e-05 | 2.1e-05 | 8.7e-05  | 3e-06   | 1.4e-05  | 3e-05    | 4.7e-05  |
| 09_nM_uL_onnL_omL | 1.4e-05  | 6.1e-05 | 0.000108 | 5.3e-05 | 7.8e-05  | 0.000108 | 0.000143 |
| 10_nM_uL_onnL_omM | 7e-06    | 5.2e-05 | 9.7e-05  | 4.4e-05 | 7e-05    | 9.8e-05  | 0.00012  |
| 11_nM_uL_onnM_omL | -1e-05   | 3.3e-05 | 7.6e-05  | 2.1e-05 | 4.4e-05  | 6.8e-05  | 9.1e-05  |
| 12_nM_uL_onnM_omM | -1.8e-05 | 2.2e-05 | 6.2e-05  | 8e-06   | 2.8e-05  | 5.5e-05  | 7.3e-05  |
| 13_nM_uM_onnL_omL | -2.2e-05 | 2.3e-05 | 6.8e-05  | 1.1e-05 | 2.5e-05  | 4.3e-05  | 6.1e-05  |
| 14_nM_uM_onnL_omM | -2.3e-05 | 1.9e-05 | 6.1e-05  | 8e-06   | 2.1e-05  | 3.5e-05  | 5e-05    |
| 15_nM_uM_onnM_omL | -2.6e-05 | 1.6e-05 | 5.8e-05  | 4e-06   | 1.3e-05  | 2.8e-05  | 4.3e-05  |
| 16_nM_uM_onnM_omM | -2.7e-05 | 1.3e-05 | 5.3e-05  | 2e-06   | 9e-06    | 2.2e-05  | 3.3e-05  |

### Bootstrap Statistics

| Network Family    | #Networks | Subsample Size | #Bootstraps | Metric   | Candidate Threshold | MSE           |
|-------------------|-----------|----------------|-------------|----------|---------------------|---------------|
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | Mean-Std | 1.7e-05             | 3.6051e-08    |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | Mean     | 9.5e-05             | 1.05082e-06   |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | Mean+Std | 0.000173            | 3.472707e-06  |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | Median   | 7.7e-05             | 7.04192e-07   |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | 75%      | 0.000115            | 1.530023e-06  |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | 90%      | 0.000166            | 3.306089e-06  |
| 01_nL_uL_onnL_omL | 72        | 58             | 1000        | 95%      | 0.000282            | 9.530053e-06  |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | Mean-Std | 1e-05               | 1.176e-08     |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | Mean     | 8.4e-05             | 6.80863e-07   |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | Mean+Std | 0.000158            | 2.392204e-06  |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | Median   | 7e-05               | 4.75676e-07   |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | 75%      | 0.000104            | 1.035443e-06  |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | 90%      | 0.000149            | 2.140496e-06  |
| 02_nL_uL_onnL_omM | 72        | 58             | 1000        | 95%      | 0.000272            | 7.038438e-06  |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | Mean-Std | -1.6e-05            | 6.0529e-08    |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | Mean     | 5.7e-05             | 7.29588e-07   |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | Mean+Std | 0.00013             | 3.808477e-06  |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | Median   | 3.9e-05             | 3.47136e-07   |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | 75%      | 6.7e-05             | 1.035803e-06  |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | 90%      | 0.000105            | 2.454411e-06  |
| 03_nL_uL_onnM_omL | 72        | 58             | 1000        | 95%      | 0.00027             | 1.5821725e-05 |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | Mean-Std | -2.7e-05            | 2.01481e-07   |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | Mean     | 3.9e-05             | 4.03374e-07   |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | Mean+Std | 0.000105            | 2.950625e-06  |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | Median   | 2e-05               | 1.01233e-07   |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | 75%      | 4.7e-05             | 5.8338e-07    |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | 90%      | 7.9e-05             | 1.664874e-06  |
| 04_nL_uL_onnM_omM | 72        | 58             | 1000        | 95%      | 0.000114            | 3.375517e-06  |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | Mean-Std | -3.7e-05            | 8.91753e-07   |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | Mean     | 4.2e-05             | 1.164379e-06  |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | Mean+Std | 0.000121            | 9.613792e-06  |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | Median   | 1.9e-05             | 2.45185e-07   |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | 75%      | 3.8e-05             | 9.61556e-07   |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | 90%      | 6.4e-05             | 2.653388e-06  |
| 05_nL_uM_onnL_omL | 72        | 58             | 1000        | 95%      | 0.00028             | 5.1931237e-05 |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | Mean-Std | -3.7e-05            | 8.67965e-07   |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | Mean     | 3.6e-05             | 7.77474e-07   |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | Mean+Std | 0.000109            | 7.254142e-06  |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | Median   | 1.6e-05             | 1.41575e-07   |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | 75%      | 3.4e-05             | 6.82938e-07   |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | 90%      | 5.8e-05             | 2.003044e-06  |
| 06_nL_uM_onnL_omM | 72        | 58             | 1000        | 95%      | 0.000271            | 4.3761579e-05 |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | Mean-Std | -4.4e-05            | 1.735265e-06  |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | Mean     | 3e-05               | 7.82309e-07   |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | Mean+Std | 0.000104            | 9.519742e-06  |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | Median   | 8e-06               | 5.5519e-08    |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | 75%      | 2.2e-05             | 4.41174e-07   |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | 90%      | 4.4e-05             | 1.743698e-06  |
| 07_nL_uM_onnM_omL | 72        | 58             | 1000        | 95%      | 0.00027             | 6.2505783e-05 |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | Mean-Std | -4.5e-05            | 1.939827e-06  |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | Mean     | 2.1e-05             | 4.57316e-07   |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | Mean+Std | 8.7e-05             | 7.534121e-06  |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | Median   | 3e-06               | 1.2147e-08    |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | 75%      | 1.4e-05             | 2.01846e-07   |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | 90%      | 3e-05               | 9.20605e-07   |
| 08_nL_uM_onnM_omM | 72        | 58             | 1000        | 95%      | 4.7e-05             | 2.267283e-06  |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | Mean-Std | 1.4e-05             | 2.7659e-08    |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | Mean     | 6.1e-05             | 4.90169e-07   |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | Mean+Std | 0.000108            | 1.5267e-06    |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | Median   | 5.3e-05             | 3.72363e-07   |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | 75%      | 7.8e-05             | 8.04268e-07   |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | 90%      | 0.000108            | 1.538116e-06  |
| 09_nM_uL_onnL_omL | 72        | 58             | 1000        | 95%      | 0.000143            | 2.568031e-06  |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | Mean-Std | 7e-06               | 5.883e-09     |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | Mean     | 5.2e-05             | 3.1874e-07    |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | Mean+Std | 9.7e-05             | 1.114816e-06  |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | Median   | 4.4e-05             | 2.27066e-07   |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | 75%      | 7e-05               | 5.8545e-07    |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | 90%      | 9.8e-05             | 1.148746e-06  |
| 10_nM_uL_onnL_omM | 72        | 58             | 1000        | 95%      | 0.00012             | 1.661594e-06  |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | Mean-Std | -1e-05              | 3.7081e-08    |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | Mean     | 3.3e-05             | 3.58433e-07   |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | Mean+Std | 7.6e-05             | 1.927411e-06  |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | Median   | 2.1e-05             | 1.5296e-07    |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | 75%      | 4.4e-05             | 6.29714e-07   |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | 90%      | 6.8e-05             | 1.517999e-06  |
| 11_nM_uL_onnM_omL | 72        | 58             | 1000        | 95%      | 9.1e-05             | 2.698475e-06  |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | Mean-Std | -1.8e-05            | 1.30378e-07   |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | Mean     | 2.2e-05             | 2.24547e-07   |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | Mean+Std | 6.2e-05             | 1.711018e-06  |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | Median   | 8e-06               | 3.2798e-08    |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | 75%      | 2.8e-05             | 3.41812e-07   |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | 90%      | 5.5e-05             | 1.307267e-06  |
| 12_nM_uL_onnM_omM | 72        | 58             | 1000        | 95%      | 7.3e-05             | 2.369712e-06  |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | Mean-Std | -2.2e-05            | 4.63376e-07   |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | Mean     | 2.3e-05             | 5.56597e-07   |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | Mean+Std | 6.8e-05             | 4.713852e-06  |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | Median   | 1.1e-05             | 1.14944e-07   |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | 75%      | 2.5e-05             | 6.40296e-07   |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | 90%      | 4.3e-05             | 1.855859e-06  |
| 13_nM_uM_onnL_omL | 72        | 58             | 1000        | 95%      | 6.1e-05             | 3.815864e-06  |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | Mean-Std | -2.3e-05            | 5.05209e-07   |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | Mean     | 1.9e-05             | 3.89067e-07   |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | Mean+Std | 6.1e-05             | 3.829912e-06  |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | Median   | 8e-06               | 5.9252e-08    |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | 75%      | 2.1e-05             | 4.42023e-07   |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | 90%      | 3.5e-05             | 1.281237e-06  |
| 14_nM_uM_onnL_omM | 72        | 58             | 1000        | 95%      | 5e-05               | 2.502472e-06  |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | Mean-Std | -2.6e-05            | 1.117115e-06  |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | Mean     | 1.6e-05             | 4.07692e-07   |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | Mean+Std | 5.8e-05             | 5.444117e-06  |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | Median   | 4e-06               | 2.1662e-08    |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | 75%      | 1.3e-05             | 2.74971e-07   |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | 90%      | 2.8e-05             | 1.250113e-06  |
| 15_nM_uM_onnM_omL | 72        | 58             | 1000        | 95%      | 4.3e-05             | 3.031483e-06  |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | Mean-Std | -2.7e-05            | 1.384486e-06  |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | Mean     | 1.3e-05             | 3.13353e-07   |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | Mean+Std | 5.3e-05             | 5.270775e-06  |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | Median   | 2e-06               | 6.471e-09     |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | 75%      | 9e-06               | 1.50153e-07   |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | 90%      | 2.2e-05             | 8.97857e-07   |
| 16_nM_uM_onnM_omM | 72        | 58             | 1000        | 95%      | 3.3e-05             | 2.069605e-06  |

### Thresholds

| Network Family    | Selected Metric | Threshold |
|-------------------|-----------------|-----------|
| 01_nL_uL_onnL_omL | Mean-Std        | 1.7e-05   |
| 02_nL_uL_onnL_omM | Mean-Std        | 1e-05     |
| 03_nL_uL_onnM_omL | Mean-Std        | -1.6e-05  |
| 04_nL_uL_onnM_omM | Median          | 2e-05     |
| 05_nL_uM_onnL_omL | Median          | 1.9e-05   |
| 06_nL_uM_onnL_omM | Median          | 1.6e-05   |
| 07_nL_uM_onnM_omL | Median          | 8e-06     |
| 08_nL_uM_onnM_omM | Median          | 3e-06     |
| 09_nM_uL_onnL_omL | Mean-Std        | 1.4e-05   |
| 10_nM_uL_onnL_omM | Mean-Std        | 7e-06     |
| 11_nM_uL_onnM_omL | Mean-Std        | -1e-05    |
| 12_nM_uL_onnM_omM | Median          | 8e-06     |
| 13_nM_uM_onnL_omL | Median          | 1.1e-05   |
| 14_nM_uM_onnL_omM | Median          | 8e-06     |
| 15_nM_uM_onnM_omL | Median          | 4e-06     |
| 16_nM_uM_onnM_omM | Median          | 2e-06     |

### Extrinsic Metrics Results

[Open Folder](../results\experience1_cluster\results_2026-03-29_23-26-27-954876)

---

## Experience 2 (LAPIN-off + Extraction of clusters until the end)

---

## Experience 3 (LAPIN-on + Extraction of K desired clusters)

---

## Experience 4 (LAPIN-on + Extraction of clusters until the end)
