# Report 8 - New Experimental Protocol for FADDIS Threshold Selection


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
- [(5) Experience 1 (V1) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#5-experience-1-v1---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(6) Experience 2 (V1 + Tolerance Values) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#6-experience-2-v1--tolerance-values---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(7) Experience 3 (V1 + Overlapping Communities) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#7-experience-3-v1--overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(8) Experience 4 (V2) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#8-experience-4-v2---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(9) Experience 5 (V2 + Tolerance Values) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#9-experience-5-v2--tolerance-values---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
- [(10) Experience 6 (V2 + Overlapping Communities) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#10-experience-6-v2--overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)


## (1) Network Selection and Division

- `Reasonable meta-data or informal labels to be considered ground-truth`
- Networks pre-processed to **undirected, unweighted simple graphs without self-loops**, saved as .gml files.
- **26 small- to medium-size networks**:
    - 9 networks with non-overlapping ground-truth: **7 train + 2 test**
    - 10 networks with overlapping ground-truth: **7 train + 3 test**
    - 7 networks without ground-truth: **7 test**
- **2 large networks**:
    - LASTFM Asia (with ground-truth) [[8](https://archive.ics.uci.edu/dataset/595/lastfm+asia+social+network)]
    - US Power Grid (without ground-truth) [[2](https://websites.umich.edu/~mejn/netdata/)]

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
- `LAPIN-on allows the ground-truth number of communities, K, to be extracted for all considered networks`
- `Overall, using the adjacency matrix as the affinity matrix and K as the FADDIS stopping criterion achieves better results`


## (3) FADDIS Sensitivity Analysis

- `FADDIS sensitivity analysis is necessary to select the properties used to form network families, unlike LFR networks, which leverage prior knowledge from the literature`

### Network Properties

- [Train networks](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/train_networks/network_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/test_networks_with_gt/network_properties.csv)
- [Test networks without ground-truth](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/test_networks_without_gt/network_properties.csv)

### Ground-Truth Properties

- [Train networks](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/train_networks/ground_truth_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/test_networks_with_gt/ground_truth_properties.csv)

### FADDIS Correlations

- [Open File](../../../results/real-world/stage2/results_2026-07-12_22-54-20-144373/train_networks/faddis_sensitivity_analysis.csv)

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

- `Only network properties are considered, rather than ground-truth properties, because they are available for all networks`
- `Degree assortativity is clearly the network property most strongly correlated with (c_K) for the combined and non-overlapping ground-truth groups`
- `Average degree exhibits a balanced correlated with (c_K) for the combined, non-overlapping and overlapping ground-truth groups`

### Degree Assortativity (Primary)

| Category       | Empirical Range         | Group      |
|----------------|-------------------------|------------|
| Disassortative | \(r < -0.10\)           | Low (L)    |
| Near-Neutral   | \(-0.10 \leq r < 0.10\) | Medium (M) |
| Assortative    | \(r \geq 0.10\)         | High (H)   |

### Average Degree (Secondary)

| Category                  | Empirical Range    | Group          |
|---------------------------|--------------------|----------------|
| Low Average Degree        | \(a < 15\)         | Low (L)        |
| Medium Average Degree     | \(15 \leq a < 35\) | Medium (M)     |
| Large Average Degree      | \(35 \leq a < 65\) | High (H)       |
| Very Large Average Degree | \(a \geq 65\)      | Very High (VH) |


## (4) Real-World Network Families

### Combinations

| Network Family | Degree Assortativity Range | Average Degree Range | Combination                                    |
|----------------|----------------------------|----------------------|------------------------------------------------|
| 01_aL_davdL    | \(r < -0.10\)              | \(a < 15\)           | Disassortative + Low Average Degree            |
| 02_aL_davdM    | \(r < -0.10\)              | \(15 \leq a < 35\)   | Disassortative + Medium Average Degree         |
| 03_aL_davdH    | \(r < -0.10\)              | \(35 \leq a < 65\)   | Disassortative + Large Average Degree          |
| 04_aL_davdVH   | \(r < -0.10\)              | \(a \geq 65\)        | Disassortative + Very Large Average Degree     |
| 05_aM_davdL    | \(-0.10 \leq r < 0.10\)    | \(a < 15\)           | Near-Neutral + Low Average Degree              |
| 06_aM_davdM    | \(-0.10 \leq r < 0.10\)    | \(15 \leq a < 35\)   | Near-Neutral + Medium Average Degree           |
| 07_aM_davdH    | \(-0.10 \leq r < 0.10\)    | \(35 \leq a < 65\)   | Near-Neutral + Large Average Degree            |
| 08_aM_davdVH   | \(-0.10 \leq r < 0.10\)    | \(a \geq 65\)        | Near-Neutral + Very Large Average Degree       |
| 09_aH_davdL    | \(r \geq 0.10\)            | \(a < 15\)           | Assortative + Low Average Degree               |
| 10_aH_davdM    | \(r \geq 0.10\)            | \(15 \leq a < 35\)   | Assortative + Medium Average Degree            |
| 11_aH_davdH    | \(r \geq 0.10\)            | \(35 \leq a < 65\)   | Assortative + Large Average Degree             |
| 12_aH_davdVH   | \(r \geq 0.10\)            | \(a \geq 65\)        | Assortative + Very Large Average Degree        |

### Train Assignment

| Network                            | Average Degree | Degree Assortativity | Combination                             | Assigned Family   | Set   |
|------------------------------------|----------------|----------------------|-----------------------------------------|-------------------|-------|
| zachary-karate-club                | 4.5882         | -0.4756              | Disassortative + Low Average Degree     | 01_aL_davdL       | Train |
| books-about-us-politics            | 8.4000         | -0.1279              | Disassortative + Low Average Degree     | 01_aL_davdL       | Train |
| us-political-blogs                 | 27.3552        | -0.2213              | Disassortative + Medium Average Degree  | 02_aL_davdM       | Train |
| cora                               | 4.0797         | -0.0714              | Near-Neutral + Low Average Degree       | 05_aM_davdL       | Train |
| facebook-network-ego698            | 11.0000        | 0.0125               | Near-Neutral + Low Average Degree       | 05_aM_davdL       | Train |
| email-eu-core                      | 32.5842        | -0.0257              | Near-Neutral + Medium Average Degree    | 06_aM_davdM       | Train |
| american-college-football          | 10.6609        | 0.1624               | Assortative + Low Average Degree        | 09_aH_davdL       | Train |
| facebook-network-ego0              | 15.5185        | 0.2330               | Assortative + Medium Average Degree     | 10_aH_davdM       | Train |
| facebook-network-ego3437           | 18.0902        | 0.2221               | Assortative + Medium Average Degree     | 10_aH_davdM       | Train |
| facebook-network-ego414            | 22.8649        | 0.3039               | Assortative + Medium Average Degree     | 10_aH_davdM       | Train |
| facebook-network-ego1684           | 36.1445        | 0.3268               | Assortative + Large Average Degree      | 11_aH_davdH       | Train |
| socio-patterns-primary-school-day1 | 49.9915        | 0.1729               | Assortative + Large Average Degree      | 11_aH_davdH       | Train |
| facebook-network-ego107            | 51.7389        | 0.4316               | Assortative + Large Average Degree      | 11_aH_davdH       | Train |
| facebook-network-ego1912           | 80.7070        | 0.5026               | Assortative + Very Large Average Degree | 12_aH_davdVH      | Train |

### Test Assignment

| Network                              | Average Degree | Degree Assortativity | Combination                                | Assigned Family | Calibrated? |
|--------------------------------------|---------------:|---------------------:|--------------------------------------------|-----------------|-------------|
| socio-patterns-primary-school-day2   |        46.5462 |               0.2168 | Assortative + Large Average Degree         | 11_aH_davdH     | Yes         |
| citeseer                             |         3.4768 |               0.0071 | Near-Neutral + Low Average Degree          | 05_aM_davdL     | Yes         |
| facebook-network-ego3980             |         6.2727 |               0.0530 | Near-Neutral + Low Average Degree          | 05_aM_davdL     | Yes         |
| facebook-network-ego686              |        19.7143 |               0.0841 | Near-Neutral + Medium Average Degree       | 06_aM_davdM     | Yes         |
| facebook-network-ego348              |        28.5000 |               0.2227 | Assortative + Medium Average Degree        | 10_aH_davdM     | Yes         |
| dolphins                             |         5.1290 |              -0.0436 | Near-Neutral + Low Average Degree          | 05_aM_davdL     | Yes         |
| les-miserables                       |         6.5974 |              -0.1652 | Disassortative + Low Average Degree        | 01_aL_davdL     | Yes         |
| jazz-musicians                       |        27.6970 |               0.0202 | Near-Neutral + Medium Average Degree       | 06_aM_davdM     | Yes         |
| c-elegans-neural-network             |        14.4646 |              -0.1632 | Disassortative + Low Average Degree        | 01_aL_davdL     | Yes         |
| c-elegans-metabolic                  |         8.9404 |              -0.2258 | Disassortative + Low Average Degree        | 01_aL_davdL     | Yes         |
| email-urv                            |         9.6222 |               0.0782 | Near-Neutral + Low Average Degree          | 05_aM_davdL     | Yes         |
| co-authorships-in-network-science    |         4.8232 |              -0.0817 | Near-Neutral + Low Average Degree          | 05_aM_davdL     | Yes         |


---
---
---


## (5) Experience 1 (V1) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/)

### Configuration

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
  "pareto_tolerance_fraction_modularity": 0.05,
  "pareto_tolerance_fraction_conductance": 0.05,
  "pareto_tolerance_fraction_stability": 0.05,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": 25578.557138668373
}
```

### K-Boundary Thresholds by Network

| Network                            | #Contributions | K  | c_K                    | c_K+1                  | Valid Threshold? | Threshold              |
|------------------------------------|----------------|----|------------------------|------------------------|------------------|------------------------|
| zachary-karate-club                | 14             | 2  | 0.09307023422932034    | 0.02122012749862965    | True             | 0.044440547213929565   |
| books-about-us-politics            | 6              | 3  | 0.022859050982710166   | 0.005294041417938491   | True             | 0.01100076191348741    |
| us-political-blogs                 | 64             | 2  | 0.050822692775361465   | 0.0431107505765329     | True             | 0.04680816629463676    |
| cora                               | 136            | 7  | 0.010398798894426074   | 0.00980880542050125    | True             | 0.010099494787480654   |
| facebook-network-ego698            | 18             | 9  | 0.00030576431360469525 | 0.00020341051848118692 | True             | 0.00024939061242030603 |
| email-eu-core                      | 63             | 42 | 9.683599871564725e-05  | 8.88471707233404e-05   | True             | 9.27556171347821e-05   |
| american-college-football          | 43             | 12 | 0.0009074459308225949  | 0.0007354430047911205  | True             | 0.0008169300839420987  |
| facebook-network-ego0              | 39             | 22 | 1.9815981134743903e-05 | 1.8957982253285638e-05 | True             | 1.9382234615335713e-05 |
| facebook-network-ego414            | 20             | 7  | 5.431357068130504e-05  | 5.174797193047763e-05  | True             | 5.301525375833059e-05  |
| facebook-network-ego3437           | 66             | 32 | 0.0001288972910471274  | 0.00012697768504916213 | True             | 0.0001279338877165559  |
| facebook-network-ego107            | 67             | 9  | 0.0036724114188061096  | 0.002535313399038592   | True             | 0.0030513462400850967  |
| facebook-network-ego1684           | 40             | 17 | 4.612934543383213e-05  | 4.1832575871964605e-05 | True             | 4.3928457095427864e-05 |
| socio-patterns-primary-school-day1 | 22             | 11 | 0.0003876416675583618  | 0.00028133728532698203 | True             | 0.00033023938958048893 |
| facebook-network-ego1912           | 56             | 45 | 4.1198016663589883e-10 | 3.6618561969374855e-11 | True             | 1.228255725087819e-10  |

### K-Boundary Thresholds by Family

| Network Family | #Networks | #Valid Thresholds | Valid Thresholds                                                        | e_family               | e_global              |
|----------------|-----------|-------------------|-------------------------------------------------------------------------|------------------------|-----------------------|
| 01_aL_davdL    | 2         | 2                 | [0.044440547213929565, 0.01100076191348741]                             | 0.027720654563708487   | 0.0002898150010003975 |
| 02_aL_davdM    | 1         | 1                 | [0.04680816629463676]                                                   | 0.04680816629463676    | 0.0002898150010003975 |
| 05_aM_davdL    | 2         | 2                 | [0.010099494787480654, 0.00024939061242030603]                          | 0.00517444269995048    | 0.0002898150010003975 |
| 06_aM_davdM    | 1         | 1                 | [9.27556171347821e-05]                                                  | 9.27556171347821e-05   | 0.0002898150010003975 |
| 09_aH_davdL    | 1         | 1                 | [0.0008169300839420987]                                                 | 0.0008169300839420987  | 0.0002898150010003975 |
| 10_aH_davdM    | 3         | 3                 | [1.9382234615335713e-05, 5.301525375833059e-05, 0.0001279338877165559]  | 5.301525375833059e-05  | 0.0002898150010003975 |
| 11_aH_davdH    | 3         | 3                 | [0.0030513462400850967, 4.3928457095427864e-05, 0.00033023938958048893] | 0.00033023938958048893 | 0.0002898150010003975 |
| 12_aH_davdVH   | 1         | 1                 | [1.228255725087819e-10]                                                 | 1.228255725087819e-10  | 0.0002898150010003975 |

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family             | e_global              | e*                    | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Stability           | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable? |
|-------------|-----------------------------------|----------------------|-----------------------|-----------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|---------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.027720654563708487 | 0.0002898150010003975 | 0.0002898150010003975 | 2            | 46     | 0.24341533302850177 | 0.09375              | 0.32608695652173914               | 0.13024282560706402        | 0.527715940784333   | 5.671354642991849  | 0.09090909090909091          | 1               | 11.439680021439262 | 0.09090909090909091           | 1                | False       |
| 01_aL_davdL | c-elegans-neural-network          | 0.027720654563708487 | 0.0002898150010003975 | 0.0002898150010003975 |              | 16     | 0.2842342406777427  | 0.46195652173913043  | 0.0625                            | 0.15151515151515152        | 0.545943643563116   | 30.504997337155242 | 0.09090909090909091          | 1               | 5.891852981116436  | 0.09090909090909091           | 1                | False       |
| 05_aM_davdL | co-authorships-in-network-science | 0.00517444269995048  | 0.0002898150010003975 | 0.003949251189157377  | 5            | 7      | 0.7602209012252873  | 0.021739130434782608 | 0.0                               | 0.31398416886543534        | 0.5462553288728     | 54.546406956094536 | 0.09090909090909091          | 1               | 14.076048035260847 | 0.09090909090909091           | 1                | False       |
| 05_aM_davdL | dolphins                          | 0.00517444269995048  | 0.0002898150010003975 | 0.013938562276953103  | 2            | 2      | 0.38477512756615634 | 0.0707070707070707   | 0.0                               | 0.6451612903225806         | 0.6052930319025152  | 4.866851653431884  | 0.09090909090909091          | 1               | 7.679261006647712  | 0.09090909090909091           | 1                | True        |
| 05_aM_davdL | email-urv                         | 0.00517444269995048  | 0.0002898150010003975 | 0.005347645826241863  | 8            | 8      | 0.4752620543168384  | 0.24347413383958236  | 0.0                               | 0.22241835834068843        | 0.33861371739004165 | 16.25059416236578  | 0.09090909090909091          | 1               | 6.0977803433018645 | 0.09090909090909091           | 1                | False       |
| 06_aM_davdM | jazz-musicians                    | 9.27556171347821e-05 | 0.0002898150010003975 | 9.27556171347821e-05  | 24           | 24     | 0.24936124770634396 | 0.2746234067207416   | 0.4166666666666667                | 0.15656565656565657        | 0.6159677056681716  | 28.801778304736953 | 0.09090909090909091          | 1               | 47.5960099793492   | 0.09090909090909091           | 1                | True        |
| 01_aL_davdL | les-miserables                    | 0.027720654563708487 | 0.0002898150010003975 | 0.021558116419948353  | 4            | 5      | 0.47517670035340065 | 0.16666666666666666  | 0.0                               | 0.2727272727272727         | 0.6216738690624128  | 7.040930385590737  | 0.09090909090909091          | 1               | 3.8742438960197836 | 0.09090909090909091           | 1                | False       |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- [socio-patterns-primary-school-day2](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/socio-patterns-primary-school-day2/)
- [citeseer](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/citeseer/)
- [facebook-network-ego3980](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/facebook-network-ego3980/)
- [facebook-network-ego686](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/facebook-network-ego686/)
- [facebook-network-ego348](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/facebook-network-ego348/)

#### Summary

| Family      | Network                            | e_family               | e_global              | e*                    | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Stability          | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable? |
|-------------|------------------------------------|------------------------|-----------------------|-----------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|--------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|-------------|
| 05_aM_davdL | citeseer                           | 0.00517444269995048    | 0.0002898150010003975 | 0.0002898150010003975 | 9            | 33     | 0.691827934483624   | 0.005076142131979695 | 0.0                               | 0.34218009478672984        | 0.4347534913509913 | 36.3026230176481   | 0.09090909090909091          | 1               | 3.3781208783817944 | 0.09090909090909091           | 1                | True        |
| 10_aH_davdM | facebook-network-ego348            | 5.301525375833059e-05  | 0.0002898150010003975 | 6.414810348671026e-05 | 18           | 18     | 0.21253507751207587 | 0.24                 | 0.3888888888888889                | 0.27232142857142855        | 0.5534923368261204 | 34.111875287370275 | 0.09090909090909091          | 1               | 27.546288363388246 | 0.09090909090909091           | 1                | True        |
| 05_aM_davdL | facebook-network-ego3980           | 0.00517444269995048    | 0.0002898150010003975 | 0.0043708620491837245 | 7            | 7      | 0.3532083595883218  | 0.34831460674157305  | 0.2857142857142857                | 0.2727272727272727         | 0.743484915560415  | 4.714779009693943  | 0.09090909090909091          | 1               | 2.180740734270952  | 0.18181818181818182           | 2                | True        |
| 06_aM_davdM | facebook-network-ego686            | 9.27556171347821e-05   | 0.0002898150010003975 | 0.0002898150010003975 | 22           | 17     | 0.20652447402506474 | 0.35537190082644626  | 0.17647058823529413               | 0.17857142857142858        | 0.6024911855186317 | 19.784881806959213 | 0.09090909090909091          | 1               | 4.286799423526288  | 0.09090909090909091           | 1                | True        |
| 11_aH_davdH | socio-patterns-primary-school-day2 | 0.00033023938958048893 | 0.0002898150010003975 | 0.00052156630059955   | 13           | 13     | 0.3438556177061009  | 0.38663171690694625  | 0.07692307692307693               | 0.18067226890756302        | 0.8829606582908681 | 73.61561861606107  | 0.09090909090909091          | 1               | 38.550193348199514 | 0.09090909090909091           | 1                | True        |

#### Blind Validation + Thresholds Details

- [Open File](../../../results/real-world/stage2/v1/results_2026-07-12_23-54-12-394620/test_networks_with_gt/_combine_threshold_details.csv)


## (6) Experience 2 (V1 + Tolerance Values) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/)

### Configuration

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
  "pareto_tolerance_fraction_modularity": 0.1,
  "pareto_tolerance_fraction_conductance": 0.1,
  "pareto_tolerance_fraction_stability": 0.1,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": 25146.02458238788
}
```

### K-Boundary Thresholds by Network

``

### K-Boundary Thresholds by Family

``

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family             | e_global              | e*                    | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Stability           | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable? |
|-------------|-----------------------------------|----------------------|-----------------------|-----------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|---------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.027720654563708487 | 0.0002898150010003975 | 0.0002898150010003975 | 2            | 46     | 0.24341533302850177 | 0.09375              | 0.32608695652173914               | 0.13024282560706402        | 0.527715940784333   | 5.671354642991849  | 0.09090909090909091          | 1               | 11.439680021439262 | 0.09090909090909091           | 1                | False       |
| 01_aL_davdL | c-elegans-neural-network          | 0.027720654563708487 | 0.0002898150010003975 | 0.0002898150010003975 |              | 16     | 0.2842342406777427  | 0.46195652173913043  | 0.0625                            | 0.15151515151515152        | 0.545943643563116   | 30.504997337155242 | 0.09090909090909091          | 1               | 5.891852981116436  | 0.09090909090909091           | 1                | False       |
| 05_aM_davdL | co-authorships-in-network-science | 0.00517444269995048  | 0.0002898150010003975 | 0.003949251189157377  | 5            | 7      | 0.7602209012252873  | 0.021739130434782608 | 0.0                               | 0.31398416886543534        | 0.5462553288728     | 54.546406956094536 | 0.09090909090909091          | 1               | 14.076048035260847 | 0.09090909090909091           | 1                | False       |
| 05_aM_davdL | dolphins                          | 0.00517444269995048  | 0.0002898150010003975 | 0.013938562276953103  | 2            | 2      | 0.38477512756615634 | 0.0707070707070707   | 0.0                               | 0.6451612903225806         | 0.6052930319025152  | 4.866851653431884  | 0.09090909090909091          | 1               | 7.679261006647712  | 0.09090909090909091           | 1                | True        |
| 05_aM_davdL | email-urv                         | 0.00517444269995048  | 0.0002898150010003975 | 0.005347645826241863  | 8            | 8      | 0.4752620543168384  | 0.24347413383958236  | 0.0                               | 0.22241835834068843        | 0.33861371739004165 | 16.25059416236578  | 0.09090909090909091          | 1               | 6.0977803433018645 | 0.09090909090909091           | 1                | False       |
| 06_aM_davdM | jazz-musicians                    | 9.27556171347821e-05 | 0.0002898150010003975 | 9.27556171347821e-05  | 24           | 24     | 0.24936124770634396 | 0.2746234067207416   | 0.4166666666666667                | 0.15656565656565657        | 0.6159677056681716  | 28.801778304736953 | 0.09090909090909091          | 1               | 47.5960099793492   | 0.09090909090909091           | 1                | True        |
| 01_aL_davdL | les-miserables                    | 0.027720654563708487 | 0.0002898150010003975 | 0.021558116419948353  | 4            | 5      | 0.47517670035340065 | 0.16666666666666666  | 0.0                               | 0.2727272727272727         | 0.6216738690624128  | 7.040930385590737  | 0.09090909090909091          | 1               | 3.8742438960197836 | 0.09090909090909091           | 1                | False       |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- [socio-patterns-primary-school-day2](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/socio-patterns-primary-school-day2/)
- [citeseer](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/citeseer/)
- [facebook-network-ego3980](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/facebook-network-ego3980/)
- [facebook-network-ego686](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/facebook-network-ego686/)
- [facebook-network-ego348](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/facebook-network-ego348/)

#### Summary

| Family      | Network                            | e_family               | e_global              | e*                    | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Stability          | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable? |
|-------------|------------------------------------|------------------------|-----------------------|-----------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|--------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|-------------|
| 05_aM_davdL | citeseer                           | 0.00517444269995048    | 0.0002898150010003975 | 0.0002898150010003975 | 9            | 33     | 0.691827934483624   | 0.005076142131979695 | 0.0                               | 0.34218009478672984        | 0.4347534913509913 | 36.3026230176481   | 0.09090909090909091          | 1               | 3.3781208783817944 | 0.09090909090909091           | 1                | True        |
| 10_aH_davdM | facebook-network-ego348            | 5.301525375833059e-05  | 0.0002898150010003975 | 6.414810348671026e-05 | 18           | 18     | 0.21253507751207587 | 0.24                 | 0.3888888888888889                | 0.27232142857142855        | 0.5534923368261204 | 34.111875287370275 | 0.09090909090909091          | 1               | 27.546288363388246 | 0.09090909090909091           | 1                | True        |
| 05_aM_davdL | facebook-network-ego3980           | 0.00517444269995048    | 0.0002898150010003975 | 0.0043708620491837245 | 7            | 7      | 0.3532083595883218  | 0.34831460674157305  | 0.2857142857142857                | 0.2727272727272727         | 0.743484915560415  | 4.714779009693943  | 0.09090909090909091          | 1               | 2.180740734270952  | 0.18181818181818182           | 2                | True        |
| 06_aM_davdM | facebook-network-ego686            | 9.27556171347821e-05   | 0.0002898150010003975 | 0.0002898150010003975 | 22           | 17     | 0.20652447402506474 | 0.35537190082644626  | 0.17647058823529413               | 0.17857142857142858        | 0.6024911855186317 | 19.784881806959213 | 0.09090909090909091          | 1               | 4.286799423526288  | 0.09090909090909091           | 1                | True        |
| 11_aH_davdH | socio-patterns-primary-school-day2 | 0.00033023938958048893 | 0.0002898150010003975 | 0.00052156630059955   | 13           | 13     | 0.3438556177061009  | 0.38663171690694625  | 0.07692307692307693               | 0.18067226890756302        | 0.8829606582908681 | 73.61561861606107  | 0.09090909090909091          | 1               | 38.550193348199514 | 0.09090909090909091           | 1                | True        |

#### Blind Validation + Thresholds Details

- [Open File](../../../results/real-world/stage2/v1/results_2026-07-14_00-00-52-195086/test_networks_with_gt/_combine_threshold_details.csv)


## (7) Experience 3 (V1 + Overlapping Communities) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/)

### Configuration

```json
{
  "apply_lapin": true,
  "tau": 0.05,
  "k_max_boundary": 500,
  "overlapping_communities": true,
  "defuzzification_gamma": 0.8,
  "number_of_thresholds_to_retain_after_intrinsic_evaluation": 3,
  "number_of_thresholds_to_retain_after_stability_evaluation": 2,
  "near_singleton_boundary": 2,
  "number_of_perturbed_graphs": 10,
  "fraction_of_edges_swaps_in_perturbed_graphs": 0.05,
  "number_of_null_models": 10,
  "fraction_of_edges_swaps_in_null_models": 10,
  "pareto_tolerance_fraction_modularity": 0.05,
  "pareto_tolerance_fraction_conductance": 0.05,
  "pareto_tolerance_fraction_stability": 0.05,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": 25578.557138668373
}
```

### K-Boundary Thresholds by Network

``

### K-Boundary Thresholds by Family

``

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family             | e_global              | e*                     | K'(e_family) | K'(e*) | Modularity            | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Stability          | Z Modularity        | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable? |
|-------------|-----------------------------------|----------------------|-----------------------|------------------------|--------------|--------|-----------------------|----------------------|-----------------------------------|----------------------------|--------------------|---------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.027720654563708487 | 0.0002898150010003975 | 0.01563527520019711    | 2            | 3      | 0.0026532813020887637 | 0.045421203662466526 | 0.0                               | 0.8741721854304636         | 0.7248363450581694 | 9.164952552445696   | 0.3333333333333333           | 1               |                    | 0.3333333333333333            | 1                | False       |
| 01_aL_davdL | c-elegans-neural-network          | 0.027720654563708487 | 0.0002898150010003975 | 1.2461521332244188e-11 |              | 38     | 0.028782408709858896  | 0.0                  | 0.07894736842105263               | 0.1111111111111111         | 0.5600342689191836 | 4.28862962730567    | 0.09090909090909091          | 1               | 0.7584401570086422 | 0.6363636363636364            | 1                | False       |
| 05_aM_davdL | co-authorships-in-network-science | 0.00517444269995048  | 0.0002898150010003975 | 0.003949251189157377   | 5            | 7      | 0.01696119322019819   | 0.010980177511617673 | 0.0                               | 0.316622691292876          | 0.5779843805447145 | 5.041168047915715   | 0.09090909090909091          | 1               | 12.793703164493177 | 0.09090909090909091           | 1                | False       |
| 05_aM_davdL | dolphins                          | 0.00517444269995048  | 0.0002898150010003975 | 0.013938562276953103   | 2            | 2      | 0.019277385165251716  | 0.02438791554357592  | 0.0                               | 0.6451612903225806         | 0.8334116976285113 | -2.3481442388282034 | 1.0                          | 11              | 6.270185582737237  | 0.09090909090909091           | 1                | True        |
| 05_aM_davdL | email-urv                         | 0.00517444269995048  | 0.0002898150010003975 | 6.379616864371859e-12  | 8            | 66     | 0.015868900966845817  | 0.0                  | 0.09090909090909091               | 0.11915269196822595        | 0.6199054702487004 | 15.663306116653718  | 0.09090909090909091          | 1               |                    | 1.0                           | 1                | True        |
| 06_aM_davdM | jazz-musicians                    | 9.27556171347821e-05 | 0.0002898150010003975 | 9.27556171347821e-05   | 24           | 24     | 0.017946870694294657  | 0.0                  | 0.375                             | 0.1919191919191919         | 0.7195917553705065 | 7.972024766664742   | 0.09090909090909091          | 1               | 1.7910269085015522 | 0.2727272727272727            | 1                | True        |
| 01_aL_davdL | les-miserables                    | 0.027720654563708487 | 0.0002898150010003975 | 0.021558116419948353   | 4            | 5      | 0.041066744129782326  | 0.10408712615986418  | 0.0                               | 0.3246753246753247         | 0.8315318060875819 | 9.289244973055629   | 0.09090909090909091          | 1               | 0.9074030718615549 | 0.2727272727272727            | 3                | False       |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v1/results_2026-07-14_10-55-24-787794/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- TODO

#### Summary

- TODO

#### Blind Validation + Thresholds Details

- TODO


---
---
---


## (8) Experience 4 (V2) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/)

### Configuration

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
  "pareto_tolerance_fraction_modularity": 0.05,
  "pareto_tolerance_fraction_conductance": 0.05,
  "pareto_tolerance_fraction_stability": 0.05,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": 18655.70619255677
}
```

### K-Boundary Thresholds by Network

``

### K-Boundary Thresholds by Family

``

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family              | e_global               | e* (Name) | e*                     | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Runtime              | Stability          | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable Modularity? | Acceptable Conductance? | Acceptable Non-Degenerate? | Acceptable Stability? | Acceptable Null Model? | Acceptable? |
|-------------|-----------------------------------|-----------------------|------------------------|-----------|------------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|----------------------|--------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|------------------------|-------------------------|----------------------------|-----------------------|------------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.028080065029042933  | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 2            | 44     | 0.23949019966468527 | 0.1                  | 0.3409090909090909                | 0.11920529801324503        | 6.374951345846057    | 0.5220908374696105 | 6.291086957439757  | 0.09090909090909091          | 1               | 15.169280518320992 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 01_aL_davdL | c-elegans-neural-network          | 0.028080065029042933  | 0.00028981500100176477 | e_global  | 0.00028981500100176477 |              | 15     | 0.2913849096123369  | 0.39045553145336226  | 0.0                               | 0.19528619528619529        | 0.9493749253451824   | 0.5059237544986177 | 31.987684758093874 | 0.09090909090909091          | 1               | 7.496780139756489  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | co-authorships-in-network-science | 0.004363122171917465  | 0.00028981500100176477 | e_family  | 0.004363122171917465   | 7            | 7      | 0.7602209012252873  | 0.021739130434782608 | 0.0                               | 0.31398416886543534        | 0.768794784322381    | 0.546836540493014  | 65.66964073115368  | 0.09090909090909091          | 1               | 14.13075992531666  | 0.09090909090909091           | 1                | True                   | False                   | True                       | False                 | True                   | False       |
| 05_aM_davdL | dolphins                          | 0.004363122171917465  | 0.00028981500100176477 | e_above   | 0.012602118948721593   | 2            | 2      | 0.38477512756615634 | 0.0707070707070707   | 0.0                               | 0.6451612903225806         | 0.015210874378681183 | 0.5935080201453792 | 4.68409402587843   | 0.09090909090909091          | 1               | 6.639080835580617  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | email-urv                         | 0.004363122171917465  | 0.00028981500100176477 | e_above   | 0.004663807868446709   | 11           | 10     | 0.46375682474045976 | 0.22097625329815304  | 0.0                               | 0.2418358340688438         | 7.808940853923559    | 0.3807104935240541 | 23.791808418239977 | 0.09090909090909091          | 1               | 12.312083332926166 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 06_aM_davdM | jazz-musicians                    | 7.588552945420201e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 25           | 23     | 0.26522770837622717 | 0.20977596741344195  | 0.43478260869565216               | 0.1919191919191919         | 0.6483434308320284   | 0.5904498366910051 | 29.530481509316328 | 0.09090909090909091          | 1               | 38.69488783928572  | 0.09090909090909091           | 1                | True                   | True                    | True                       | False                 | True                   | False       |
| 01_aL_davdL | les-miserables                    | 0.028080065029042933  | 0.00028981500100176477 | e_above   | 0.03812106247407752    | 4            | 4      | 0.42300359600719195 | 0.1557377049180328   | 0.0                               | 0.37662337662337664        | 0.030305463820695877 | 0.5973478824696391 | 3.529654813639928  | 0.09090909090909091          | 1               | 1.5931131604663968 | 0.09090909090909091           | 1                | False                  | True                    | True                       | False                 | True                   | False       |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- [socio-patterns-primary-school-day2](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/socio-patterns-primary-school-day2/)
- [citeseer](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/citeseer/)
- [facebook-network-ego3980](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/facebook-network-ego3980/)
- [facebook-network-ego686](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/facebook-network-ego686/)
- [facebook-network-ego348](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/facebook-network-ego348/)

#### Summary

| Family      | Network                            | e_family              | e_global               | e* (Name) | e*                     | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Runtime             | Stability           | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable Modularity? | Acceptable Conductance? | Acceptable Non-Degenerate? | Acceptable Stability? | Acceptable Null Model? | Acceptable? |
|-------------|------------------------------------|-----------------------|------------------------|-----------|------------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|---------------------|---------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|------------------------|-------------------------|----------------------------|-----------------------|------------------------|-------------|
| 05_aM_davdL | citeseer                           | 0.004363122171917465  | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 11           | 34     | 0.7155972354853021  | 0.005076142131979695 | 0.0                               | 0.3127962085308057         | 228.16781814023852  | 0.43893379661566795 | 59.79536373509533  | 0.09090909090909091          | 1               | 3.517708357610432  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 10_aH_davdM | facebook-network-ego348            | 5.301634600929657e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 19           | 10     | 0.26271108339457666 | 0.015873015873015872 | 0.1                               | 0.3794642857142857         | 0.37763713113963604 | 0.5464112115252049  | 27.38235941213545  | 0.09090909090909091          | 1               | 7.399103266050899  | 0.09090909090909091           | 1                | True                   | True                    | True                       | False                 | True                   | False       |
| 05_aM_davdL | facebook-network-ego3980           | 0.004363122171917465  | 0.00028981500100176477 | e_above   | 0.004370862049253332   | 7            | 7      | 0.35320835958832175 | 0.34831460674157305  | 0.2857142857142857                | 0.2727272727272727         | 0.02337164618074894 | 0.74526744180572    | 5.129444014180584  | 0.09090909090909091          | 1               | 2.222551052706473  | 0.18181818181818182           | 2                | True                   | True                    | True                       | True                  | True                   | True        |
| 06_aM_davdM | facebook-network-ego686            | 7.588552945420201e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 21           | 17     | 0.1996146715792667  | 0.38461538461538464  | 0.17647058823529413               | 0.16666666666666666        | 0.36107429303228855 | 0.5948303702369957  | 18.768904990837214 | 0.09090909090909091          | 1               | 3.9625825119867626 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 11_aH_davdH | socio-patterns-primary-school-day2 | 0.0003302393895804786 | 0.00028981500100176477 | e_above   | 0.000521566300561776   | 13           | 13     | 0.3438556177061009  | 0.38663171690694625  | 0.07692307692307693               | 0.18067226890756302        | 0.5356441475450993  | 0.8829606582908681  | 73.61561861606107  | 0.09090909090909091          | 1               | 38.550193348199514 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |

#### Blind Validation + Thresholds Details

- [Open File](../../../results/real-world/stage2/v2/results_2026-07-14_18-35-00-623858/test_networks_with_gt/_combine_threshold_details.csv)


## (9) Experience 5 (V2 + Tolerance Values) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/)

### Configuration

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
  "pareto_tolerance_fraction_modularity": 0.1,
  "pareto_tolerance_fraction_conductance": 0.1,
  "pareto_tolerance_fraction_stability": 0.1,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": 16401.477376449853
}
```

### K-Boundary Thresholds by Network

``

### K-Boundary Thresholds by Family

``

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family              | e_global               | e* (Name) | e*                     | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Runtime              | Stability           | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable Modularity? | Acceptable Conductance? | Acceptable Non-Degenerate? | Acceptable Stability? | Acceptable Null Model? | Acceptable? |
|-------------|-----------------------------------|-----------------------|------------------------|-----------|------------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|----------------------|---------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|------------------------|-------------------------|----------------------------|-----------------------|------------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.028080065029042933  | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 2            | 44     | 0.23949019966468527 | 0.1                  | 0.3409090909090909                | 0.11920529801324503        | 6.443678721785545    | 0.5220908374696105  | 6.291086957439757  | 0.09090909090909091          | 1               | 15.169280518320992 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 01_aL_davdL | c-elegans-neural-network          | 0.028080065029042933  | 0.00028981500100176477 | e_global  | 0.00028981500100176477 |              | 15     | 0.2913849096123369  | 0.39045553145336226  | 0.0                               | 0.19528619528619529        | 0.9605815783143044   | 0.5059237544986177  | 31.987684758093874 | 0.09090909090909091          | 1               | 7.496780139756489  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | co-authorships-in-network-science | 0.004363122171917465  | 0.00028981500100176477 | e_family  | 0.004363122171917465   | 7            | 7      | 0.7602209012252873  | 0.021739130434782608 | 0.0                               | 0.31398416886543534        | 0.7767880018800497   | 0.546836540493014   | 65.66964073115368  | 0.09090909090909091          | 1               | 14.13075992531666  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | dolphins                          | 0.004363122171917465  | 0.00028981500100176477 | e_above   | 0.012602118948721593   | 2            | 2      | 0.38477512756615634 | 0.0707070707070707   | 0.0                               | 0.6451612903225806         | 0.013360997661948204 | 0.5935080201453792  | 4.68409402587843   | 0.09090909090909091          | 1               | 6.639080835580617  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | email-urv                         | 0.004363122171917465  | 0.00028981500100176477 | e_below   | 0.004134568218102241   | 11           | 11     | 0.457439119809947   | 0.22022621423819028  | 0.0                               | 0.22859664607237423        | 8.334643641486764    | 0.38956158755033055 | 20.9916526997366   | 0.09090909090909091          | 1               | 20.039234649310075 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 06_aM_davdM | jazz-musicians                    | 7.588552945420201e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 25           | 23     | 0.26522770837622717 | 0.20977596741344195  | 0.43478260869565216               | 0.1919191919191919         | 0.6524173356592655   | 0.5904498366910051  | 29.530481509316328 | 0.09090909090909091          | 1               | 38.69488783928572  | 0.09090909090909091           | 1                | True                   | True                    | True                       | False                 | True                   | False       |
| 01_aL_davdL | les-miserables                    | 0.028080065029042933  | 0.00028981500100176477 | e_below   | 0.021815121633352176   | 4            | 5      | 0.47517670035340065 | 0.16666666666666666  | 0.0                               | 0.2727272727272727         | 0.03669731877744198  | 0.6351915179720857  | 6.769313341340573  | 0.09090909090909091          | 1               | 7.743297729344654  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- [socio-patterns-primary-school-day2](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/socio-patterns-primary-school-day2/)
- [citeseer](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/citeseer/)
- [facebook-network-ego3980](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/facebook-network-ego3980/)
- [facebook-network-ego686](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/facebook-network-ego686/)
- [facebook-network-ego348](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/facebook-network-ego348/)

#### Summary

| Family      | Network                            | e_family              | e_global               | e* (Name) | e*                     | K'(e_family) | K'(e*) | Modularity          | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Runtime              | Stability          | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable Modularity? | Acceptable Conductance? | Acceptable Non-Degenerate? | Acceptable Stability? | Acceptable Null Model? | Acceptable? |
|-------------|------------------------------------|-----------------------|------------------------|-----------|------------------------|--------------|--------|---------------------|----------------------|-----------------------------------|----------------------------|----------------------|--------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|------------------------|-------------------------|----------------------------|-----------------------|------------------------|-------------|
| 05_aM_davdL | citeseer                           | 0.004363122171917465  | 0.00028981500100176477 | e_below   | 0.0034848743111167086  | 11           | 14     | 0.6887774426826849  | 0.005076142131979695 | 0.0                               | 0.3819905213270142         | 84.23463627882302    | 0.3860131985902274 | 20.437528887262687 | 0.09090909090909091          | 1               | 13.30591785039913  | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 10_aH_davdM | facebook-network-ego348            | 5.301634600929657e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 19           | 10     | 0.26271108339457666 | 0.015873015873015872 | 0.1                               | 0.3794642857142857         | 0.370725866407156    | 0.5464112115252049 | 27.38235941213545  | 0.09090909090909091          | 1               | 7.399103266050899  | 0.09090909090909091           | 1                | True                   | True                    | True                       | False                 | True                   | False       |
| 05_aM_davdL | facebook-network-ego3980           | 0.004363122171917465  | 0.00028981500100176477 | e_above   | 0.004370862049253332   | 7            | 7      | 0.35320835958832175 | 0.34831460674157305  | 0.2857142857142857                | 0.2727272727272727         | 0.024328209459781647 | 0.74526744180572   | 5.129444014180584  | 0.09090909090909091          | 1               | 2.222551052706473  | 0.18181818181818182           | 2                | True                   | True                    | True                       | True                  | True                   | True        |
| 06_aM_davdM | facebook-network-ego686            | 7.588552945420201e-05 | 0.00028981500100176477 | e_global  | 0.00028981500100176477 | 21           | 17     | 0.1996146715792667  | 0.38461538461538464  | 0.17647058823529413               | 0.16666666666666666        | 0.37371474876999855  | 0.5948303702369957 | 18.768904990837214 | 0.09090909090909091          | 1               | 3.9625825119867626 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 11_aH_davdH | socio-patterns-primary-school-day2 | 0.0003302393895804786 | 0.00028981500100176477 | e_above   | 0.000521566300561776   | 13           | 13     | 0.3438556177061009  | 0.38663171690694625  | 0.07692307692307693               | 0.18067226890756302        | 0.5343852806836367   | 0.8829606582908681 | 73.61561861606107  | 0.09090909090909091          | 1               | 38.550193348199514 | 0.09090909090909091           | 1                | True                   | True                    | True                       | True                  | True                   | True        |

#### Blind Validation + Thresholds Details

- [Open File](../../../results/real-world/stage2/v2/results_2026-07-14_23-45-56-297136/test_networks_with_gt/_combine_threshold_details.csv)


## (10) Experience 6 (V2 + Overlapping Communities) - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

- [Open Folder](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/)

### Configuration

```json
{
  "apply_lapin": true,
  "tau": 0.05,
  "k_max_boundary": 500,
  "overlapping_communities": true,
  "defuzzification_gamma": 0.8,
  "number_of_thresholds_to_retain_after_intrinsic_evaluation": 3,
  "number_of_thresholds_to_retain_after_stability_evaluation": 2,
  "near_singleton_boundary": 2,
  "number_of_perturbed_graphs": 10,
  "fraction_of_edges_swaps_in_perturbed_graphs": 0.05,
  "number_of_null_models": 10,
  "fraction_of_edges_swaps_in_null_models": 10,
  "pareto_tolerance_fraction_modularity": 0.05,
  "pareto_tolerance_fraction_conductance": 0.05,
  "pareto_tolerance_fraction_stability": 0.05,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.5,
  "execution_elapsed_time_secs": "-"
}
```

### K-Boundary Thresholds by Network

``

### K-Boundary Thresholds by Family

``

### Networks Without Ground-Truth

- [les-miserables](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/les-miserables/)
- [jazz-musicians](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/jazz-musicians/)
- [c-elegans-neural-network](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/c-elegans-neural-network/)
- [c-elegans-metabolic](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/c-elegans-metabolic/)
- [email-urv](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/email-urv/)
- [co-authorships-in-network-science](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/co-authorships-in-network-science/)

#### Summary

| Family      | Network                           | e_family              | e_global               | e* (Name) | e*                     | K'(e_family) | K'(e*) | Modularity           | Conductance          | Singleton/Near-Singleton Fraction | Largest-Community Fraction | Runtime              | Stability          | Z Modularity       | Modularity Empirical p-value | Modularity Rank | Z Conductance      | Conductance Empirical p-value | Conductance Rank | Acceptable Modularity? | Acceptable Conductance? | Acceptable Non-Degenerate? | Acceptable Stability? | Acceptable Null Model? | Acceptable? |
|-------------|-----------------------------------|-----------------------|------------------------|-----------|------------------------|--------------|--------|----------------------|----------------------|-----------------------------------|----------------------------|----------------------|--------------------|--------------------|------------------------------|-----------------|--------------------|-------------------------------|------------------|------------------------|-------------------------|----------------------------|-----------------------|------------------------|-------------|
| 01_aL_davdL | c-elegans-metabolic               | 0.028080065029042933  | 0.00028981500100176477 | e_family  | 0.028080065029042933   | 2            | 2      | 0.00222199354578602  | 0.019544961746700035 | 0.0                               | 0.9558498896247241         | 0.4360369350761175   | 0.8189446354990911 |                    | 0.5                          | 1               |                    | 0.5                           | 1                | False                  | False                   | False                      | True                  | True                   | False       |
| 01_aL_davdL | c-elegans-neural-network          | 0.028080065029042933  | 0.00028981500100176477 | e_elbow   | 1.5597606978890488e-20 |              | 66     | 0.02796129334610027  | 0.0                  | 0.015151515151515152              | 0.13468013468013468        | 4.016998283565044    | 0.3187950892964603 | 0.7762619625274938 | 0.18181818181818182          | 2               | 0.7584401570086422 | 0.6363636363636364            | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 05_aM_davdL | co-authorships-in-network-science | 0.004363122171917465  | 0.00028981500100176477 | e_family  | 0.004363122171917465   | 7            | 7      | 0.016961192574523155 | 0.010980177511617673 | 0.0                               | 0.316622691292876          | 0.7642318587750196   | 0.5790444947433135 | 4.9876718355766645 | 0.09090909090909091          | 1               | 22.98397734941673  | 0.09090909090909091           | 1                | False                  | False                   | True                       | True                  | True                   | False       |
| 05_aM_davdL | dolphins                          | 0.004363122171917465  | 0.00028981500100176477 | e_family  | 0.004363122171917465   | 2            | 2      | 0.019277385165251716 | 0.02438791554357592  | 0.0                               | 0.6451612903225806         | 0.018761711195111275 | 0.6863826033070823 | -4.711440067059297 | 1.0                          | 11              | 0.6254260636019793 | 0.6363636363636364            | 7                | False                  | False                   | True                       | True                  | False                  | False       |
| 05_aM_davdL | email-urv                         | 0.004363122171917465  | 0.00028981500100176477 | e_elbow   | 5.0591288420340946e-06 | 11           | 60     | 0.014546307204618962 | 0.0                  | 0.03333333333333333               | 0.12268314210061783        | 43.47265254892409    | 0.6742654591819897 | 10.310816099930953 | 0.09090909090909091          | 1               |                    | 1.0                           | 1                | True                   | True                    | True                       | True                  | True                   | True        |
| 06_aM_davdM | jazz-musicians                    | 7.588552945420201e-05 | 0.00028981500100176477 | e_family  | 7.588552945420201e-05  | 25           | 25     | 0.01900795179582708  | 0.0                  | 0.36                              | 0.1919191919191919         | 0.7309540808200836   | 0.7247722266219945 | 11.041292212260425 | 0.09090909090909091          | 1               | 1.7862746508211103 | 0.2727272727272727            | 1                | False                  | True                    | True                       | True                  | True                   | False       |
| 01_aL_davdL | les-miserables                    | 0.028080065029042933  | 0.00028981500100176477 | e_family  | 0.028080065029042933   | 4            | 4      | 0.03877543424896348  | 0.09746692622976323  | 0.0                               | 0.45454545454545453        | 0.031031902879476547 | 0.799058519501774  | 7.502488555876716  | 0.09090909090909091          | 1               | 1.0604210797692872 | 0.09090909090909091           | 1                | False                  | False                   | True                       | False                 | True                   | False       |

#### Thresholds Details

- [Open File](../../../results/real-world/stage2/v2/results_2026-07-15_04-19-17-796221/test_networks_without_gt/_combine_threshold_details.csv)

### Networks With Ground-Truth

- TODO

#### Summary

- TODO

#### Blind Validation + Thresholds Details

- TODO
