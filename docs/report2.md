# Report 2 - Extend the experiment to larger networks and larger parameter values



## Table of Contents
- [Networks](#networks)
- [Scripts](#scripts)
- [Experience 5 (LAPIN-off + Extraction of K desired clusters)](#experience-5-lapin-off--extraction-of-k-desired-clusters)
- [Experience 6 (LAPIN-off + Extraction of clusters until the end)](#experience-6-lapin-off--extraction-of-clusters-until-the-end)
- [Experience 7 (LAPIN-on + Extraction of K desired clusters)](#experience-7-lapin-on--extraction-of-k-desired-clusters)
- [Experience 8 (LAPIN-on + Extraction of clusters until the end)](#experience-8-lapin-on--extraction-of-clusters-until-the-end)
- [Discussion](#discussion)



## Networks

### LFR Network Parameterization

- $\overline{d}$ = 20
- $d_{max}$ = 50
- $c_{min}$ = 20
- $c_{max}$ = 100
- $t1$ = -2
- $t2$ = -1
- $n$ (4 groups):
  - L: [500, 700]
  - M: [800, 1000]
  - H: [2000, 5000]
  - VH: [6000, 10000]
- $\mu$ (3 groups):
  - L: [0.1, 0.3]
  - M: [0.4, 0.6]
  - H: [0.7, 0.8]
- $o_{n}$ / $n$ (3 groups):
  - L: [0.1, 0.2]
  - M: [0.3, 0.4]
  - H: [0.5, 0.6]
- $o_{m}$ (3 groups):
  - L: [2, 3]
  - M: [4, 5]
  - H: [6, 8]

### Network Families

| Network Family      | $n$           | $\mu$      | $o_{n}$/$n$| $o_{m}$|
|---------------------|---------------|------------|------------|--------|
| 01_nL_uL_onnL_omL   | [500, 700]    | [0.1, 0.3] | [0.1, 0.2] | [2, 3] |
| 02_nL_uL_onnL_omM   | [500, 700]    | [0.1, 0.3] | [0.1, 0.2] | [4, 5] |
| 03_nL_uL_onnL_omH   | [500, 700]    | [0.1, 0.3] | [0.1, 0.2] | [6, 8] |
| 04_nL_uL_onnM_omL   | [500, 700]    | [0.1, 0.3] | [0.3, 0.4] | [2, 3] |
| 05_nL_uL_onnM_omM   | [500, 700]    | [0.1, 0.3] | [0.3, 0.4] | [4, 5] |
| 06_nL_uL_onnM_omH   | [500, 700]    | [0.1, 0.3] | [0.3, 0.4] | [6, 8] |
| 07_nL_uL_onnH_omL   | [500, 700]    | [0.1, 0.3] | [0.5, 0.6] | [2, 3] |
| 08_nL_uL_onnH_omM   | [500, 700]    | [0.1, 0.3] | [0.5, 0.6] | [4, 5] |
| 09_nL_uL_onnH_omH   | [500, 700]    | [0.1, 0.3] | [0.5, 0.6] | [6, 8] |
| 10_nL_uM_onnL_omL   | [500, 700]    | [0.4, 0.6] | [0.1, 0.2] | [2, 3] |
| 11_nL_uM_onnL_omM   | [500, 700]    | [0.4, 0.6] | [0.1, 0.2] | [4, 5] |
| 12_nL_uM_onnL_omH   | [500, 700]    | [0.4, 0.6] | [0.1, 0.2] | [6, 8] |
| 13_nL_uM_onnM_omL   | [500, 700]    | [0.4, 0.6] | [0.3, 0.4] | [2, 3] |
| 14_nL_uM_onnM_omM   | [500, 700]    | [0.4, 0.6] | [0.3, 0.4] | [4, 5] |
| 15_nL_uM_onnM_omH   | [500, 700]    | [0.4, 0.6] | [0.3, 0.4] | [6, 8] |
| 16_nL_uM_onnH_omL   | [500, 700]    | [0.4, 0.6] | [0.5, 0.6] | [2, 3] |
| 17_nL_uM_onnH_omM   | [500, 700]    | [0.4, 0.6] | [0.5, 0.6] | [4, 5] |
| 18_nL_uM_onnH_omH   | [500, 700]    | [0.4, 0.6] | [0.5, 0.6] | [6, 8] |
| 19_nL_uH_onnL_omL   | [500, 700]    | [0.7, 0.8] | [0.1, 0.2] | [2, 3] |
| 20_nL_uH_onnL_omM   | [500, 700]    | [0.7, 0.8] | [0.1, 0.2] | [4, 5] |
| 21_nL_uH_onnL_omH   | [500, 700]    | [0.7, 0.8] | [0.1, 0.2] | [6, 8] |
| 22_nL_uH_onnM_omL   | [500, 700]    | [0.7, 0.8] | [0.3, 0.4] | [2, 3] |
| 23_nL_uH_onnM_omM   | [500, 700]    | [0.7, 0.8] | [0.3, 0.4] | [4, 5] |
| 24_nL_uH_onnM_omH   | [500, 700]    | [0.7, 0.8] | [0.3, 0.4] | [6, 8] |
| 25_nL_uH_onnH_omL   | [500, 700]    | [0.7, 0.8] | [0.5, 0.6] | [2, 3] |
| 26_nL_uH_onnH_omM   | [500, 700]    | [0.7, 0.8] | [0.5, 0.6] | [4, 5] |
| 27_nL_uH_onnH_omH   | [500, 700]    | [0.7, 0.8] | [0.5, 0.6] | [6, 8] |
| 28_nM_uL_onnL_omL   | [800, 1000]   | [0.1, 0.3] | [0.1, 0.2] | [2, 3] |
| 29_nM_uL_onnL_omM   | [800, 1000]   | [0.1, 0.3] | [0.1, 0.2] | [4, 5] |
| 30_nM_uL_onnL_omH   | [800, 1000]   | [0.1, 0.3] | [0.1, 0.2] | [6, 8] |
| 31_nM_uL_onnM_omL   | [800, 1000]   | [0.1, 0.3] | [0.3, 0.4] | [2, 3] |
| 32_nM_uL_onnM_omM   | [800, 1000]   | [0.1, 0.3] | [0.3, 0.4] | [4, 5] |
| 33_nM_uL_onnM_omH   | [800, 1000]   | [0.1, 0.3] | [0.3, 0.4] | [6, 8] |
| 34_nM_uL_onnH_omL   | [800, 1000]   | [0.1, 0.3] | [0.5, 0.6] | [2, 3] |
| 35_nM_uL_onnH_omM   | [800, 1000]   | [0.1, 0.3] | [0.5, 0.6] | [4, 5] |
| 36_nM_uL_onnH_omH   | [800, 1000]   | [0.1, 0.3] | [0.5, 0.6] | [6, 8] |
| 37_nM_uM_onnL_omL   | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2] | [2, 3] |
| 38_nM_uM_onnL_omM   | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2] | [4, 5] |
| 39_nM_uM_onnL_omH   | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2] | [6, 8] |
| 40_nM_uM_onnM_omL   | [800, 1000]   | [0.4, 0.6] | [0.3, 0.4] | [2, 3] |
| 41_nM_uM_onnM_omM   | [800, 1000]   | [0.4, 0.6] | [0.3, 0.4] | [4, 5] |
| 42_nM_uM_onnM_omH   | [800, 1000]   | [0.4, 0.6] | [0.3, 0.4] | [6, 8] |
| 43_nM_uM_onnH_omL   | [800, 1000]   | [0.4, 0.6] | [0.5, 0.6] | [2, 3] |
| 44_nM_uM_onnH_omM   | [800, 1000]   | [0.4, 0.6] | [0.5, 0.6] | [4, 5] |
| 45_nM_uM_onnH_omH   | [800, 1000]   | [0.4, 0.6] | [0.5, 0.6] | [6, 8] |
| 46_nM_uH_onnL_omL   | [800, 1000]   | [0.7, 0.8] | [0.1, 0.2] | [2, 3] |
| 47_nM_uH_onnL_omM   | [800, 1000]   | [0.7, 0.8] | [0.1, 0.2] | [4, 5] |
| 48_nM_uH_onnL_omH   | [800, 1000]   | [0.7, 0.8] | [0.1, 0.2] | [6, 8] |
| 49_nM_uH_onnM_omL   | [800, 1000]   | [0.7, 0.8] | [0.3, 0.4] | [2, 3] |
| 50_nM_uH_onnM_omM   | [800, 1000]   | [0.7, 0.8] | [0.3, 0.4] | [4, 5] |
| 51_nM_uH_onnM_omH   | [800, 1000]   | [0.7, 0.8] | [0.3, 0.4] | [6, 8] |
| 52_nM_uH_onnH_omL   | [800, 1000]   | [0.7, 0.8] | [0.5, 0.6] | [2, 3] |
| 53_nM_uH_onnH_omM   | [800, 1000]   | [0.7, 0.8] | [0.5, 0.6] | [4, 5] |
| 54_nM_uH_onnH_omH   | [800, 1000]   | [0.7, 0.8] | [0.5, 0.6] | [6, 8] |
| 55_nH_uL_onnL_omL   | [2000, 5000]  | [0.1, 0.3] | [0.1, 0.2] | [2, 3] |
| 56_nH_uL_onnL_omM   | [2000, 5000]  | [0.1, 0.3] | [0.1, 0.2] | [4, 5] |
| 57_nH_uL_onnL_omH   | [2000, 5000]  | [0.1, 0.3] | [0.1, 0.2] | [6, 8] |
| 58_nH_uL_onnM_omL   | [2000, 5000]  | [0.1, 0.3] | [0.3, 0.4] | [2, 3] |
| 59_nH_uL_onnM_omM   | [2000, 5000]  | [0.1, 0.3] | [0.3, 0.4] | [4, 5] |
| 60_nH_uL_onnM_omH   | [2000, 5000]  | [0.1, 0.3] | [0.3, 0.4] | [6, 8] |
| 61_nH_uL_onnH_omL   | [2000, 5000]  | [0.1, 0.3] | [0.5, 0.6] | [2, 3] |
| 62_nH_uL_onnH_omM   | [2000, 5000]  | [0.1, 0.3] | [0.5, 0.6] | [4, 5] |
| 63_nH_uL_onnH_omH   | [2000, 5000]  | [0.1, 0.3] | [0.5, 0.6] | [6, 8] |
| 64_nH_uM_onnL_omL   | [2000, 5000]  | [0.4, 0.6] | [0.1, 0.2] | [2, 3] |
| 65_nH_uM_onnL_omM   | [2000, 5000]  | [0.4, 0.6] | [0.1, 0.2] | [4, 5] |
| 66_nH_uM_onnL_omH   | [2000, 5000]  | [0.4, 0.6] | [0.1, 0.2] | [6, 8] |
| 67_nH_uM_onnM_omL   | [2000, 5000]  | [0.4, 0.6] | [0.3, 0.4] | [2, 3] |
| 68_nH_uM_onnM_omM   | [2000, 5000]  | [0.4, 0.6] | [0.3, 0.4] | [4, 5] |
| 69_nH_uM_onnM_omH   | [2000, 5000]  | [0.4, 0.6] | [0.3, 0.4] | [6, 8] |
| 70_nH_uM_onnH_omL   | [2000, 5000]  | [0.4, 0.6] | [0.5, 0.6] | [2, 3] |
| 71_nH_uM_onnH_omM   | [2000, 5000]  | [0.4, 0.6] | [0.5, 0.6] | [4, 5] |
| 72_nH_uM_onnH_omH   | [2000, 5000]  | [0.4, 0.6] | [0.5, 0.6] | [6, 8] |
| 73_nH_uH_onnL_omL   | [2000, 5000]  | [0.7, 0.8] | [0.1, 0.2] | [2, 3] |
| 74_nH_uH_onnL_omM   | [2000, 5000]  | [0.7, 0.8] | [0.1, 0.2] | [4, 5] |
| 75_nH_uH_onnL_omH   | [2000, 5000]  | [0.7, 0.8] | [0.1, 0.2] | [6, 8] |
| 76_nH_uH_onnM_omL   | [2000, 5000]  | [0.7, 0.8] | [0.3, 0.4] | [2, 3] |
| 77_nH_uH_onnM_omM   | [2000, 5000]  | [0.7, 0.8] | [0.3, 0.4] | [4, 5] |
| 78_nH_uH_onnM_omH   | [2000, 5000]  | [0.7, 0.8] | [0.3, 0.4] | [6, 8] |
| 79_nH_uH_onnH_omL   | [2000, 5000]  | [0.7, 0.8] | [0.5, 0.6] | [2, 3] |
| 80_nH_uH_onnH_omM   | [2000, 5000]  | [0.7, 0.8] | [0.5, 0.6] | [4, 5] |
| 81_nH_uH_onnH_omH   | [2000, 5000]  | [0.7, 0.8] | [0.5, 0.6] | [6, 8] |
| 82_nVH_uL_onnL_omL  | [6000, 10000] | [0.1, 0.3] | [0.1, 0.2] | [2, 3] |
| 83_nVH_uL_onnL_omM  | [6000, 10000] | [0.1, 0.3] | [0.1, 0.2] | [4, 5] |
| 84_nVH_uL_onnL_omH  | [6000, 10000] | [0.1, 0.3] | [0.1, 0.2] | [6, 8] |
| 85_nVH_uL_onnM_omL  | [6000, 10000] | [0.1, 0.3] | [0.3, 0.4] | [2, 3] |
| 86_nVH_uL_onnM_omM  | [6000, 10000] | [0.1, 0.3] | [0.3, 0.4] | [4, 5] |
| 87_nVH_uL_onnM_omH  | [6000, 10000] | [0.1, 0.3] | [0.3, 0.4] | [6, 8] |
| 88_nVH_uL_onnH_omL  | [6000, 10000] | [0.1, 0.3] | [0.5, 0.6] | [2, 3] |
| 89_nVH_uL_onnH_omM  | [6000, 10000] | [0.1, 0.3] | [0.5, 0.6] | [4, 5] |
| 90_nVH_uL_onnH_omH  | [6000, 10000] | [0.1, 0.3] | [0.5, 0.6] | [6, 8] |
| 91_nVH_uM_onnL_omL  | [6000, 10000] | [0.4, 0.6] | [0.1, 0.2] | [2, 3] |
| 92_nVH_uM_onnL_omM  | [6000, 10000] | [0.4, 0.6] | [0.1, 0.2] | [4, 5] |
| 93_nVH_uM_onnL_omH  | [6000, 10000] | [0.4, 0.6] | [0.1, 0.2] | [6, 8] |
| 94_nVH_uM_onnM_omL  | [6000, 10000] | [0.4, 0.6] | [0.3, 0.4] | [2, 3] |
| 95_nVH_uM_onnM_omM  | [6000, 10000] | [0.4, 0.6] | [0.3, 0.4] | [4, 5] |
| 96_nVH_uM_onnM_omH  | [6000, 10000] | [0.4, 0.6] | [0.3, 0.4] | [6, 8] |
| 97_nVH_uM_onnH_omL  | [6000, 10000] | [0.4, 0.6] | [0.5, 0.6] | [2, 3] |
| 98_nVH_uM_onnH_omM  | [6000, 10000] | [0.4, 0.6] | [0.5, 0.6] | [4, 5] |
| 99_nVH_uM_onnH_omH  | [6000, 10000] | [0.4, 0.6] | [0.5, 0.6] | [6, 8] |
| 100_nVH_uH_onnL_omL | [6000, 10000] | [0.7, 0.8] | [0.1, 0.2] | [2, 3] |
| 101_nVH_uH_onnL_omM | [6000, 10000] | [0.7, 0.8] | [0.1, 0.2] | [4, 5] |
| 102_nVH_uH_onnL_omH | [6000, 10000] | [0.7, 0.8] | [0.1, 0.2] | [6, 8] |
| 103_nVH_uH_onnM_omL | [6000, 10000] | [0.7, 0.8] | [0.3, 0.4] | [2, 3] |
| 104_nVH_uH_onnM_omM | [6000, 10000] | [0.7, 0.8] | [0.3, 0.4] | [4, 5] |
| 105_nVH_uH_onnM_omH | [6000, 10000] | [0.7, 0.8] | [0.3, 0.4] | [6, 8] |
| 106_nVH_uH_onnH_omL | [6000, 10000] | [0.7, 0.8] | [0.5, 0.6] | [2, 3] |
| 107_nVH_uH_onnH_omM | [6000, 10000] | [0.7, 0.8] | [0.5, 0.6] | [4, 5] |
| 108_nVH_uH_onnH_omH | [6000, 10000] | [0.7, 0.8] | [0.5, 0.6] | [6, 8] |

### Networks for Each Network Family

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
- $n$: step 100 or 1000 or 2000
  - L: (500 600 700)
  - M: (800 900 1000)
  - H: (2000 3000 5000)
  - VH: (6000 8000 10000)
- $\mu$: step 0.1 or 0.05
  - L: (0.1 0.2 0.3)
  - M: (0.4 0.5 0.6)
  - H: (0.7 0.75 0.8)
- $o_{n}$/$n$: step 0.1
  - L: (10 20)
  - M: (30 40)
  - H: (50 60)
- $o_{m}$: step 1 or 2
  - L: (2 3)
  - M: (4 5)
  - H: (6 8)
- Instances: 2

**Networks for Each Network Family: 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 72 networks**

**Total Networks: 108 (families) * 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 7776 networks**

**NOTE**: The total number of networks is quite large (7776), which make the computation computationally intensive. Therefore, the 16 base network families from [Report 1](./report1.md) (combinations of L/M for $n$, $\mu$, $o_{n}$/$n$ and $o_m$) are used to ensure robustness in the experiment, and only the necessary network families with larger parameters are computed.

### Reduced Network Families

| Network Family          | $n$           | $\mu$      | $o_{n}$/$n$ | $o_{m}$ |
|-------------------------|---------------|------------|-------------|---------|
| 01_nL_uL_onnL_omL       | [500, 700]    | [0.1, 0.3] | [0.1, 0.2]  | [2, 3]  |
| 02_nL_uL_onnL_omM       | [500, 700]    | [0.1, 0.3] | [0.1, 0.2]  | [4, 5]  |
| 03_nL_uL_onnM_omL       | [500, 700]    | [0.1, 0.3] | [0.3, 0.4]  | [2, 3]  |
| 04_nL_uL_onnM_omM       | [500, 700]    | [0.1, 0.3] | [0.3, 0.4]  | [4, 5]  |
| 05_nL_uM_onnL_omL       | [500, 700]    | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |
| 06_nL_uM_onnL_omM       | [500, 700]    | [0.4, 0.6] | [0.1, 0.2]  | [4, 5]  |
| 07_nL_uM_onnM_omL       | [500, 700]    | [0.4, 0.6] | [0.3, 0.4]  | [2, 3]  |
| 08_nL_uM_onnM_omM       | [500, 700]    | [0.4, 0.6] | [0.3, 0.4]  | [4, 5]  |
| 09_nM_uL_onnL_omL       | [800, 1000]   | [0.1, 0.3] | [0.1, 0.2]  | [2, 3]  |
| 10_nM_uL_onnL_omM       | [800, 1000]   | [0.1, 0.3] | [0.1, 0.2]  | [4, 5]  |
| 11_nM_uL_onnM_omL       | [800, 1000]   | [0.1, 0.3] | [0.3, 0.4]  | [2, 3]  |
| 12_nM_uL_onnM_omM       | [800, 1000]   | [0.1, 0.3] | [0.3, 0.4]  | [4, 5]  |
| 13_nM_uM_onnL_omL       | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |
| 14_nM_uM_onnL_omM       | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2]  | [4, 5]  |
| 15_nM_uM_onnM_omL       | [800, 1000]   | [0.4, 0.6] | [0.3, 0.4]  | [2, 3]  |
| 16_nM_uM_onnM_omM       | [800, 1000]   | [0.4, 0.6] | [0.3, 0.4]  | [4, 5]  |
| 39_nM_uM_onnL_omH       | [800, 1000]   | [0.4, 0.6] | [0.1, 0.2]  | [6, 8]  |
| 43_nM_uM_onnH_omL       | [800, 1000]   | [0.4, 0.6] | [0.5, 0.6]  | [2, 3]  |
| 46_nM_uH_onnL_omL       | [800, 1000]   | [0.7, 0.8] | [0.1, 0.2]  | [2, 3]  |
| ~~64_nH_uM_onnL_omL~~   | [2000, 5000]  | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |
| ~~91_nVH_uM_onnL_omL~~  | [6000, 10000] | [0.4, 0.6] | [0.1, 0.2]  | [2, 3]  |

**Networks for Each Network Family: 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 72 networks**

**Total Networks: 21 (families) * 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 1512 networks**

**NOTE**: The last two network families (64 and 91) are computationally intensive due to their large number of nodes ($n$) and are therefore excluded from the experiment for now.

**Networks for Each Network Family: 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 72 networks**

**Total Networks: 19 (families) * 3 ($n$) * 3 ($\mu$) * 2 ($o_{n}$/$n$) * 2 ($o_{m}$) * 2 (instances) = 1368 networks**



## Experience 5 (LAPIN-off + Extraction of K desired clusters)

[Open Folder](../results/experience5_cluster/results_2026-04-18_11-37-07-535201/)

### Thresholds 

| Network Family    | Selected Metric | Threshold              |
|-------------------|-----------------|------------------------|
| 01_nL_uL_onnL_omL | Median          | 7.131570706178536e-05  |
| 02_nL_uL_onnL_omM | Median          | 6.452183162665591e-05  |
| 03_nL_uL_onnM_omL | Median          | 3.597517130544882e-05  |
| 04_nL_uL_onnM_omM | Median          | 1.8061869999003227e-05 |
| 05_nL_uM_onnL_omL | Median          | 1.7825136109080203e-05 |
| 06_nL_uM_onnL_omM | Median          | 1.4275401255574377e-05 |
| 07_nL_uM_onnM_omL | Median          | 7.19077150618138e-06   |
| 08_nL_uM_onnM_omM | Median          | 3.169941198295696e-06  |
| 09_nM_uL_onnL_omL | Median          | 4.884506224590443e-05  |
| 10_nM_uL_onnL_omM | Median          | 4.015680373336101e-05  |
| 11_nM_uL_onnM_omL | Median          | 1.9732615784769943e-05 |
| 12_nM_uL_onnM_omM | Median          | 7.844071757855867e-06  |
| 13_nM_uM_onnL_omL | Median          | 9.836007762161582e-06  |
| 14_nM_uM_onnL_omM | Median          | 6.934873453732481e-06  |
| 15_nM_uM_onnM_omL | Median          | 3.3096368147017807e-06 |
| 16_nM_uM_onnM_omM | Median          | 1.672976896664927e-06  |
| 39_nM_uM_onnL_omH | Median          | 5.638508927189958e-06  |
| 43_nM_uM_onnH_omL | Median          | 1.3655437454067635e-06 |
| 46_nM_uH_onnL_omL | Median          | 1.5705502911294985e-06 |



## Experience 6 (LAPIN-off + Extraction of clusters until the end)

[Open Folder](../results/experience6_cluster/results_2026-04-25_17-54-35-105243/)

### Thresholds

| Network Family    | Selected Metric | Threshold              |
|-------------------|-----------------|------------------------|
| 01_nL_uL_onnL_omL | Median          | 5.3353016777232356e-05 |
| 02_nL_uL_onnL_omM | Median          | 5.527270873336184e-05  |
| 03_nL_uL_onnM_omL | Median          | 2.690490304442535e-05  |
| 04_nL_uL_onnM_omM | Median          | 1.3983497043349274e-05 |
| 05_nL_uM_onnL_omL | Median          | 5.8928286105116595e-06 |
| 06_nL_uM_onnL_omM | Median          | 7.332702993754699e-06  |
| 07_nL_uM_onnM_omL | Median          | 2.7991218366511875e-06 |
| 08_nL_uM_onnM_omM | Median          | 2.10701450455141e-06   |
| 09_nM_uL_onnL_omL | Median          | 4.033213398067446e-05  |
| 10_nM_uL_onnL_omM | Median          | 3.196001074894147e-05  |
| 11_nM_uL_onnM_omL | Median          | 1.4625381004154202e-05 |
| 12_nM_uL_onnM_omM | Median          | 6.976670015680567e-06  |
| 13_nM_uM_onnL_omL | Median          | 5.688900607855931e-06  |
| 14_nM_uM_onnL_omM | Median          | 4.939332202483173e-06  |
| 15_nM_uM_onnM_omL | Median          | 2.518244987918179e-06  |
| 16_nM_uM_onnM_omM | Median          | 1.376378534048229e-06  |
| 39_nM_uM_onnL_omH | Median          | 4.8468375111567665e-06 |
| 43_nM_uM_onnH_omL | Median          | 1.1942623005433341e-06 |
| 46_nM_uH_onnL_omL | Median          | 4.912281783543144e-07  |



## Experience 7 (LAPIN-on + Extraction of K desired clusters)

[Open Folder](../results/experience7_cluster/results_2026-04-25_20-05-14-328211/)

### Thresholds

| Network Family    | Selected Metric | Threshold              |
|-------------------|-----------------|------------------------|
| 01_nL_uL_onnL_omL | Median          | 8.54072591150887e-05   |
| 02_nL_uL_onnL_omM | Median          | 7.783638353177548e-05  |
| 03_nL_uL_onnM_omL | Median          | 3.992705481071253e-05  |
| 04_nL_uL_onnM_omM | Median          | 2.964651050231931e-05  |
| 05_nL_uM_onnL_omL | Median          | 1.880780206186746e-05  |
| 06_nL_uM_onnL_omM | Median          | 1.2569171467468851e-05 |
| 07_nL_uM_onnM_omL | Median          | 1.031100658696153e-05  |
| 08_nL_uM_onnM_omM | Median          | 4.448279379989367e-06  |
| 09_nM_uL_onnL_omL | Median          | 4.1007015206001445e-05 |
| 10_nM_uL_onnL_omM | Median          | 3.87299688230591e-05   |
| 11_nM_uL_onnM_omL | Median          | 1.6618869423213632e-05 |
| 12_nM_uL_onnM_omM | Median          | 1.3186705265267445e-05 |
| 13_nM_uM_onnL_omL | Median          | 6.906092966372945e-06  |
| 14_nM_uM_onnL_omM | Median          | 4.279168882073914e-06  |
| 15_nM_uM_onnM_omL | Median          | 3.300124021751621e-06  |
| 16_nM_uM_onnM_omM | Median          | 1.6481801384039982e-06 |
| 39_nM_uM_onnL_omH | Median          | 3.4437125125331185e-06 |
| 43_nM_uM_onnH_omL | Median          | 1.5681039929237823e-06 |
| 46_nM_uH_onnL_omL | Median          | 2.771063765186848e-06  |



## Experience 8 (LAPIN-on + Extraction of clusters until the end)

[Open Folder](../results/experience8_cluster/results_2026-04-25_22-23-02-010592/)

### Thresholds

| Network Family    | Selected Metric | Threshold              |
|-------------------|-----------------|------------------------|
| 01_nL_uL_onnL_omL | Median          | 1.4709309158741336e-05 |
| 02_nL_uL_onnL_omM | Median          | 4.31681230914532e-05   |
| 03_nL_uL_onnM_omL | Median          | 1.6602807554414064e-05 |
| 04_nL_uL_onnM_omM | Median          | 2.329059920286411e-05  |
| 05_nL_uM_onnL_omL | Median          | 2.148188332926315e-06  |
| 06_nL_uM_onnL_omM | Median          | 2.252070158372644e-06  |
| 07_nL_uM_onnM_omL | Median          | 1.6805572285539315e-06 |
| 08_nL_uM_onnM_omM | Median          | 2.1605073908487925e-06 |
| 09_nM_uL_onnL_omL | Median          | 2.025730812729182e-05  |
| 10_nM_uL_onnL_omM | Median          | 2.285632463928619e-05  |
| 11_nM_uL_onnM_omL | Median          | 9.222547654010063e-06  |
| 12_nM_uL_onnM_omM | Median          | 1.1976657667071576e-05 |
| 13_nM_uM_onnL_omL | Median          | 2.0513948237377787e-06 |
| 14_nM_uM_onnL_omM | Median          | 2.207547290125855e-06  |
| 15_nM_uM_onnM_omL | Median          | 1.4807924756032774e-06 |
| 16_nM_uM_onnM_omM | Median          | 1.5371305372157242e-06 |
| 39_nM_uM_onnL_omH | Median          | 2.6718167104796284e-06 |
| 43_nM_uM_onnH_omL | Median          | 1.0565510582107734e-06 |
| 46_nM_uH_onnL_omL | Median          | 6.224030661783513e-07  |



## Discussion

- **Observations**
  - The median was always the most stable and robust measure across all experiments, even in larger parameter values;
  - The same order of magnitude was observed between network families within the same experiment and across experiments (`10^-5`, `10^-6`, `10^-7`).

- **Warnings**
  - Different normalizations are used across Stage 1 and Stage 2.

- **TODO**
  - Change $u$ to $\mu$ in network family names;
  - Change numeration in network family names.
