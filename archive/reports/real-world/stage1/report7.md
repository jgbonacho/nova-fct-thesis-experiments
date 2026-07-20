# Report 7 - Checkpoint

## Pipeline

### LAPIN-on Median Normalized Contributions

`Median of the normalized contributions for each network family, where each contribution is normalized by the global sum of all contributions across all networks and all families, under the LAPIN-on and extraction of K clusters configuration`

### LAPIN-on Median K Boundary Raw Contributions

`Median of the geometric means between the K-th and (K+1)-th normalized contributions for each network family multiplied by the global sum, computed only when the K-th contribution is greater than the (K+1)-th contribution, where each contribution is normalized by the global sum of all contributions across all networks and all families, under the LAPIN-on configuration`

## Real-World Networks

### Network Selection and Division

- Pre-processed to **undirected, unweighted simple graphs without self-loops**, saved as .gml files.

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
| Word Adjacencies [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                          | Language                          | Yes           | 112   | 425   | 1   | 112       | 425       | 1.0000            | No                        | 2      | Test  |
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


#### Legend:

- **Network**: Name of the network.
- **Knowledge Domain**: The domain to which the network belongs.
- **Ground-Truth?**: Indicates whether the network has ground-truth community labels.
- **Nodes**: Number of nodes in the original network.
- **Edges**: Number of edges in the original network.
- **CC**: Number of connected components.
- **Nodes LCC**: Number of nodes in the largest connected component.
- **Edges LCC**: Number of edges in the largest connected component.
- **Relative Size LCC**: Proportion of nodes that belong to the largest connected component, computed as `Nodes LCC / Nodes`.
- **Overlapping Ground-Truth?**: Indicates whether nodes can belong to more than one ground-truth community.
- **K LCC**: Number of ground-truth communities represented in the largest connected component.
- **Set**: Indicates whether the network is part of the training set or the test set.

### Network Properties (Structural and Ground-Truth)

### Train Networks

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-06-21-764261/network_properties.csv)

### Test Networks

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-06-01_16-03-37-120532/network_properties.csv)

#### Legend:

- **Network**: Name of the network.
- **Ground-Truth?**: Indicates whether the network has ground-truth community labels.
- **Nodes LCc**: Number of nodes in the largest connected component.
- **Edges LCC**: Number of edges in the largest connected component.
- **Min Degree**: Minimum node degree in the network.
- **Max Degree**: Maximum node degree in the network.
- **Average Degree**: Average node degree in the network.
- **Degree Std**: Standard deviation of node degrees.
- **Degree CV**: Coefficient of variation of node degrees, computed as `Degree Std / Average Degree`.
- **Degree Hub Ratio**: Ratio between the maximum degree and the average degree, computed as `Max Degree / Average Degree`.
- **Density**: Proportion of existing edges relative to all possible edges.
- **Sparsity**: Proportion of missing edges relative to all possible edges, computed as `1 - Density`.
- **Global Clustering Coefficient**: Global tendency of nodes to form triangles, computed using transitivity.
- **Degree Assortativity**: Correlation between the degrees of connected nodes.
- **Average Clustering**: Average local clustering coefficient over all nodes.
- **Overlapping Ground-Truth?**: Indicates whether nodes can belong to more than one ground-truth community.
- **Overlap Fraction**: Fraction of labeled nodes that belong to more than one ground-truth community.
- **K**: Number of ground-truth communities represented in the network.
- **Community Proportion**: Proportion of communities relative to the number of nodes, computed as `K / Nodes`.
- **Min Community Size**: Size of the smallest ground-truth community.
- **Max Community Size**: Size of the largest ground-truth community.
- **Average Community Size**: Average size of the ground-truth communities.
- **Community Size Std**: Standard deviation of ground-truth community sizes.
- **Community Size CV**: Coefficient of variation of community sizes, computed as `Community Size Std / Average Community Size`.
- **Nodes Without Community**: Number of nodes without ground-truth community labels.
- **Nodes Fraction Without Community**: Fraction of nodes without ground-truth community labels, computed as `Nodes Without Community / Nodes`.

## Sensitivity Analysis

### LAPIN-on Median Normalized Contributions

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-06-21-764261/faddis_sensitivity_correlations.csv)

### LAPIN-on Median K Boundary Raw Contributions

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-13-24-576635/faddis_sensitivity_correlations.csv)

## Networks grouped by degree assortativity and average degree

### Range Definitions

#### Degree Assortativity (Primary)

| Category       | Range                |
|----------------|----------------------|
| Disassortative | `r < -0.10`          |
| Near-Neutral   | `-0.10 <= r < 0.10`  |
| Assortative    | `r >= 0.10`          |

#### Average Degree (Secondary)

| Category                  | Range          |
|---------------------------|----------------|
| Low Average Degree        | `a < 15`       |
| Medium Average Degree     | `15 <= a < 35` |
| Large Average Degree      | `35 <= a < 65` |
| Very Large Average Degree | `a >= 65`      |

---

### Network Families

| Combination                                      | Name             |
|--------------------------------------------------|------------------|
| Disassortative + Low Average Degree              | Network Family 1 |
| Disassortative + Medium Average Degree           | Network Family 2 |
| Disassortative + Large Average Degree            | -                |
| Disassortative + Very Large Average Degree       | -                |
| Near-Neutral + Low Average Degree                | Network Family 3 |
| Near-Neutral + Medium Average Degree             | Network Family 4 |
| Near-Neutral + Large Average Degree              | -                |
| Near-Neutral + Very Large Average Degree         | -                |
| Assortative + Low Average Degree                 | Network Family 5 |
| Assortative + Medium Average Degree              | Network Family 6 |
| Assortative + Large Average Degree               | Network Family 7 |
| Assortative + Very Large Average Degree          | Network Family 8 |

### Network Family 1 (Disassortative + Low Average Degree)

#### Range
- Disassortative: `r < -0.10`
- Low Average Degree: `a < 15`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| zachary-karate-club     | Train | 4.5882         | -0.4756              |
| books-about-us-politics | Train | 8.4000         | -0.1279              |

### Network Family 2 (Disassortative + Medium Average Degree)

#### Range
- Disassortative: `r < -0.10`
- Medium Average Degree: `15 <= a < 35`

| Network            | Set   | Average Degree | Degree Assortativity |
|--------------------|-------|----------------|----------------------|
| us-political-blogs | Train | 27.3552        | -0.2213              |

### Network Family 3 (Near-Neutral + Low Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| cora                    | Train | 4.0797         | -0.0714              |
| facebook-network-ego698 | Train | 11.0000        | 0.0125               |

### Network Family 4 (Near-Neutral + Medium Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`

| Network       | Set   | Average Degree | Degree Assortativity |
|---------------|-------|----------------|----------------------|
| email-eu-core | Train | 32.5842        | -0.0257              |

### Network Family 5 (Assortative + Low Average Degree)

#### Range
- Assortative: `r >= 0.10`
- Low Average Degree: `a < 15`

| Network                   | Set   | Average Degree | Degree Assortativity |
|---------------------------|-------|----------------|----------------------|
| american-college-football | Train | 10.6609        | 0.1624               |

### Network Family 6 (Assortative + Medium Average Degree)

#### Range
- Assortative: `r >= 0.10`
- Medium Average Degree: `15 <= a < 35`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego0    | Train | 15.5185        | 0.2330               |
| facebook-network-ego3437 | Train | 18.0902        | 0.2221               |
| facebook-network-ego414  | Train | 22.8649        | 0.3039               |

### Network Family 7 (Assortative + Large Average Degree)

#### Range
- Assortative: `r >= 0.10`
- Large Average Degree: `35 <= a < 65`

| Network                            | Set   | Average Degree | Degree Assortativity |
|------------------------------------|-------|----------------|----------------------|
| facebook-network-ego1684           | Train | 36.1445        | 0.3268               |
| socio-patterns-primary-school-day1 | Train | 49.9915        | 0.1729               |
| facebook-network-ego107            | Train | 51.7389        | 0.4316               |

### Network Family 8 (Assortative + Very Large Average Degree)

#### Range
- Assortative: `r >= 0.10`
- Very Large Average Degree: `a >= 65`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego1912 | Train | 80.7070        | 0.5026               |

---

### LAPIN-on Median Normalized Contributions Thresholds

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-06-21-764261/thresholds.csv)

### LAPIN-on Median K Boundary Raw Contributions Thresholds

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-13-24-576635/k_boundary_thresholds_by_network.csv)

[Open File](../../../results/real-world/stage1/_checkpoint/results_2026-05-31_22-13-24-576635/thresholds.csv)

## Test Networks Assignment

| Network                            | Average Degree | Degree Assortativity | Combination                          | Assigned Family     | Calibrated? |
|------------------------------------|----------------|----------------------|--------------------------------------|---------------------|-------------|
| word-adjacencies                   | 7.5893         | -0.1293              | Disassortative + Low Average Degree  | `network_family_01` | Yes         |
| socio-patterns-primary-school-day2 | 46.5462        | 0.2168               | Assortative + Large Average Degree   | `network_family_07` | Yes         |
| citeseer                           | 3.4768         | 0.0071               | Near-Neutral + Low Average Degree    | `network_family_03` | Yes         |
| facebook-network-ego3980           | 6.2727         | 0.0530               | Near-Neutral + Low Average Degree    | `network_family_03` | Yes         |
| facebook-network-ego686            | 19.7143        | 0.0841               | Near-Neutral + Medium Average Degree | `network_family_04` | Yes         |
| facebook-network-ego348            | 28.5000        | 0.2227               | Assortative + Medium Average Degree  | `network_family_06` | Yes         |
| dolphins                           | 5.1290         | -0.0436              | Near-Neutral + Low Average Degree    | `network_family_03` | Yes         |
| les-miserables                     | 6.5974         | -0.1652              | Disassortative + Low Average Degree  | `network_family_01` | Yes         |
| jazz-musicians                     | 27.6970        | 0.0202               | Near-Neutral + Medium Average Degree | `network_family_04` | Yes         |
| c-elegans-neural-network           | 14.4646        | -0.1632              | Disassortative + Low Average Degree  | `network_family_01` | Yes         |
| c-elegans-metabolic                | 8.9404         | -0.2258              | Disassortative + Low Average Degree  | `network_family_01` | Yes         |
| email-urv                          | 9.6222         | 0.0782               | Near-Neutral + Low Average Degree    | `network_family_03` | Yes         |
| co-authorships-in-network-science  | 4.8232         | -0.0817              | Near-Neutral + Low Average Degree    | `network_family_03` | Yes         |


## Discussion

- **Observations**
  - The results are not sufficiently strong to be considered final.

- **Warnings**
  - The families do not contain the same number of networks;
  - The total number of networks is small.

- **TODO**
  - [DONE [Report 8](../stage2/report8.md)] A new experimental protocol for FADDIS threshold selection is required.
