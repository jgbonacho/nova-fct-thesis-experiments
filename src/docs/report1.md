# Report 1 - Question: Does the relative contribution to data scatter provide a good hyperparameter for the definition of the stop rules under variations in the structure/architecture parameters of LFR synthetic networks?

---

## LFR Network Parameterization

- $\overline{d}$ = 20
- $d_{max}$ = 50
- $c_{min}$ = 20
- $c_{max}$ = 100
- $t1$ = -2
- $t2$ = -1
- $n$ (3 groups):
  - L: [200, 400] (*[1000, 3000])
  - M: [500, 700] (*[4000, 6000])
  - H: [800, 1000] (*[7000, 10000])
- $\mu$ (2 groups) (*3 groups):
  - L: [0.1, 0.4]
  - H: [0.5, 0.8]
- $o_{n}$ / $n$ (2 groups) (*3 groups):
  - L: [0.1, 0.3]
  - H: [0.4, 0.6]
- $o_{m}$ (2 groups) (*3 groups):
  - L: [2, 4]
  - H: [5, 8]

## Network Families

| Network Family    | $n$         | $\mu$      | $o_{n}$/$n$  | $o_{m}$  |
|-------------------|-------------|------------|--------------|----------|
| 1_nL_uL_onnL_omL  | [200, 400]  | [0.1, 0.4] | [0.1, 0.3]   | [2, 4]   |
| 2_nL_uL_onnL_omH  | [200, 400]  | [0.1, 0.4] | [0.1, 0.3]   | [5, 8]   |
| 3_nL_uL_onnH_omL  | [200, 400]  | [0.1, 0.4] | [0.4, 0.6]   | [2, 4]   |
| 4_nL_uL_onnH_omH  | [200, 400]  | [0.1, 0.4] | [0.4, 0.6]   | [5, 8]   |
| 5_nL_uH_onnL_omL  | [200, 400]  | [0.5, 0.8] | [0.1, 0.3]   | [2, 4]   |
| 6_nL_uH_onnL_omH  | [200, 400]  | [0.5, 0.8] | [0.1, 0.3]   | [5, 8]   |
| 7_nL_uH_onnH_omL  | [200, 400]  | [0.5, 0.8] | [0.4, 0.6]   | [2, 4]   |
| 8_nL_uH_onnH_omH  | [200, 400]  | [0.5, 0.8] | [0.4, 0.6]   | [5, 8]   |
| 9_nM_uL_onnL_omL  | [500, 700]  | [0.1, 0.4] | [0.1, 0.3]   | [2, 4]   |
| 10_nM_uL_onnL_omH | [500, 700]  | [0.1, 0.4] | [0.1, 0.3]   | [5, 8]   |
| 11_nM_uL_onnH_omL | [500, 700]  | [0.1, 0.4] | [0.4, 0.6]   | [2, 4]   |
| 12_nM_uL_onnH_omH | [500, 700]  | [0.1, 0.4] | [0.4, 0.6]   | [5, 8]   |
| 13_nM_uH_onnL_omL | [500, 700]  | [0.5, 0.8] | [0.1, 0.3]   | [2, 4]   |
| 14_nM_uH_onnL_omH | [500, 700]  | [0.5, 0.8] | [0.1, 0.3]   | [5, 8]   |
| 15_nM_uH_onnH_omL | [500, 700]  | [0.5, 0.8] | [0.4, 0.6]   | [2, 4]   |
| 16_nM_uH_onnH_omH | [500, 700]  | [0.5, 0.8] | [0.4, 0.6]   | [5, 8]   |
| 17_nH_uL_onnL_omL | [800, 1000] | [0.1, 0.4] | [0.1, 0.3]   | [2, 4]   |
| 18_nH_uL_onnL_omH | [800, 1000] | [0.1, 0.4] | [0.1, 0.3]   | [5, 8]   |
| 19_nH_uL_onnH_omL | [800, 1000] | [0.1, 0.4] | [0.4, 0.6]   | [2, 4]   |
| 20_nH_uL_onnH_omH | [800, 1000] | [0.1, 0.4] | [0.4, 0.6]   | [5, 8]   |
| 21_nH_uH_onnL_omL | [800, 1000] | [0.5, 0.8] | [0.1, 0.3]   | [2, 4]   |
| 22_nH_uH_onnL_omH | [800, 1000] | [0.5, 0.8] | [0.1, 0.3]   | [5, 8]   |
| 23_nH_uH_onnH_omL | [800, 1000] | [0.5, 0.8] | [0.4, 0.6]   | [2, 4]   |
| 24_nH_uH_onnH_omH | [800, 1000] | [0.5, 0.8] | [0.4, 0.6]   | [5, 8]   |

## Networks for Each Network Family

- $\overline{d}$: fixed
- $d_{max}$: fixed
- $c_{min}$: fixed
- $c_{max}$: fixed
- $t1$: fixed
- $t2$: fixed
- $n$: step 200 (*100)
- $\mu$: step 0.3 (*0.1)
- $o_{n}$/$n$: step 0.2 (*0.1)
- $o_{m}$: step 2 or 3 (*1)
- Instances: 1 (*10)

---

## Experience 1

## Experience 2

## Experience 3

## Experience 4