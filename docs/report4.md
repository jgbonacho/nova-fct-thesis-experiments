# Report 4 - Question: Does the relative contribution to data scatter provide a good hyperparameter for the definition of the stop rules under variations in the structure/architecture parameters of real-world networks?



## Table of Contents

- [Real-World Networks with Ground-truth](#real-world-networks-with-ground-truth)
- [Experience 1 (All networks in the same family)](#experience-1-all-networks-in-the-same-family)
  - [Network Family 0](#network-family-0)
- [Experience 2 (Networks grouped by ground-truth type)](#experience-2-networks-grouped-by-ground-truth-type)
  - [Network Family 1 (Non-Overlapping)](#network-family-1-non-overlapping)
  - [Network Family 2 (Overlapping)](#network-family-2-overlapping)
- [Experience 3 (Networks grouped by ground-truth type and K range)](#experience-3-networks-grouped-by-ground-truth-type-and-k-range)
  - [Network Family 1 (Non-Overlapping + K $\in$ [2, 9])](#network-family-1-non-overlapping--k-in-2-9)
  - [Network Family 2 (Non-Overlapping + K $\in$ [10, 19])](#network-family-2-non-overlapping--k-in-10-19)
  - [Network Family 3 (Non-Overlapping + K $\in$ [40, 49])](#network-family-3-non-overlapping--k-in-40-49)
  - [Network Family 4 (Overlapping + K $\in$ [2, 9])](#network-family-4-overlapping--k-in-2-9)
  - [Network Family 5 (Overlapping + K $\in$ [10, 19])](#network-family-5-overlapping--k-in-10-19)
  - [Network Family 6 (Overlapping + K $\in$ [20, 29])](#network-family-6-overlapping--k-in-20-29)
  - [Network Family 7 (Overlapping + K $\in$ [30, 39])](#network-family-7-overlapping--k-in-30-39)
  - [Network Family 8 (Overlapping + K $\in$ [40, 49])](#network-family-8-overlapping--k-in-40-49)
- [Experience 4 (Networks grouped by ground-truth type and the proportion of communities relative to the number of nodes)](#experience-4-networks-grouped-by-ground-truth-type-and-the-proportion-of-communities-relative-to-the-number-of-nodes)
  - [Network Family 1 (Non-Overlapping + Low Community Proportion (p < 0.03))](#network-family-1-non-overlapping--low-community-proportion-p--003)
  - [Network Family 2 (Non-Overlapping + Medium Community Proportion (0.03 < p < 0.07))](#network-family-2-non-overlapping--medium-community-proportion-003--p--007)
  - [Network Family 3 (Non-Overlapping + High Community Proportion (p > 0.07))](#network-family-3-non-overlapping--high-community-proportion-p--007)
  - [Network Family 4 (Overlapping + Low Community Proportion (p < 0.03))](#network-family-4-overlapping--low-community-proportion-p--003)
  - [Network Family 5 (Overlapping + Medium Community Proportion (0.03 < p < 0.07))](#network-family-5-overlapping--medium-community-proportion-003--p--007)
  - [Network Family 6 (Overlapping + High Community Proportion (p > 0.07))](#network-family-6-overlapping--high-community-proportion-p--007)
- [Experience 5 (Networks grouped by ground-truth type and average degree)](#experience-5-networks-grouped-by-ground-truth-type-and-average-degree)
  - [Network Family 1 (Non-Overlapping + Low Average Degree (a < 15))](#network-family-1-non-overlapping--low-average-degree-a--15)
  - [Network Family 2 (Non-Overlapping + Medium Average Degree (15 < a < 35))](#network-family-2-non-overlapping--medium-average-degree-15--a--35)
  - [Network Family 3 (Overlapping + Low Average Degree (a < 15))](#network-family-3-overlapping--low-average-degree-a--15)
  - [Network Family 4 (Overlapping + Medium Average Degree (15 < a < 35))](#network-family-4-overlapping--medium-average-degree-15--a--35)
  - [Network Family 5 (Overlapping + High Average Degree (a > 35))](#network-family-5-overlapping--high-average-degree-a--35)
- [Experience 6 (One network per family)](#experience-6-one-network-per-family)
  - [Network Family 1](#network-family-1)
  - [Network Family 2](#network-family-2)
  - [Network Family 3](#network-family-3)
  - [Network Family 4](#network-family-4)
  - [Network Family 5](#network-family-5)
  - [Network Family 6](#network-family-6)
  - [Network Family 7](#network-family-7)
  - [Network Family 8](#network-family-8)
  - [Network Family 9](#network-family-9)
  - [Network Family 10](#network-family-10)
  - [Network Family 11](#network-family-11)
  - [Network Family 12](#network-family-12)
  - [Network Family 13](#network-family-13)
  - [Network Family 14](#network-family-14)
  - [Network Family 15](#network-family-15)


## Real-World Networks with Ground-truth

- Pre-processed to **undirected, unweighted simple graphs without self-loops**, saved as .gml files.

| Network                                                                                                                                                                                 | Ground-Truth? | Nodes | Edges | CC  | Nodes LCC | Edges LCC | Nodes without Community |  Overlapping Ground-Truth? | K in LCC  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|-------|-------|-----|-----------|-----------|-------------------------|----------------------------|-----------|
| Zachary Karate Club [[1](https://networkx.org/documentation/stable/reference/generated/networkx.generators.social.karate_club_graph.html)] [[2](https://networks.skewed.de/net/karate)] | Yes           | 34    | 78    | 1   | 34        | 78        | 0                       | No                         | 2         |
| US Political Blogs [[3](https://websites.umich.edu/~mejn/netdata/)] [[4](https://networks.skewed.de/net/polblogs)]                                                                      | Yes           | 1490  | 16715 | 268 | 1222      | 16714     | 0                       | No                         | 2         |
| Books about US Politics [[3](https://websites.umich.edu/~mejn/netdata/)] [[5](https://networks.skewed.de/net/polbooks)]                                                                 | Yes           | 105   | 441   | 1   | 105       | 441       | 0                       | No                         | 3         |
| American College Football [[3](https://websites.umich.edu/~mejn/netdata/)] [[6](https://networks.skewed.de/net/football)]                                                               | Yes           | 115   | 613   | 1   | 115       | 613       | 0                       | No                         | 12        |
| E-mail EU Core [[7](https://snap.stanford.edu/data/email-Eu-core.html/)] [[8](https://networks.skewed.de/net/email_eu)]*                                                                | Yes           | 1005  | 16064 | 20  | 986       | 16064     | 0                       | No                         | 42        |
| Facebook Ego-414 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                    | Yes           | 150   | 1693  | 2   | 148       | 1692      | 14                      | Yes                        | 7         |
| Facebook Ego-107 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                    | Yes           | 1034  | 26749 | 1   | 1034      | 26749     | 554                     | Yes                        | 9         |
| Facebook Ego-698 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                    | Yes           | 61    | 270   | 3   | 40        | 220       | 8                       | Yes                        | 9         |
| Facebook Ego-3980 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                   | Yes           | 52    | 146   | 4   | 44        | 138       | 0                       | Yes                        | 11        |
| Facebook Ego-348 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                    | Yes           | 224   | 3192  | 1   | 224       | 3192      | 6                       | Yes                        | 14        |
| Facebook Ego-686 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                    | Yes           | 168   | 1656  | 1   | 168       | 1656      | 0                       | Yes                        | 14        |
| Facebook Ego-1684 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                   | Yes           | 786   | 14024 | 4   | 775       | 14006     | 22                      | Yes                        | 17        |
| Facebook Ego-0 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                      | Yes           | 333   | 2519  | 5   | 324       | 2514      | 56                      | Yes                        | 22        |
| Facebook Ego-3437 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                   | Yes           | 534   | 4813  | 2   | 532       | 4812      | 435                     | Yes                        | 32        |
| Facebook Ego-1912 Network [[9](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                                                                   | Yes           | 747   | 30025 | 2   | 744       | 30023     | 41                      | Yes                        | 45        |

| Network                | Reason                                             |
|------------------------|----------------------------------------------------|
| Dolphin Social Network | Ground-truth labels require further interpretation |
| LastFM Asia            | Very large network                                 |



## Experience 1 (All networks in the same family)

[Open Folder](../results/real-world/experience1/)

### Network Family 0

| Network                   |
|---------------------------|
| Zachary Karate Club       |
| US Political Blogs        |
| Books about US Politics   |
| American College Football |
| E-mail EU Core            |
| Facebook Ego-414 Network  |
| Facebook Ego-107 Network  |
| Facebook Ego-698 Network  |
| Facebook Ego-3980 Network |
| Facebook Ego-348 Network  |
| Facebook Ego-686 Network  |
| Facebook Ego-1684 Network |
| Facebook Ego-0 Network    |
| Facebook Ego-3437 Network |
| Facebook Ego-1912 Network |



## Experience 2 (Networks grouped by ground-truth type)

[Open Folder](../results/real-world/experience2/)

### Network Family 1 (Non-Overlapping)

| Network                   | Overlapping Ground-Truth? |
|---------------------------|---------------------------|
| Zachary Karate Club       | No                        |
| US Political Blogs        | No                        |
| Books about US Politics   | No                        |
| American College Football | No                        |
| E-mail EU Core            | No                        |

### Network Family 2 (Overlapping)

| Network                   | Overlapping Ground-Truth? |
|---------------------------|---------------------------|
| Facebook Ego-414 Network  | Yes                       |
| Facebook Ego-107 Network  | Yes                       |
| Facebook Ego-698 Network  | Yes                       |
| Facebook Ego-3980 Network | Yes                       |
| Facebook Ego-348 Network  | Yes                       |
| Facebook Ego-686 Network  | Yes                       |
| Facebook Ego-1684 Network | Yes                       |
| Facebook Ego-0 Network    | Yes                       |
| Facebook Ego-3437 Network | Yes                       |
| Facebook Ego-1912 Network | Yes                       |



## Experience 3 (Networks grouped by ground-truth type and K range)

[Open Folder](../results/real-world/experience3/)

### Network Family 1 (Non-Overlapping + K $\in$ [2, 9])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Zachary Karate Club       | No                        | 2         |
| US Political Blogs        | No                        | 2         |
| Books about US Politics   | No                        | 3         |

### Network Family 2 (Non-Overlapping + K $\in$ [10, 19])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| American College Football | No                        | 12        |

### Network Family 3 (Non-Overlapping + K $\in$ [40, 49])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| E-mail EU Core            | No                        | 42        |

### Network Family 4 (Overlapping + K $\in$ [2, 9])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Facebook Ego-414 Network  | Yes                       | 7         |
| Facebook Ego-107 Network  | Yes                       | 9         |
| Facebook Ego-698 Network  | Yes                       | 9         |

### Network Family 5 (Overlapping + K $\in$ [10, 19])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Facebook Ego-3980 Network | Yes                       | 11        |
| Facebook Ego-348 Network  | Yes                       | 14        |
| Facebook Ego-686 Network  | Yes                       | 14        |
| Facebook Ego-1684 Network | Yes                       | 17        |

### Network Family 6 (Overlapping + K $\in$ [20, 29])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Facebook Ego-0 Network    | Yes                       | 22        |

### Network Family 7 (Overlapping + K $\in$ [30, 39])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Facebook Ego-3437 Network | Yes                       | 32        |

### Network Family 8 (Overlapping + K $\in$ [40, 49])

| Network                   | Overlapping Ground-Truth? | K in LCC  |
|---------------------------|---------------------------|-----------|
| Facebook Ego-1912 Network | Yes                       | 45        |



## Experience 4 (Networks grouped by ground-truth type and the proportion of communities relative to the number of nodes)

[Open Folder](../results/real-world/experience4/)

### Network Family 1 (Non-Overlapping + Low Community Proportion (p < 0.03))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| US Political Blogs        | No                        | 2 / 1222 = 0.0016          |
| Books about US Politics   | No                        | 3 / 105 = 0.0286           |

### Network Family 2 (Non-Overlapping + Medium Community Proportion (0.03 < p < 0.07))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| E-mail EU Core            | No                        | 42 / 986 = 0.0426          |
| Zachary Karate Club       | No                        | 2 / 34 = 0.0588            |

### Network Family 3 (Non-Overlapping + High Community Proportion (p > 0.07))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| American College Football | No                        | 12 / 115 = 0.1043          |

### Network Family 4 (Overlapping + Low Community Proportion (p < 0.03))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| Facebook Ego-107 Network  | Yes                       | 9 / 1034 = 0.0087          |
| Facebook Ego-1684 Network | Yes                       | 17 / 775 = 0.0219          |

### Network Family 5 (Overlapping + Medium Community Proportion (0.03 < p < 0.07))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| Facebook Ego-414 Network  | Yes                       | 7 / 148 = 0.0473           |
| Facebook Ego-3437 Network | Yes                       | 32 / 532 = 0.0602          |
| Facebook Ego-1912 Network | Yes                       | 45 / 744 = 0.0605          |
| Facebook Ego-348 Network  | Yes                       | 14 / 224 = 0.0625          |
| Facebook Ego-0 Network    | Yes                       | 22 / 324 = 0.0679          |

### Network Family 6 (Overlapping + High Community Proportion (p > 0.07))

| Network                   | Overlapping Ground-Truth? | p = (K in LCC / Nodes LCC) |
|---------------------------|---------------------------|----------------------------|
| Facebook Ego-686 Network  | Yes                       | 14 / 168 = 0.0833          |
| Facebook Ego-698 Network  | Yes                       | 9 / 40 = 0.2250            |
| Facebook Ego-3980 Network | Yes                       | 11 / 44 = 0.2500           |

- **NOTES**:
    - Low p means the network has few communities compared with its number of nodes. So, communities are expected to be larger on average.
    - High p means the network has many communities compared with its number of nodes. So, communities are expected to be smaller on average.



## Experience 5 (Networks grouped by ground-truth type and average degree)

[Open Folder](../results/real-world/experience5/)

### Network Family 1 (Non-Overlapping + Low Average Degree (a < 15))

| Network                   | Overlapping Ground-Truth? | a = (2*Edges LCC / Nodes LCC) |
|---------------------------|---------------------------|-------------------------------|
| Zachary Karate Club       | No                        | 156 / 34 = 4.5882             |
| Books about US Politics   | No                        | 882 / 105 = 8.4000            |
| American College Football | No                        | 1226 / 115 = 10.6609          |

### Network Family 2 (Non-Overlapping + Medium Average Degree (15 < a < 35))

| Network                   | Overlapping Ground-Truth? | a = (2*Edges LCC / Nodes LCC) |
|---------------------------|---------------------------|-------------------------------|
| US Political Blogs        | No                        | 33428 / 1222 = 27.3552        |
| E-mail EU Core            | No                        | 32128 / 986 = 32.5842         |

### Network Family 3 (Overlapping + Low Average Degree (a < 15))

| Network                   | Overlapping Ground-Truth? | a = (2*Edges LCC / Nodes LCC) |
|---------------------------|---------------------------|-------------------------------|
| Facebook Ego-3980 Network | Yes                       | 276 / 44 = 6.2727             |
| Facebook Ego-698 Network  | Yes                       | 440 / 40 = 11.0000            |

### Network Family 4 (Overlapping + Medium Average Degree (15 < a < 35))

| Network                   | Overlapping Ground-Truth? | a = (2*Edges LCC / Nodes LCC) |
|---------------------------|---------------------------|-------------------------------|
| Facebook Ego-0 Network    | Yes                       | 5028 / 324 = 15.5185          |
| Facebook Ego-3437 Network | Yes                       | 9624 / 532 = 18.0902          |
| Facebook Ego-686 Network  | Yes                       | 3312 / 168 = 19.7143          |
| Facebook Ego-414 Network  | Yes                       | 3384 / 148 = 22.8649          |
| Facebook Ego-348 Network  | Yes                       | 6384 / 224 = 28.5000          |

### Network Family 5 (Overlapping + High Average Degree (a > 35))

| Network                   | Overlapping Ground-Truth? | a = (2*Edges LCC / Nodes LCC) |
|---------------------------|---------------------------|-------------------------------|
| Facebook Ego-1684 Network | Yes                       | 28012 / 775 = 36.1445         |
| Facebook Ego-107 Network  | Yes                       | 53498 / 1034 = 51.7389        |
| Facebook Ego-1912 Network | Yes                       | 60046 / 744 = 80.7070         |



## Experience 6 (One network per family)

[Open Folder](../results/real-world/experience6/)

### Network Family 1

| Network                   |
|---------------------------|
| Zachary Karate Club       |

### Network Family 2

| Network                   |
|---------------------------|
| US Political Blogs        |

### Network Family 3

| Network                   |
|---------------------------|
| Books about US Politics   |

### Network Family 4

| Network                   |
|---------------------------|
| American College Football |

### Network Family 5

| Network                   |
|---------------------------|
| E-mail EU Core            |

### Network Family 6

| Network                   |
|---------------------------|
| Facebook Ego-414 Network  |

### Network Family 7

| Network                   |
|---------------------------|
| Facebook Ego-107 Network  |

### Network Family 8

| Network                   |
|---------------------------|
| Facebook Ego-698 Network  |

### Network Family 9

| Network                   |
|---------------------------|
| Facebook Ego-3980 Network |

### Network Family 10

| Network                   |
|---------------------------|
| Facebook Ego-348 Network  |

### Network Family 11

| Network                   |
|---------------------------|
| Facebook Ego-686 Network  |

### Network Family 12

| Network                   |
|---------------------------|
| Facebook Ego-1684 Network |

### Network Family 13

| Network                   |
|---------------------------|
| Facebook Ego-0 Network    |

### Network Family 14

| Network                   |
|---------------------------|
| Facebook Ego-3437 Network |

### Network Family 15

| Network                   |
|---------------------------|
| Facebook Ego-1912 Network |
