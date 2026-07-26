# Report 9 - Fine-Tuned Experimental Protocol for FADDIS Threshold Selection


## Table of Contents

- [(1) Network Selection and Division](#1-network-selection-and-division)
  - [Train Networks](#train-networks)
  - [Test Networks](#test-networks)
- [(2) Observations from Stage 1](#2-observations-from-stage-1)
- [(3) FADDIS Sensitivity Analysis](#3-faddis-sensitivity-analysis)
  - [Network Properties (LAPIN-on)](#network-properties-lapin-on)
  - [Ground-Truth Properties (LAPIN-on)](#ground-truth-properties-lapin-on)
  - [FADDIS Correlations (LAPIN-on)](#faddis-correlations-lapin-on)
  - [Network Properties (LAPIN-off)](#network-properties-lapin-off)
  - [Ground-Truth Properties (LAPIN-off)](#ground-truth-properties-lapin-off)
  - [FADDIS Correlations (LAPIN-off)](#faddis-correlations-lapin-off)
  - [Degree Assortativity (Primary)](#degree-assortativity-primary)
  - [Average Degree (Secondary)](#average-degree-secondary)
- [(4) Real-World Network Families](#4-real-world-network-families)
  - [Combinations](#combinations)
  - [Train Assignment](#train-assignment)
  - [Test Assignment](#test-assignment)
- [(5) Pipeline Configuration](#5-pipeline-configuration)
- [(6) Pipeline](#6-pipeline)
  - [Stage 1: Network Family K-Boundary Thresholds](#stage-1-network-family-k-boundary-thresholds)
  - [Stage 2: Network Contribution-Boundary Thresholds](#stage-2-network-contribution-boundary-thresholds)
    - [Stage 2.1: Candidate Thresholds](#stage-21-candidate-thresholds)
    - [Stage 2.2: Intrinsic Evaluation](#stage-22-intrinsic-evaluation---number_of_thresholds_to_retain_after_intrinsic_evaluation--epsilon_family)
    - [Stage 2.3: Stability Evaluation](#stage-23-stability-evaluation---number_of_thresholds_to_retain_after_stability_evaluation--e_family)
    - [Stage 2.4: Null Model Diagnostic](#stage-24-null-model-diagnostic)
    - [Stage 2.5: Pareto-based Filtering and Parsimony](#stage-25-pareto-based-filtering-and-parsimony)
    - [Stage 2.6: Extrinsic Evaluation](#stage-26-extrinsic-evaluation)
- [(7) Non-overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#7-non-overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
  - [Default Affinity (Adjacency Matrix) + LAPIN-on](#default-affinity-adjacency-matrix--lapin-on)
  - [Default Affinity (Adjacency Matrix) + LAPIN-off](#default-affinity-adjacency-matrix--lapin-off)
  - [Ip_b0 + LAPIN-on](#ip_b0--lapin-on)
  - [Ip_b0 + LAPIN-off](#ip_b0--lapin-off)
  - [CosIp_b0 + LAPIN-on](#cosip_b0--lapin-on)
  - [CosIp_b0 + LAPIN-off](#cosip_b0--lapin-off)
  - [Kul + LAPIN-on](#kul--lapin-on)
  - [Kul + LAPIN-off](#kul--lapin-off)
  - [Dice + LAPIN-on](#dice--lapin-on)
  - [Dice + LAPIN-off](#dice--lapin-off)
  - [Ochiai + LAPIN-on](#ochiai--lapin-on)
  - [Ochiai + LAPIN-off](#ochiai--lapin-off)
- [(8) Overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds](#8-overlapping-communities---network-family-k-boundary-thresholds--network-contribution-boundary-thresholds)
  - [Default Affinity (Adjacency Matrix) + LAPIN-on](#default-affinity-adjacency-matrix--lapin-on-1)
  - [Default Affinity (Adjacency Matrix) + LAPIN-off](#default-affinity-adjacency-matrix--lapin-off-1)
- [(9) Literature Review of Community Detection Results in Networks without Ground-Truth](#9-literature-review-of-community-detection-results-in-networks-without-ground-truth)
  - [Reference Paper - "Modularity and community structure in networks"](#reference-paper---modularity-and-community-structure-in-networks)
  - [Reference Paper - "Community detection in complex networks using Extremal Optimization"](#reference-paper---community-detection-in-complex-networks-using-extremal-optimization)
  - [Reference Paper - "Overlapping community detection using Bayesian non-negative matrix factorization"](#reference-paper---overlapping-community-detection-using-bayesian-non-negative-matrix-factorization)
  - [Reference Paper - "Graph neural network inspired algorithm for unsupervised network community detection"](#reference-paper---graph-neural-network-inspired-algorithm-for-unsupervised-network-community-detection)
  - [Reference Paper - "A three-stage algorithm on community detection in social networks"](#reference-paper---a-three-stage-algorithm-on-community-detection-in-social-networks)
  - [Summary of Literature Reference Results](#summary-of-literature-reference-results)
- [(10) Literature Review of Community Detection Results in Networks with Ground-Truth](#10-literature-review-of-community-detection-results-in-networks-with-ground-truth)
- [(11) Observations](#11-observations)
  - [Comparison of Network Family K-Boundary Thresholds](#comparison-of-network-family-k-boundary-thresholds)
  - [Comparison with Literature Reference Results of the Real-World Networks without Ground-Truth](#comparison-with-literature-reference-results-of-the-real-world-networks-without-ground-truth)
  - [Comparison with Literature Reference Results of the Real-World Networks with Ground-Truth](#comparison-with-literature-reference-results-of-the-real-world-networks-with-ground-truth)


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
- `The network family K-boundary thresholds are not enough due to diversity and heterogeneity of the real-world networks`

## (3) FADDIS Sensitivity Analysis

- `FADDIS sensitivity analysis is necessary to select the properties used to form network families, unlike LFR networks, which leverage prior knowledge from the literature`

### Network Properties (LAPIN-on)

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/train_networks/network_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/test_networks_with_gt/network_properties.csv)
- [Test networks without ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/test_networks_without_gt/network_properties.csv)

### Ground-Truth Properties (LAPIN-on)

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/train_networks/ground_truth_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/test_networks_with_gt/ground_truth_properties.csv)

### FADDIS Correlations (LAPIN-on)

- [Open File](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-21_00-06-25-411658/train_networks/faddis_sensitivity_analysis.csv)

| Ground-Truth Type               | Network Property              | FADDIS Property | #Networks | Spearman Correlation | Pearson Correlation   |
|---------------------------------|-------------------------------|-----------------|-----------|----------------------|-----------------------|
| Non-overlapping and Overlapping | Degree Assortativity          | c_K             | 14        | -0.767032967032967   | -0.7827115029017235   |
| Non-overlapping and Overlapping | Global Clustering Coefficient | c_K             | 14        | -0.665934065934066   | -0.44293166357643315  |
| Non-overlapping and Overlapping | Average Degree                | c_K             | 14        | -0.4945054945054946  | -0.3482019687473264   |
|                                 |                               |                 |           |                      |                       |
| Non-overlapping                 | Degree Assortativity          | c_K             | 7         | -0.8928571428571429  | -0.9176830279543988   |
| Non-overlapping                 | Average Degree                | c_K             | 7         | -0.6071428571428572  | -0.4286907010443401   |
| Non-overlapping                 | Global Clustering Coefficient | c_K             | 7         | -0.5                 | -0.23921174424961072  |
|                                 |                               |                 |           |                      |                       |
| Overlapping                     | Degree Assortativity          | c_K             | 7         | -0.3214285714285715  | 0.33019323930539896   |
| Overlapping                     | Degree Std                    | c_K             | 7         | -0.28571428571428575 | 0.37377667176219176   |
| Overlapping                     | Average Degree                | c_K             | 7         | -0.21428571428571433 | 0.2774095170932811    |
| Overlapping                     | Edges LCC                     | c_K             | 7         | -0.1785714285714286  | 0.5078078373827776    |
| Overlapping                     | Max Degree                    | c_K             | 7         | -0.1785714285714286  | 0.4753208820030245    |
| Overlapping                     | Nodes LCC                     | c_K             | 7         | 0.14285714285714288  | 0.5985070325030003    |
| Overlapping                     | Degree Hub Ratio              | c_K             | 7         | 0.14285714285714288  | 0.2752415698777623    |
| Overlapping                     | Degree CV                     | c_K             | 7         | -0.10714285714285716 | 0.30829148535650897   |
| Overlapping                     | Global Clustering Coefficient | c_K             | 7         | -0.07142857142857144 | -0.15109420759755204  |

- `Only network properties are considered in sensitivity correlations, rather than ground-truth properties, because they are available for all networks`
- `Degree assortativity is clearly the network property most strongly correlated with c_K for the combined, non-overlapping and overlapping ground-truth groups`
- `Average degree exhibits a balanced correlated with c_K for the combined, non-overlapping and overlapping ground-truth groups`

### Network Properties (LAPIN-off)

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/train_networks/network_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/test_networks_with_gt/network_properties.csv)
- [Test networks without ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/test_networks_without_gt/network_properties.csv)

### Ground-Truth Properties (LAPIN-off)

- [Train networks](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/train_networks/ground_truth_properties.csv)
- [Test networks with ground-truth](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/test_networks_with_gt/ground_truth_properties.csv)

### FADDIS Correlations (LAPIN-off)

- [Open File](../../../results/real-world/stage2/experience2/sensitivity/results_2026-07-26_14-08-05-867933/train_networks/faddis_sensitivity_analysis.csv)

| Ground-Truth Type               | Network Property              | FADDIS Property | #Networks | Spearman Correlation  | Pearson Correlation   |
|---------------------------------|-------------------------------|-----------------|-----------|-----------------------|-----------------------|
| Non-overlapping and Overlapping | Degree Assortativity          | c_K             | 11        | -0.6363636363636364   | -0.7899425242612974   |
| Non-overlapping and Overlapping | Global Clustering Coefficient | c_K             | 11        | -0.6000000000000001   | -0.38760373768575995  |
| Non-overlapping and Overlapping | Average Degree                | c_K             | 11        | -0.46363636363636374  | -0.4324586239457222   |
|                                 |                               |                 |           |                       |                       |
| Non-overlapping                 | Degree Assortativity          | c_K             | 6         | -0.942857142857143    | -0.8504803336639603   |
| Non-overlapping                 | Min Degree                    | c_K             | 6         | -0.6982532518267538   | -0.45307746706750557  |
| Non-overlapping                 | Edges LCC                     | c_K             | 6         | -0.6                  | -0.39568649105365006  |
| Non-overlapping                 | Nodes LCC                     | c_K             | 6         | -0.5428571428571429   | -0.35731023756280617  |
| Non-overlapping                 | Average Degree                | c_K             | 6         | -0.5428571428571429   | -0.4832883658153081   |
| Non-overlapping                 | Degree CV                     | c_K             | 6         | 0.48571428571428577   | 0.10859078034035918   |
| Non-overlapping                 | Global Clustering Coefficient | c_K             | 6         | -0.48571428571428577  | -0.1738684802241147   |
|                                 |                               |                 |           |                       |                       |
| Overlapping                     | Degree Assortativity          | c_K             | 5         | 0.8999999999999998    | 0.9729634358506289    |
| Overlapping                     | Average Degree                | c_K             | 5         | 0.7999999999999999    | 0.9278743775775963    |
| Overlapping                     | Density                       | c_K             | 5         | 0.7999999999999999    | 0.07756819167456096   |
| Overlapping                     | Sparsity                      | c_K             | 5         | -0.7999999999999999   | -0.07756819167456087  |
| Overlapping                     | Global Clustering Coefficient | c_K             | 5         | 0.7999999999999999    | 0.31309955544264145   |

- `Again only network properties are considered in sensitivity correlations, rather than ground-truth properties, because they are available for all networks`
- `Again degree assortativity is clearly the network property most strongly correlated with c_K for the combined, non-overlapping and overlapping ground-truth groups`
- `Again average degree exhibits a balanced correlated with c_K for the combined, non-overlapping and overlapping ground-truth groups`

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


## (5) Pipeline Configuration

```json
{
  "affinity_design": "Default",
  "apply_lapin": false,
  "tau": 0.05,
  "k_max_boundary": 500,
  "overlapping_communities": false,
  "defuzzification_gamma": 0.8,
  "number_of_thresholds_to_retain_after_intrinsic_evaluation": 3,
  "number_of_thresholds_to_retain_after_stability_evaluation": 2,
  "near_singleton_boundary": 2,
  "number_of_perturbed_graphs": 10,
  "edge_swap_multiplier_in_perturbed_graphs": 0.05,
  "number_of_null_models": 10,
  "edge_swap_multiplier_in_null_models": 10,
  "pareto_tolerance_fraction_modularity": 0.1,
  "pareto_tolerance_fraction_conductance": 0.1,
  "pareto_tolerance_fraction_stability": 0.15,
  "pareto_largest_community_fraction_boundary": 0.95,
  "pareto_singleton_or_near_singleton_fraction_boundary": 0.5,
  "pareto_null_model_p_value_boundary": 0.1,
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

#### Stage 2.4: Null Model Diagnostic

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

#### Stage 2.5: Pareto-based Filtering and Parsimony

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
      - *Fallback*: Non-degenerate; Highest Modularity; Lowest Conductance; Highest threshold value
  - **Stability Evaluation**
    - *Evaluate*: Acceptable Stability
    - *Filter*: Parsimony Principle (Top-2) over Acceptables
      - *Fallback*: Non-degenerate; Highest Modularity; Lowest Conductance; Highest Stability
  - **Null Model Diagnostic**
    - *Evaluate*: Acceptable Null Model
  - **Pareto-based Filtering and Parsimony**
    - *Select*: Parsimony Principle over Acceptables
      - *Condition*: Retain the $\epsilon_{family}$ if it is practically indistinguishable from the best candidate (acceptable and same k');
      - *Fallback*: Non-degenerate; Highest Modularity; Lowest Conductance; Highest Stability; Highest threshold value

#### Stage 2.6: Extrinsic Evaluation

- For each network with ground-truth and final threshold $\epsilon$:
  - K' | K, |K'-K|/K, AMI, F-measure, ARI, FMI, NMI, VI if not network.overlapping_ground_truth
  - K' | K, |K'-K|/K, ONMI, Omega if network.overlapping_ground_truth


## (7) Non-overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

### Default Affinity (Adjacency Matrix) + LAPIN-on

```json
{
  "affinity_design": "Default",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 13476.537909917999 + 42568.27264089789
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_01-35-02-985213/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_01-35-02-985213/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_01-35-02-985213/test_networks_with_gt/)
- [Test with train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_01-35-02-985213/test_with_train_networks/)


### Default Affinity (Adjacency Matrix) + LAPIN-off

```json
{
  "affinity_design": "Default",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 5106.170760306995 + 9067.550150152761
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_03-15-17-101707/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_03-15-17-101707/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_03-15-17-101707/test_networks_with_gt/)
- [Test with train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_03-15-17-101707/test_with_train_networks/)

### Ip_b0 + LAPIN-on

```json
{
  "affinity_design": "Ip_b0",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 20216.17830928904
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_05-19-39-556936/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_05-19-39-556936/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_05-19-39-556936/test_networks_with_gt/)
- Test with train networks results

### Ip_b0 + LAPIN-off

```json
{
  "affinity_design": "Ip_b0",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 4665.296060502995
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_20-05-55-517321/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_20-05-55-517321/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_20-05-55-517321/test_networks_with_gt/)
- Test with train networks results

### CosIp_b0 + LAPIN-on

```json
{
  "affinity_design": "CosIp_b0",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 24780.44658103492
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_21-23-40-813696/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_21-23-40-813696/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-21_21-23-40-813696/test_networks_with_gt/)
- Test with train networks results

### CosIp_b0 + LAPIN-off

```json
{
  "affinity_design": "CosIp_b0",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 8834.372523091966
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_04-16-41-275586/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_04-16-41-275586/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_04-16-41-275586/test_networks_with_gt/)
- Test with train networks results

### Kul + LAPIN-on

```json
{
  "affinity_design": "Kul",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 21827.662761374144
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_12-45-13-205463/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_12-45-13-205463/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-22_12-45-13-205463/test_networks_with_gt/)
- Test with train networks results

### Kul + LAPIN-off

```json
{
  "affinity_design": "Kul",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 5098.827821595129
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_08-27-39-974371/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_08-27-39-974371/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_08-27-39-974371/test_networks_with_gt/)
- Test with train networks results

### Dice + LAPIN-on

```json
{
  "affinity_design": "Dice",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 20408.998805815354
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_09-52-38-785445/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_09-52-38-785445/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_09-52-38-785445/test_networks_with_gt/)
- Test with train networks results

### Dice + LAPIN-off

```json
{
  "affinity_design": "Dice",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 6559.998357471079
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_15-32-47-785178/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_15-32-47-785178/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-24_15-32-47-785178/test_networks_with_gt/)
- Test with train networks results

### Ochiai + LAPIN-on

```json
{
  "affinity_design": "Ochiai",
  "apply_lapin": true,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 18881.176445811056
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_15-40-23-273023/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_15-40-23-273023/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_15-40-23-273023/test_networks_with_gt/)
- Test with train networks results

### Ochiai + LAPIN-off

```json
{
  "affinity_design": "Ochiai",
  "apply_lapin": false,
  "overlapping_communities": false,
  "execution_elapsed_time_secs": 5610.623681175057
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_20-55-04-450298/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_20-55-04-450298/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-25_20-55-04-450298/test_networks_with_gt/)
- Test with train networks results


## (8) Overlapping Communities - Network Family K-Boundary Thresholds + Network Contribution-Boundary Thresholds

### Default Affinity (Adjacency Matrix) + LAPIN-on

```json
{
  "affinity_design": "Default",
  "apply_lapin": true,
  "overlapping_communities": true,
  "execution_elapsed_time_secs": 19415.325708261924 + 43559.760930565135
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_07-21-37-879275/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_07-21-37-879275/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_07-21-37-879275/test_networks_with_gt/)
- [Test with train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-20_12-17-10-818425-old/train_networks_with_gt/)

### Default Affinity (Adjacency Matrix) + LAPIN-off

```json
{
  "affinity_design": "Default",
  "apply_lapin": false,
  "overlapping_communities": true,
  "execution_elapsed_time_secs": 11053.010993575212
}
```

- [Train networks results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_15-04-51-954365/train_networks/)
- [Test networks without ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_15-04-51-954365/test_networks_without_gt/)
- [Test networks with ground-truth results](../../../results/real-world/stage2/experience2/ths/results_2026-07-26_15-04-51-954365/test_networks_with_gt/)
- Test with train networks results


## (9) Literature Review of Community Detection Results in Networks without Ground-Truth

- Canonical references;
- Table results;
- Same networks without ground-truth;
- Modularity; K'; Conductance;
- Common algorithms.

### Reference Paper - "Modularity and community structure in networks"

- `MEJ Newman`
- `Proceedings of the National Academy of Sciences, 2006`
- `16616 citations`

| Network             | $Q$ (Girvan–Newman)  | $K'$ (Girvan–Newman)  | $Q$ (Fast Greedy) | $K'$ (Fast Greedy) | $Q$ (Extremal Optimization)  | $K'$ (Extremal Optimization)  | $Q$ (Leading Eigenvector) | $K'$ (Leading Eigenvector) |
|---------------------|---------------------:|----------------------:|------------------:|-------------------:|-----------------------------:|------------------------------:|--------------------------:|---------------------------:|
| jazz-musicians      |                0.405 |                     — |             0.439 |                  — |                        0.445 |                             — |                     0.442 |                          — |
| c-elegans-metabolic |                0.403 |                     — |             0.402 |                  — |                        0.434 |                             — |                     0.435 |                          — |
| email-urv           |                0.532 |                     — |             0.494 |                  — |                        0.574 |                             — |                     0.572 |                          — |


### Reference Paper - "Community detection in complex networks using Extremal Optimization"

- `J Duch, A Arenas`
- `Physical Review E—Statistical, Nonlinear, and Soft Matter Physics, 2005`
- `2149 citations`

| Network             | $Q$ (Newman Fast Greedy) | $K'$ (Newman Fast Greedy)   | $Q$ (Extremal Optimization)  | $K'$ (Extremal Optimization)  |
|---------------------|-------------------------:|----------------------------:|-----------------------------:|------------------------------:|
| jazz-musicians      |                   0.4379 |                           4 |                       0.4452 |                             5 |
| c-elegans-metabolic |                   0.4001 |                          10 |                       0.4342 |                            12 |
| email-urv           |                   0.4796 |                          13 |                       0.5738 |                            15 |


### Reference Paper - "Overlapping community detection using Bayesian non-negative matrix factorization"

- `I Psorakis, S Roberts, M Ebden, B Sheldon`
- `Physical Review E—Statistical, Nonlinear, and Soft Matter Physics, 2011`
- `522 citations`

| Network                           | $Q$ (Bayesian NMF) | $K'$ (Bayesian NMF)   | $Q$ (Extremal Optimization)  | $K'$ (Extremal Optimization)  | $Q$ (Louvain) | $K'$ (Louvain) |
|-----------------------------------|-------------------:|----------------------:|-----------------------------:|------------------------------:|--------------:|---------------:|
| dolphins                          |        0.47 ± 0.03 |           6.67 ± 0.83 |                  0.51 ± 0.01 |                      4.00 ± 0 |          0.52 |              5 |
| les-miserables                    |        0.53 ± 0.02 |           9.97 ± 0.78 |                  0.53 ± 0.01 |                   4.96 ± 1.72 |          0.57 |              6 |
| jazz-musicians                    |        0.43 ± 0.01 |           8.57 ± 8.89 |                  0.42 ± 0.01 |                      4.00 ± 0 |          0.44 |              4 |
| c-elegans-metabolic               |        0.36 ± 0.01 |          15.69 ± 1.14 |                  0.40 ± 0.09 |                   7.96 ± 1.06 |          0.43 |             10 |
| co-authorships-in-network-science |        0.83 ± 0.01 |         342.53 ± 5.28 |                  0.86 ± 0.01 |                 58.24 ± 12.36 |          0.95 |            418 |


### Reference Paper - "Graph neural network inspired algorithm for unsupervised network community detection"

- `S Sobolevsky, A Belyi`
- `Applied Network Science, Springer, 2022`
- `47 citations`

| Network                  | $Q$ (ADVNDS) | $K'$ (ADVNDS)  | $Q$ (Leiden) | $K'$ (Leiden)  | $Q$ (Louvain) | $K'$ (Louvain) | $Q$ (Combo) | $K'$ (Combo) | $Q$ (GNNS100) | $K'$ (GNNS100)   | $Q$ (GNNS2500) | $K'$ (GNNS2500)   | $Q$ (GNNS25000) | $K'$ (GNNS25000)   |
|--------------------------|-------------:|---------------:|-------------:|---------------:|--------------:|---------------:|------------:|-------------:|--------------:|-----------------:|---------------:|------------------:|----------------:|-------------------:|
| dolphins                 |     0.528519 |              — |     0.528519 |              — |      0.527728 |              — |    0.526799 |            — |      0.528519 |                — |       0.528519 |                 — |        0.528519 |                  — |
| les-miserables           |     0.566688 |              — |     0.566688 |              — |      0.566688 |              — |    0.566688 |            — |      0.566688 |                — |       0.566688 |                 — |        0.566688 |                  — |
| jazz-musicians           |     0.445144 |              — |     0.445144 |              — |      0.445144 |              — |    0.444469 |            — |      0.445144 |                — |       0.445144 |                 — |        0.445144 |                  — |
| c-elegans-neural-network |     0.503782 |              — |     0.503485 |              — |      0.498211 |              — |    0.503782 |            — |      0.502002 |                — |       0.503736 |                 — |        0.503782 |                  — |
| c-elegans-metabolic      |     0.453248 |              — |     0.452867 |              — |      0.446379 |              — |    0.453209 |            — |      0.441670 |                — |       0.446602 |                 — |        0.448080 |                  — |
| email-urv                |     0.582829 |              — |     0.582636 |              — |      0.577651 |              — |    0.582792 |            — |      0.568329 |                — |       0.576863 |                 — |        0.578422 |                  — |


### Reference Paper - "A three-stage algorithm on community detection in social networks"

- `X You, Y Ma, Z Liu`
- `Knowledge-Based Systems, Elsevier, 2020`
- `107 citations`

| Network          | $Q$ (Three-Stage) | $K'$ (Three-Stage) | $Q$ (Louvain) | $K'$ (Louvain) | $Q$ (Fast Greedy) | $K'$ (Fast Greedy) | $Q$ (Infomap) | $K'$ (Infomap) | $Q$ (Leading Eigenvector) | $K'$ (Leading Eigenvector) | $Q$ (Label Propagation) | $K'$ (Label Propagation) | $Q$ (Walktrap) | $K'$ (Walktrap) |
|------------------|------------------:|-------------------:|--------------:|---------------:|------------------:|-------------------:|--------------:|---------------:|--------------------------:|---------------------------:|------------------------:|-------------------------:|---------------:|----------------:|
| les-miserables   |              0.54 |                  6 |          0.56 |              6 |              0.50 |                  5 |          0.55 |              9 |                      0.53 |                          8 |                    0.55 |                        6 |           0.52 |               8 |
| jazz-musicians   |              0.44 |                  3 |          0.44 |              4 |              0.44 |                  4 |          0.28 |              7 |                      0.39 |                          3 |                    0.28 |                        2 |           0.44 |              11 |
| email-urv        |              0.55 |                  9 |          0.54 |             12 |              0.51 |                 16 |          0.52 |             68 |                      0.49 |                          7 |                    0.28 |                        8 |           0.53 |              49 |

### Summary of Literature Reference Results

| Network                            | Typical \(Q\) Range   | Typical \(K'\) Communities      |
|------------------------------------|----------------------:|--------------------------------:|
| dolphins                           | 0.470000–0.528519     | 4–5; 7                          |
| les-miserables                     | 0.500000–0.570000     | 5–6; 8–10                       |
| jazz-musicians                     | 0.280000–0.445200     | 2–5; 7; 9; 11                   |
| c-elegans-neural-network           | 0.498211–0.503782     | 5                               |
| c-elegans-metabolic                | 0.360000–0.453248     | 8; 10; 12; 16                   |
| email-urv                          | 0.280000–0.582829     | 7–9; 12–13; 15–16; 49; 68       |
| *co-authorships-in-network-science | 0.830000–0.950000     | 58; 343; 418                    |

## (10) Literature Review of Community Detection Results in Networks with Ground-Truth

TODO


## (11) Observations

### Comparison of Network Family K-Boundary Thresholds

| Configuration                     | #Valid Network Thresholds/#Total        |
|-----------------------------------|----------------------------------------:|
| Default + LAPIN-on                | 14/14                                   |
| Default + LAPIN-off               | 10/14                                   |
| Ip_b0 + LAPIN-on                  | 11/14                                   |
| Ip_b0 + LAPIN-off                 | 7/14                                    |
| CosIp_b0 + LAPIN-on               | 14/14                                   |
| CosIp_b0 + LAPIN-off              | 9/14                                    |
| Kul + LAPIN-on                    | 13/14                                   |
| Kul + LAPIN-off                   | 9/14                                    |
| Dice + LAPIN-on                   | 12/14                                   |
| Dice + LAPIN-off                  | 10/14                                   |
| Ochiai + LAPIN-on                 | 14/14                                   |
| Ochiai + LAPIN-off                | 9/14                                    |

### Comparison with Literature Reference Results of the Real-World Networks without Ground-Truth

| Configuration                     | #Acceptbale Thresholds/#Total           |
|-----------------------------------|----------------------------------------:|
| Default + LAPIN-on                | 6/7                                     |
| Default + LAPIN-off               | 4/7                                     |
| Ip_b0 + LAPIN-on                  | 4/7                                     |
| Ip_b0 + LAPIN-off                 | 2/7                                     |
| CosIp_b0 + LAPIN-on               | 5/7                                     |
| CosIp_b0 + LAPIN-off              | 5/7                                     |
| Kul + LAPIN-on                    | 5/7                                     |
| Kul + LAPIN-off                   | 5/7                                     |
| Dice + LAPIN-on                   | 6/7                                     |
| Dice + LAPIN-off                  | 4/7                                     |
| Ochiai + LAPIN-on                 | 5/7                                     |
| Ochiai + LAPIN-off                | 5/7                                     |

---

| Network                           | Literature \(Q\) Range | \(Q\) (Default + LAPIN-on) | \(Q\)  (Default + LAPIN-off) | \(Q\) (Ip_b0 + LAPIN-on) | \(Q\) (Ip_b0 + LAPIN-of) | \(Q\) (CosIp_b0 + LAPIN-on) | \(Q\) (CosIp_b0 + LAPIN-off) | \(Q\) (Kul + LAPIN-on) | \(Q\) (Kul + LAPIN-off) | \(Q\) (Dice + LAPIN-on) | \(Q\) (Dice + LAPIN-off) | \(Q\) (Ochiai + LAPIN-on) | \(Q\) (Ochiai + LAPIN-off) |
|-----------------------------------|------------------------|----------------------------|------------------------------|--------------------------|--------------------------|-----------------------------|------------------------------|------------------------|-------------------------|-------------------------|--------------------------|---------------------------|----------------------------|
| c-elegans-metabolic               | 0.360–0.453            | 0.239                      | 0.340                        | 0.091                    | 0.034                    | 0.089                       | 0.198                        | 0.092                  | 0.199                   | 0.185                   | 0.193                    | 0.089                     | 0.198                      |
| c-elegans-neural-network          | 0.498–0.504            | 0.291                      | 0.336                        | 0.092                    | 0.294                    | 0.180                       | 0.275                        | 0.219                  | 0.244                   | 0.253                   | 0.192                    | 0.229                     | 0.275                      |
| co-authorships-in-network-science | -                      | 0.760                      | 0.776                        | 0.695                    | 0.770                    | 0.763                       | 0.757                        | 0.746                  | 0.748                   | 0.709                   | 0.730                    | 0.763                     | 0.757                      |
| dolphins                          | 0.470–0.529            | 0.385                      | 0.470                        | 0.316                    | 0.488                    | 0.390                       | 0.452                        | 0.390                  | 0.437                   | 0.390                   | 0.478                    | 0.390                     | 0.452                      |
| email-urv                         | 0.280–0.583            | 0.457                      | 0.450                        | 0.482                    | 0.463                    | 0.482                       | 0.490                        | 0.494                  | 0.493                   | 0.449                   | 0.502                    | 0.482                     | 0.490                      |
| jazz-musicians                    | 0.280–0.445            | 0.265                      | 0.377                        | 0.108                    | 0.404                    | 0.328                       | 0.434                        | 0.323                  | 0.432                   | 0.351                   | 0.432                    | 0.328                     | 0.434                      |
| les-miserables                    | 0.500–0.570            | 0.475                      | 0.495                        | 0.357                    | 0.467                    | 0.291                       | 0.456                        | 0.289                  | 0.474                   | 0.330                   | 0.486                    | 0.291                     | 0.456                      |



| Network                           | Literature \(K'\) Range   | \(K'\) (Default + LAPIN-on) | \(K'\)  (Default + LAPIN-off) | \(K'\) (Ip_b0 + LAPIN-on) | \(K'\) (Ip_b0 + LAPIN-of) | \(K'\) (CosIp_b0 + LAPIN-on) | \(K'\) (CosIp_b0 + LAPIN-off) | \(K'\) (Kul + LAPIN-on) | \(K'\) (Kul + LAPIN-off) | \(K'\) (Dice + LAPIN-on) | \(K'\) (Dice + LAPIN-off) | \(K'\) (Ochiai + LAPIN-on) | \(K'\) (Ochiai + LAPIN-off) |
|-----------------------------------|--------------------------:|----------------------------:|------------------------------:|--------------------------:|--------------------------:|-----------------------------:|------------------------------:|------------------------:|-------------------------:|-------------------------:|--------------------------:|---------------------------:|----------------------------:|
| c-elegans-metabolic               | 8; 10; 12; 16             | 44                          | 8                             | 2                         | 5                         | 2                            | 3                             | 2                       | 3                        | 11                       | 3                         | 2                          | 3                           |
| c-elegans-neural-network          | 5                         | 15                          | 5                             | 21                        | 3                         | 15                           | 3                             | 12                      | 3                        | 11                       | 7                         | 14                         | 3                           |
| co-authorships-in-network-science | -                         | 7                           | 22                            | 21                        | 10                        | 14                           | 8                             | 12                      | 8                        | 9                        | 8                         | 14                         | 8                           |
| dolphins                          | 4–5; 7                    | 2                           | 6                             | 14                        | 4                         | 2                            | 5                             | 2                       | 5                        | 2                        | 4                         | 2                          | 5                           |
| email-urv                         | 7–9; 12–13; 15–16; 49; 68 | 11                          | 6                             | 44                        | 6                         | 15                           | 9                             | 11                      | 5                        | 11                       | 6                         | 15                         | 9                           |
| jazz-musicians                    | 2–5; 7; 9; 11             | 23                          | 5                             | 37                        | 4                         | 17                           | 4                             | 19                      | 4                        | 16                       | 4                         | 17                         | 4                           |
| les-miserables                    | 5–6; 8–10                 | 5                           | 9                             | 3                         | 4                         | 3                            | 8                             | 5                       | 7                        | 3                        | 7                         | 3                          | 8                           |

### Comparison with Literature Reference Results of the Real-World Networks with Ground-Truth

TODO
