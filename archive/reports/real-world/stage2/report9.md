# Report 9 - Fine-Tuned Experimental Protocol for FADDIS Threshold Selection


## Table of Contents

- [(1) Network Selection and Division](#1-network-selection-and-division)
  - [Train Networks](#train-networks)
  - [Test Networks](#test-networks)
- [(2) Observations from Stage 1](#2-observations-from-stage-1)
- [(3) FADDIS Sensitivity Analysis](#3-faddis-sensitivity-analysis)
  - [Network Properties](#network-properties)
  - [Ground-Truth Properties](#ground-truth-properties)
  - [FADDIS Correlations](#faddis-correlations)
  - [Degree Assortativity (Primary)](#degree-assortativity-primary)
  - [Average Degree (Secondary)](#average-degree-secondary)
- [(4) Real-World Network Families](#4-real-world-network-families)
  - [Combinations](#combinations)
  - [Train Assignment](#train-assignment)
  - [Test Assignment](#test-assignment)
- [(5) Pipeline Configuration](#5-pipeline-configuration)
- [(6) Pipeline](#6-pipeline)
- [(7) Non-overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#7-non-overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(8) Overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#8-overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(9) Discussion](#9-discussion)


## (1) Network Selection and Division

- `Networks with reasonable meta-data or informal labels to be considered ground-truth`
- Networks pre-processed to **undirected, unweighted simple graphs without self-loops**, saved as .gml files.
- **26 small- to medium-size networks**:
    - 9 networks with non-overlapping ground-truth: **7 train + 2 test**
    - 10 networks with overlapping ground-truth: **7 train + 3 test**
    - 7 networks without ground-truth: **7 test**

### Train Networks

| Network                                                                                                                                    | Knowledge Domain                  | Ground-Truth? | Nodes | Edges | CC  | Nodes LCC | Edges LCC | Relative Size LCC | Overlapping Ground-Truth? | K LCC  | Set   |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|---------------|-------|-------|-----|-----------|-----------|-------------------|---------------------------|--------|-------|
| Zachary Karate Club [[1](https://networkx.org/documentation/stable/reference/generated/networkx.generators.social.karate_club_graph.html)] | Human Social                      | Yes           | 34    | 78    | 1   | 34        | 78        | 1.0000            | No                        | 2      | Train |
| Books about US Politics [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                   | Co-purchase                       | Yes           | 105   | 441   | 1   | 105       | 441       | 1.0000            | No                        | 3      | Train |
| American College Football [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                 | Sports                            | Yes           | 115   | 613   | 1   | 115       | 613       | 1.0000            | No                        | 12     | Train |
| SocioPatterns Primary School day 1 [[3](https://sociopatterns.org/datasets/primary-school-cumulative-networks/)]                           | Human Contact                     | Yes           | 236   | 5899  | 1   | 236       | 5899      | 1.0000            | No                        | 11     | Train |
| E-mail EU Core [[4](https://snap.stanford.edu/data/email-Eu-core.html/)]                                                                   | Communication                     | Yes           | 1005  | 16064 | 20  | 986       | 16064     | 0.9811            | No                        | 42     | Train |
| US Political Blogs [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                        | Web / Hyperlink                   | Yes           | 1490  | 16715 | 268 | 1222      | 16714     | 0.8201            | No                        | 2      | Train |
| Cora [[5](https://web.archive.org/web/20151007064508/http://linqs.cs.umd.edu/projects/projects/lbc/)]                                      | Scientific Citation               | Yes           | 2708  | 5278  | 78  | 2485      | 5069      | 0.9177            | No                        | 7      | Train |
| Facebook Ego-698 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 61    | 270   | 3   | 40        | 220       | 0.6557            | Yes                       | 9      | Train |
| Facebook Ego-414 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 150   | 1693  | 2   | 148       | 1692      | 0.9867            | Yes                       | 7      | Train |
| Facebook Ego-0 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                         | Online Social                     | Yes           | 333   | 2519  | 5   | 324       | 2514      | 0.9730            | Yes                       | 22     | Train |
| Facebook Ego-3437 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 534   | 4813  | 2   | 532       | 4812      | 0.9963            | Yes                       | 32     | Train |
| Facebook Ego-1684 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 786   | 14024 | 4   | 775       | 14006     | 0.9860            | Yes                       | 17     | Train |
| Facebook Ego-1912 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 747   | 30025 | 2   | 744       | 30023     | 0.9960            | Yes                       | 45     | Train |
| Facebook Ego-107 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 1034  | 26749 | 1   | 1034      | 26749     | 1.0000            | Yes                       | 9      | Train |

### Test Networks

| Network                                                                                                                                    | Knowledge Domain                  | Ground-Truth? | Nodes | Edges | CC  | Nodes LCC | Edges LCC | Relative Size LCC | Overlapping Ground-Truth? | K LCC  | Set   |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|---------------|-------|-------|-----|-----------|-----------|-------------------|---------------------------|--------|-------|
| SocioPatterns Primary School day 2 [[3](https://sociopatterns.org/datasets/primary-school-cumulative-networks/)]                           | Human Contact                     | Yes           | 238   | 5539  | 1   | 238       | 5539      | 1.0000            | No                        | 11     | Test  |
| CiteSeer [[5](https://web.archive.org/web/20151007064508/http://linqs.cs.umd.edu/projects/projects/lbc/)]                                  | Scientific Citation               | Yes           | 3312  | 4536  | 438 | 2110      | 3668      | 0.6371            | No                        | 6      | Test  |
| Facebook Ego-3980 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 52    | 146   | 4   | 44        | 138       | 0.8462            | Yes                       | 11     | Test  |
| Facebook Ego-686 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 168   | 1656  | 1   | 168       | 1656      | 1.0000            | Yes                       | 14     | Test  |
| Facebook Ego-348 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 224   | 3192  | 1   | 224       | 3192      | 1.0000            | Yes                       | 14     | Test  |
| Dolphins [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                                  | Geographic                        | No            | 62    | 159   | 1   | 62        | 159       | 1.0000            | -                         | -      | Test  |
| Les Miserables [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                            | Character                         | No            | 77    | 254   | 1   | 77        | 254       | 1.0000            | -                         | -      | Test  |
| Jazz Musicians [[7](https://alephsyslab.com/data/)]                                                                                        | Human Social                      | No            | 198   | 2742  | 1   | 198       | 2742      | 1.0000            | -                         | -      | Test  |
| C.Elegans Neural Network [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                  | Neural                            | No            | 297   | 2148  | 1   | 297       | 2148      | 1.0000            | -                         | -      | Test  |
| C.Elegans Metabolic [[7](https://alephsyslab.com/data/)]                                                                                   | Metabolic                         | No            | 453   | 2025  | 1   | 453       | 2025      | 1.0000            | -                         | -      | Test  |
| E-mail URV [[7](https://alephsyslab.com/data/)]                                                                                            | Communication                     | No            | 1133  | 5451  | 1   | 1133      | 5451      | 1.0000            | -                         | -      | Test  |
| Co-authorships in Network Science [[2](https://websites.umich.edu/~mejn/netdata/)]                                                         | Co-authorship                     | No            | 1589  | 2742  | 396 | 379       | 914       | 0.2385            | -                         | -      | Test  |


## (2) Observations from Stage 1

- `The LFR network threshold estimation pipeline is not applicable due to the limited network sample size, the varying number of networks per family and the quality of the metadata or informal labels, which cannot be automatically treated as ground truth`
- `LAPIN-on allows the ground-truth number of communities, K, to be extracted for all considered training networks`
- `Overall, using the adjacency matrix as the affinity matrix and K as the FADDIS stopping criterion, LAPIN-on achieves better results:`
  - `LAPIN-on:`
    - `books-about-us-politics`
    - `cora`
    - `facebook-network-ego698`
    - `email-eu-core`
    - `facebook-network-ego0`
    - `facebook-network-ego414`
    - `facebook-network-ego3437`
    - `facebook-network-ego107`
    - `facebook-network-ego1684`
  - `LAPIN-off:`
	  - `[CRITICAL] us-political-blogs`
	  - `american-college-football`
  - `LAPIN-on/LAPIN-off:`
	  - `zachary-karate-club`


## (3) FADDIS Sensitivity Analysis

- `FADDIS sensitivity analysis is necessary to select the properties used to form network families, unlike LFR networks, which leverage prior knowledge from the literature`

### Network Properties

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/train_networks/network_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/test_networks_with_gt/network_properties.csv)
- [Test networks without ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/test_networks_without_gt/network_properties.csv)

### Ground-Truth Properties

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/train_networks/ground_truth_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/test_networks_with_gt/ground_truth_properties.csv)

### FADDIS Correlations

- [Open File](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-17_20-30-20-156374/train_networks/faddis_sensitivity_analysis.csv)

| Ground-Truth Type               | Network Property              | FADDIS Property | #Networks | Spearman Correlation | Pearson Correlation   |
|---------------------------------|-------------------------------|-----------------|-----------|----------------------|-----------------------|
| Non-overlapping and Overlapping | Degree Assortativity          | c_K             | 14        | -0.7714285714285714  | -0.8034827735356096   |
| Non-overlapping and Overlapping | Global Clustering Coefficient | c_K             | 14        | -0.6571428571428571  | -0.4831986256048038   |
| Non-overlapping and Overlapping | Average Degree                | c_K             | 14        | -0.5076923076923077  | -0.33647598856874567  |
|                                 |                               |                 |           |                      |                       |
| Non-overlapping                 | Degree Assortativity          | c_K             | 7         | -0.8928571428571429  | -0.9320192285277448   |
| Non-overlapping                 | Average Degree                | c_K             | 7         | -0.6071428571428572  | -0.3905267946976315   |
| Non-overlapping                 | Global Clustering Coefficient | c_K             | 7         | -0.5                 | -0.28510872178519103  |
|                                 |                               |                 |           |                      |                       |
| Overlapping                     | Degree Std                    | c_K             | 7         | -0.39285714285714296 | 0.3732117066714181    |
| Overlapping                     | Degree Assortativity          | c_K             | 7         | -0.3571428571428572  | 0.3291663269624444    |
| Overlapping                     | Edges LCC                     | c_K             | 7         | -0.28571428571428575 | 0.506706819950832     |
| Overlapping                     | Max Degree                    | c_K             | 7         | -0.28571428571428575 | 0.47484800717282394   |
| Overlapping                     | Average Degree                | c_K             | 7         | -0.25                | 0.2769450057885224    |
| Overlapping                     | Average Clustering            | c_K             | 7         | 0.25                 | -0.24390718101017886  |
| Overlapping                     | Degree CV                     | c_K             | 7         | -0.14285714285714288 | 0.3072484116685966    |
| Overlapping                     | Density                       | c_K             | 7         | 0.14285714285714288  | -0.20713915216920017  |
| Overlapping                     | Sparsity                      | c_K             | 7         | -0.14285714285714288 | 0.20713915216920015   |
| Overlapping                     | Degree Hub Ratio              | c_K             | 7         | 0.03571428571428572  | 0.2753442257892939    |
| Overlapping                     | Nodes LCC                     | c_K             | 7         | 0.0                  | 0.5956963447712103    |
| Overlapping                     | Global Clustering Coefficient | c_K             | 7         | 0.0                  | -0.14814982050285025  |

- `Only network properties are considered in sensitivity correlations, rather than ground-truth properties, because they are available for all networks`
- `Degree assortativity is clearly the network property most strongly correlated with c_K for the combined and non-overlapping ground-truth groups`
- `Average degree exhibits a balanced correlated with c_K for the combined, non-overlapping and overlapping ground-truth groups`

### Degree Assortativity (Primary)

| Category       | Empirical Range     | Group      |
|----------------|---------------------|------------|
| Disassortative | $a < -0.10$         | Low (L)    |
| Near-Neutral   | $-0.10 <= a < 0.10$ | Medium (M) |
| Assortative    | $a >= 0.10$         | High (H)   |

### Average Degree (Secondary)

| Category                  | Empirical Range    | Group          |
|---------------------------|--------------------|----------------|
| Low Average Degree        | $d_{avg} < 15$        | Low (L)        |
| Medium Average Degree     | $15 <= d_{avg} < 35$  | Medium (M)     |
| Large Average Degree      | $35 <= d_{avg} < 65$  | High (H)       |
| Very Large Average Degree | $d_{avg} >= 65$       | Very High (VH) |


## (4) Real-World Network Families

### Combinations

| Network Family | Degree Assortativity Range | Average Degree Range       | Combination                                    | Calibrated? |
|----------------|----------------------------|----------------------------|------------------------------------------------|-------------|
| 01_aL_davgL    | $a < -0.10$                | $d_{avg} < 15$             | Disassortative + Low Average Degree            | Yes         |
| 02_aL_davgM    | $a < -0.10$                | $15 <= d_{avg} < 35$       | Disassortative + Medium Average Degree         | Yes         |
| 03_aL_davgH    | $a < -0.10$                | $35 <= d_{avg} < 65$       | Disassortative + Large Average Degree          | No          |
| 04_aL_davgVH   | $a < -0.10$                | $d_{avg} >= 65$            | Disassortative + Very Large Average Degree     | No          |
| 05_aM_davgL    | $-0.10 <= a < 0.10$        | $d_{avg} < 15$             | Near-Neutral + Low Average Degree              | Yes         |
| 06_aM_davgM    | $-0.10 <= a < 0.10$        | $15 <= d_{avg} < 35$       | Near-Neutral + Medium Average Degree           | Yes         |
| 07_aM_davgH    | $-0.10 <= a < 0.10$        | $35 <= d_{avg} < 65$       | Near-Neutral + Large Average Degree            | No          |
| 08_aM_davgVH   | $-0.10 <= a < 0.10$        | $d_{avg} >= 65$            | Near-Neutral + Very Large Average Degree       | No          |
| 09_aH_davgL    | $a >= 0.10$                | $d_{avg} < 15$             | Assortative + Low Average Degree               | Yes         |
| 10_aH_davgM    | $a >= 0.10$                | $15 <= d_{avg} < 35$       | Assortative + Medium Average Degree            | Yes         |
| 11_aH_davgH    | $a >= 0.10$                | $35 <= d_{avg} < 65$       | Assortative + Large Average Degree             | Yes         |
| 12_aH_davgVH   | $a >= 0.10$                | $d_{avg} >= 65$            | Assortative + Very Large Average Degree        | Yes         |

### Train Assignment

| Network                            | Average Degree | Degree Assortativity | Combination                             | Assigned Family   | Set   |
|------------------------------------|----------------|----------------------|-----------------------------------------|-------------------|-------|
| zachary-karate-club                | 4.5882         | -0.4756              | Disassortative + Low Average Degree     | 01_aL_davgL       | Train |
| books-about-us-politics            | 8.4000         | -0.1279              | Disassortative + Low Average Degree     | 01_aL_davgL       | Train |
| us-political-blogs                 | 27.3552        | -0.2213              | Disassortative + Medium Average Degree  | 02_aL_davgM       | Train |
| cora                               | 4.0797         | -0.0714              | Near-Neutral + Low Average Degree       | 05_aM_davgL       | Train |
| facebook-network-ego698            | 11.0000        | 0.0125               | Near-Neutral + Low Average Degree       | 05_aM_davgL       | Train |
| email-eu-core                      | 32.5842        | -0.0257              | Near-Neutral + Medium Average Degree    | 06_aM_davgM       | Train |
| american-college-football          | 10.6609        | 0.1624               | Assortative + Low Average Degree        | 09_aH_davgL       | Train |
| facebook-network-ego0              | 15.5185        | 0.2330               | Assortative + Medium Average Degree     | 10_aH_davgM       | Train |
| facebook-network-ego3437           | 18.0902        | 0.2221               | Assortative + Medium Average Degree     | 10_aH_davgM       | Train |
| facebook-network-ego414            | 22.8649        | 0.3039               | Assortative + Medium Average Degree     | 10_aH_davgM       | Train |
| facebook-network-ego1684           | 36.1445        | 0.3268               | Assortative + Large Average Degree      | 11_aH_davgH       | Train |
| socio-patterns-primary-school-day1 | 49.9915        | 0.1729               | Assortative + Large Average Degree      | 11_aH_davgH       | Train |
| facebook-network-ego107            | 51.7389        | 0.4316               | Assortative + Large Average Degree      | 11_aH_davgH       | Train |
| facebook-network-ego1912           | 80.7070        | 0.5026               | Assortative + Very Large Average Degree | 12_aH_davgVH      | Train |

### Test Assignment

| Network                              | Average Degree | Degree Assortativity | Combination                                | Assigned Family | Calibrated? |
|--------------------------------------|---------------:|---------------------:|--------------------------------------------|-----------------|-------------|
| socio-patterns-primary-school-day2   |        46.5462 |               0.2168 | Assortative + Large Average Degree         | 11_aH_davgH     | Yes         |
| citeseer                             |         3.4768 |               0.0071 | Near-Neutral + Low Average Degree          | 05_aM_davgL     | Yes         |
| facebook-network-ego3980             |         6.2727 |               0.0530 | Near-Neutral + Low Average Degree          | 05_aM_davgL     | Yes         |
| facebook-network-ego686              |        19.7143 |               0.0841 | Near-Neutral + Medium Average Degree       | 06_aM_davgM     | Yes         |
| facebook-network-ego348              |        28.5000 |               0.2227 | Assortative + Medium Average Degree        | 10_aH_davgM     | Yes         |
| dolphins                             |         5.1290 |              -0.0436 | Near-Neutral + Low Average Degree          | 05_aM_davgL     | Yes         |
| les-miserables                       |         6.5974 |              -0.1652 | Disassortative + Low Average Degree        | 01_aL_davgL     | Yes         |
| jazz-musicians                       |        27.6970 |               0.0202 | Near-Neutral + Medium Average Degree       | 06_aM_davgM     | Yes         |
| c-elegans-neural-network             |        14.4646 |              -0.1632 | Disassortative + Low Average Degree        | 01_aL_davgL     | Yes         |
| c-elegans-metabolic                  |         8.9404 |              -0.2258 | Disassortative + Low Average Degree        | 01_aL_davgL     | Yes         |
| email-urv                            |         9.6222 |               0.0782 | Near-Neutral + Low Average Degree          | 05_aM_davgL     | Yes         |
| co-authorships-in-network-science    |         4.8232 |              -0.0817 | Near-Neutral + Low Average Degree          | 05_aM_davgL     | Yes         |


---
---
---


## (5) Pipeline Configuration

```json
{
  "apply_lapin": true,
  "tau": 0.05,
  "k_max_boundary": 500,
  "overlapping_communities": false,
  "defuzzification_gamma": 0.8,
  "number_of_thresholds_to_retain_after_intrinsic_evaluation": 3,
  "number_of_thresholds_to_retain_after_stability_evaluation": 2,
  "near_singleton_boundary": 2,
  "number_of_perturbed_graphs": 10,
  "fraction_of_edges_swaps_in_perturbed_graphs": 0.05,
  "number_of_null_models": 10,
  "fraction_of_edges_swaps_in_null_models": 10,
  "pareto_tolerance_fraction_modularity": 0.10,
  "pareto_tolerance_fraction_conductance": 0.10,
  "pareto_tolerance_fraction_stability": 0.10,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.10,
  "pareto_null_model_rank_boundary": 2,
  "pareto_null_model_z_score_boundary": 1.645
}
```

## (6) Pipeline

### Stage 1: Network Family K-Boundary Thresholds

- For each network:
  - $c_{K}$ = $c_{K}$ if `apply_lapin` else $c_{K+1}$
  - $c_{K+1}$ = $c_{K+1}$ if `apply_lapin` else $c_{K+2}$
  - Valid Threshold? $c_{K}$ > $c_{K+1}$ 
  - Threshold = $\sqrt{c_{K}c_{K+1}}$
- For each network family:
  - $e_{family}$ = median(valid_thresholds)
  - $e_{global}$ = median(all_valid_thresholds)

### Stage 2: Network Contribution-Boundary Thresholds

#### Stage 2.1: Candidate Thresholds

- For each network:
  - $\epsilon_{family}$
  - $\epsilon_{global}$
  - $\epsilon_{below}$ = max(below_thresholds)
  - $\epsilon_{above}$ = min(above_thresholds)
  - $\epsilon_{elbow}$ = max(adjacent_drops)

#### Stage 2.2: Intrinsic Evaluation -> `number_of_thresholds_to_retain_after_intrinsic_evaluation` + [$\epsilon_{family}$]

- For each network and threshold $\epsilon$:
  - **Modularity** ($Q$):
    - Modularity if not `overlapping_communities`
    - Fuzzy-Modularity if `overlapping_communities`
  - **Conductance** ($\phi$):
    - Conductance if not `overlapping_communities`
    - Conductance-BN if `overlapping_communities`
  - **Runtime FADDIS**
  - **K'**
  - **Overlapping Communities**
  - **Community Size Distribution**
  - **#Singleton/Near-Singleton Communities** = [community_size <= `near_singleton_boundary`]
  - **Singleton/Near-Singleton Fraction** = $\frac{\#Singleton/Near-Singleton Communities}{K'}$
  - **Largest Community Fraction** = $\frac{max(community\_size)}{n}$

#### Stage 2.3: Stability Evaluation -> `number_of_thresholds_to_retain_after_stability_evaluation` + [$e_{family}$]

- For each network and threshold $\epsilon$:
  - **#Pertubed Graphs** = `number_of_perturbed_graphs` => `fraction_of_edges_swaps_in_perturbed_graphs`*e
  - **#Valid Similarities ($B$)** [!0/1 extracted communities]
  - **Similarities** ($\times$ `number_of_perturbed_graphs`):
    - Sim = NMI if not `overlapping_communities` 
    - Sim = Fuzzy co-Memberships Similarities if `overlapping_communities`
  - **Stability** = $\frac{1}{B} \sum_{b=1}^{B} \mathrm{Sim} \!\left(C_{\epsilon}(G_i),C_{\epsilon}\!\left(G_i^{(b)}\right)\right)$

#### Stage 2.5: Null Model Diagnostic

- For each network and threshold $\epsilon$:
  - **#Null Graphs** = `number_of_null_models` => `fraction_of_edges_swaps_in_null_models`*e
  - **#Valid Null Modularities and Conductances** ($R$) [!0/1 extracted communities]
  - **Null Modularities** ($\times$ `number_of_null_models`)
  - **Mean Null Modularities** ($\mu$)
  - **Std Null Modularities** ($\sigma$)
  - **Modularity Z Score** = $ \frac{Q_{\mathrm{real}}(\epsilon)-\mu\!\left(Q_{\mathrm{null}}(\epsilon)\right)}{\sigma\!\left(Q_{\mathrm{null}}(\epsilon)\right)}$
  - **Modularity Empirical p-value** = $\frac{1 + \sum_{r=1}^{R} \mathbf{1} \!\left(Q_{\mathrm{null}}^{(r)}(\epsilon) \ge Q_{\mathrm{real}}(\epsilon) \right) }{R+1}$
  - **Modularity Rank** = $1 + \sum_{r=1}^{R} \mathbf{1} \!\left(Q_{\mathrm{null}}^{(r)}(\epsilon) > Q_{\mathrm{real}}(\epsilon) \right)$
  - **Null Conductances**
  - **Mean Null Conductances**
  - **Std Null Conductances**
  - **Conductance Z Score**
  - **Conductance Empirical p-value**
  - **Conductance Rank**

#### Stage 2.6: Pareto-based Filtering and Parsimony

- For each network:

$$
\mathcal{A}_i
=
\left\{
\epsilon \in E_i :
Q(\epsilon) \geq Q_{\max}-\delta_Q,\;
\phi(\epsilon) \leq \phi_{\min}+\delta_{\phi},\;
S(\epsilon) \geq S_{\max}-\delta_S,\;
\epsilon \text{ is non-degenerate},\;
\epsilon \text{ passes the null-model evaluation}
\right\}
$$

$$
\epsilon_i^{*}
=
\max \left\{
\epsilon : \epsilon \in \mathcal{A}_i
\right\}
$$

- **Acceptable**:
  - **Acceptable Modularity** (high modularity or fuzzy modularity):
    - $Q(\epsilon) \geq Q_{\max}-\delta_Q$
      - $Q_{\max}=\max(Q(\epsilon))$
      - $\delta_Q=$ `pareto_tolerance_fraction_modularity` $\times (Q_{\max}-Q_{\min})$
  - **Acceptable Conductance** (low conductance or boundary-node conductance):
    - $\phi(\epsilon) \leq \phi_{\min}+\delta_{\phi}$
        - $\phi_{\min}=\min(\phi(\epsilon))$
        - $\delta_{\phi}=$ `pareto_tolerance_fraction_conductance` $\times (\phi_{\max}-\phi_{\min})$
  - **Acceptable Stability** (high perturbation stability):
    - $S(\epsilon) \geq S_{\max}-\delta_S$
      - $S_{\max}=\max(S(\epsilon))$
      - $\delta_S=$ `pareto_tolerance_fraction_stability` $\times (S_{\max}-S_{\min})$
  - **Acceptable Non-degenerate** (non-degenerate K' and non-degenerate community-size distribution):
    - K' $>$ 1 $\land$ 
    Largest Community Fraction $<$ `pareto_largest_community_fraction_boundary` $\land$ 
    Singleton/Near-Singleton Fraction $<$ `pareto_singleton_or_near_singleton_fraction_boundary`
  - **Acceptable Null Model** (favourable, or at least non-poor, null-model evidence):
    - Modularity Z Score >= `pareto_null_model_z_score_boundary` $\land$ 
    Modularity Empirical p-value <= `pareto_null_model_p_value_boundary` $\land$  
    Modularity Rank <= `pareto_null_model_rank_boundary` $\land$
    Conductance Z Score >= `pareto_null_model_z_score_boundary` $\land$ 
    Conductance Empirical p-value <= `pareto_null_model_p_value_boundary` $\land$  
    Conductance Rank <= `pareto_null_model_rank_boundary`

- **Internal selection** [<= 5 candidates] --> **Intrinsic Evaluation** --> [<= 3 candidates (+1)] --> **Stability Evaluation** --> [<= 2 candidates (+1)] --> **Null Model Diagnostic** --> **Pareto-based Filtering and Parsimony**
  - **Intrinsic Evaluation**
    - *Evaluate*: Acceptable Modularity; Acceptable Conductance; Acceptable Non-degenerate
    - *Filter*: Parsimony Principle (Top-3) over Acceptables
      - *Fallback*: Non-degenerate; Highest Modularity; Lowest Conductance;
  - **Stability Evaluation**
    - *Evaluate*: Acceptable Stability
    - *Filter*: Parsimony Principle (Top-2) over Acceptables
      - *Fallback*: Non-degenerate; Highest Modularity; Lowest Conductance; Highest Stability
  - **Null Model Diagnostic**
    - *Evaluate*: Acceptable Null Model
  - **Pareto-based Filtering and Parsimony**
    - *Select*: Parsimony Principle over Acceptables
      - *Fallback*: Parsimony Principle over Non-Acceptables

#### Stage 2.7: Extrinsic Evaluation

- For each network with ground-truth and final threshold $\epsilon$:
  - K' | K, |K'-K|/K, AMI, F-measure, ARI, FMI, NMI, VI if not network.overlapping_ground_truth
  - K' | K, |K'-K|/K, ONMI, Omega if network.overlapping_ground_truth


## (7) Non-overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

TODO


## (8) Overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

TODO


## (9) Discussion
