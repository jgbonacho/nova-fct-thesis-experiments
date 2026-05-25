# Report 6 - Add more networks and divide into train and test sets



## Table of Contents

- [Real-World Networks](#real-world-networks)
- [Scripts](#scripts)
- [Experience 9 (One network per family)](#experience-9-one-network-per-family)
- [Experience 10 (Networks grouped by degree assortativity, average degree, and K)](#experience-10-networks-grouped-by-degree-assortativity-average-degree-and-k)
- [Experience 11 (Networks grouped by degree assortativity, average degree)](#experience-11-networks-grouped-by-degree-assortativity-and-average-degree)
- [Experience 12](#experience-12)
- [Experience 13 (Networks grouped by ground-truth type, degree assortativity, and average degree)](#experience-13-networks-grouped-by-ground-truth-type-degree-assortativity-and-average-degree)



## Real-World Networks

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
| Word Adjacencies [[2](https://websites.umich.edu/~mejn/netdata/)]                                                                          | Language                          | Yes           | 112   | 425   | 1   | 112       | 425       | 1.0000            | No                        | 2      | Test  |
| SocioPatterns Primary School day 2 [[3](https://sociopatterns.org/datasets/primary-school-cumulative-networks/)]                           | Human Contact                     | Yes           | 238   | 5539  | 1   | 238       | 5539      | 1.0000            | No                        | 11     | Test  |
| CiteSeer [[5](https://web.archive.org/web/20151007064508/http://linqs.cs.umd.edu/projects/projects/lbc/)]                                  | Scientific Citation               | Yes           | 3312  | 4536  | 438 | 2110      | 3668      | 0.6371            | No                        | 6      | Test  |

| Network                                                                                                                                    | Knowledge Domain                  | Ground-Truth? | Nodes | Edges | CC  | Nodes LCC | Edges LCC | Relative Size LCC | Overlapping Ground-Truth? | K LCC  | Set   |
|--------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|---------------|-------|-------|-----|-----------|-----------|-------------------|---------------------------|--------|-------|
| Facebook Ego-698 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 61    | 270   | 3   | 40        | 220       | 0.6557            | Yes                       | 9      | Train |
| Facebook Ego-414 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 150   | 1693  | 2   | 148       | 1692      | 0.9867            | Yes                       | 7      | Train |
| Facebook Ego-0 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                         | Online Social                     | Yes           | 333   | 2519  | 5   | 324       | 2514      | 0.9730            | Yes                       | 22     | Train |
| Facebook Ego-3437 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 534   | 4813  | 2   | 532       | 4812      | 0.9963            | Yes                       | 32     | Train |
| Facebook Ego-1684 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 786   | 14024 | 4   | 775       | 14006     | 0.9860            | Yes                       | 17     | Train |
| Facebook Ego-1912 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 747   | 30025 | 2   | 744       | 30023     | 0.9960            | Yes                       | 45     | Train |
| Facebook Ego-107 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 1034  | 26749 | 1   | 1034      | 26749     | 1.0000            | Yes                       | 9      | Train |
| Facebook Ego-348 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 224   | 3192  | 1   | 224       | 3192      | 1.0000            | Yes                       | 14     | Test  |
| Facebook Ego-3980 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 52    | 146   | 4   | 44        | 138       | 0.8462            | Yes                       | 11     | Test  |
| Facebook Ego-686 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 168   | 1656  | 1   | 168       | 1656      | 1.0000            | Yes                       | 14     | Test  |

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

| Network                            | Ground-Truth? | Nodes LCC | Edges LCC | Min Degree | Max Degree | Average Degree     | Degree Std         | Degree CV           | Degree Hub Ratio   | Density               | Sparsity           | Global Clustering Coefficient | Degree Assortativity  | Average Clustering  | Overlapping Ground-Truth? | Overlap Fraction     | K  | Community Proportion  | Min Community Size | Max Community Size | Average Community Size | Community Size Std | Community Size CV   | Nodes Without Community | Nodes Fraction Without Community |
|------------------------------------|---------------|-----------|-----------|------------|------------|--------------------|--------------------|---------------------|--------------------|-----------------------|--------------------|-------------------------------|-----------------------|---------------------|---------------------------|----------------------|----|-----------------------|--------------------|--------------------|------------------------|--------------------|---------------------|-------------------------|----------------------------------|
| zachary-karate-club                | True          | 34        | 78        | 1.0        | 17.0       | 4.588235294117647  | 3.8778129345135013 | 0.8451643575221734  | 3.7051282051282053 | 0.13903743315508021   | 0.8609625668449198 | 0.2556818181818182            | -0.47561309768461413  | 0.5706384782076823  | False                     | 0.0                  | 2  | 0.058823529411764705  | 17.0               | 17.0               | 17.0                   | 0.0                | 0.0                 | 0                       | 0.0                              |
| books-about-us-politics            | True          | 105       | 441       | 2.0        | 25.0       | 8.4                | 5.474767293965737  | 0.6517580111863972  | 2.9761904761904763 | 0.08076923076923077   | 0.9192307692307692 | 0.34840315221899626           | -0.1278960096667189   | 0.4875267912317313  | False                     | 0.0                  | 3  | 0.02857142857142857   | 13.0               | 49.0               | 35.0                   | 19.28730152198591  | 0.551065757771026   | 0                       | 0.0                              |
| american-college-football          | True          | 115       | 613       | 7.0        | 12.0       | 10.660869565217391 | 0.8874065952502659 | 0.08323960722168074 | 1.1256117455138663 | 0.0935163996948894    | 0.9064836003051107 | 0.4072398190045249            | 0.16244224957444287   | 0.403216011042098   | False                     | 0.0                  | 12 | 0.10434782608695652   | 5.0                | 13.0               | 9.583333333333334      | 2.3143164446679725 | 0.24149388987839712 | 0                       | 0.0                              |
| socio-patterns-primary-school-day1 | True          | 236       | 5899      | 18.0       | 98.0       | 49.99152542372882  | 18.948528607429786 | 0.379034815337636   | 1.9603322597050346 | 0.2127298954201226    | 0.7872701045798773 | 0.43842941643593236           | 0.17292222281109404   | 0.5018529176737266  | False                     | 0.0                  | 11 | 0.046610169491525424  | 10.0               | 25.0               | 21.454545454545453     | 4.033946860424326  | 0.1880229468841847  | 0                       | 0.0                              |
| email-eu-core                      | True          | 986       | 16064     | 1.0        | 345.0      | 32.5841784989858   | 37.044293876612585 | 1.1368797859294077  | 10.587960657370518 | 0.033080384262929745  | 0.9669196157370703 | 0.26739242877040204           | -0.025743368083088566 | 0.4070504475195386  | False                     | 0.0                  | 42 | 0.04259634888438134   | 1.0                | 107.0              | 23.476190476190474     | 23.593341449301363 | 1.0049902037227763  | 0                       | 0.0                              |
| us-political-blogs                 | True          | 1222      | 16714     | 1.0        | 351.0      | 27.355155482815057 | 38.41718773263562  | 1.4043856470408258  | 12.831219337082684 | 0.022403894744320276  | 0.9775961052556797 | 0.2259585173589758            | -0.2213287230119227   | 0.3202546194373154  | False                     | 0.0                  | 2  | 0.0016366612111292963 | 586.0              | 636.0              | 611.0                  | 35.35533905932738  | 0.05786471204472566 | 0                       | 0.0                              |
| cora                               | True          | 2485      | 5069      | 1.0        | 168.0      | 4.0796780684104625 | 5.406362318556419  | 1.325193367687187   | 41.179719865851254 | 0.0016423824752055003 | 0.9983576175247945 | 0.0900352512858051            | -0.07136519570204507  | 0.23763551095541197 | False                     | 0.0                  | 7  | 0.0028169014084507044 | 131.0              | 726.0              | 355.0                  | 189.6909767665997  | 0.5343407796242245  | 0                       | 0.0                              |
| facebook-network-ego698            | True          | 40        | 220       | 1.0        | 29.0       | 11.0               | 5.808923286082348  | 0.5280839350983952  | 2.6363636363636362 | 0.28205128205128205   | 0.717948717948718  | 0.6560531840447865            | 0.012473574916280844  | 0.7249190619129633  | True                      | 0.59375              | 9  | 0.225                 | 1.0                | 15.0               | 6.444444444444445      | 6.125991983163035  | 0.9505849629046089  | 8                       | 0.2                              |
| facebook-network-ego414            | True          | 148       | 1692      | 1.0        | 57.0       | 22.864864864864863 | 12.951846268016066 | 0.5664519053387641  | 2.49290780141844   | 0.15554329840044126   | 0.8444567015995588 | 0.6457982767359352            | 0.3039224601932676    | 0.6793500241563419  | True                      | 0.2537313432835821   | 7  | 0.0472972972972973    | 7.0                | 55.0               | 24.285714285714285     | 21.63880993118834  | 0.8910098206959906  | 14                      | 0.0945945945945946               |
| facebook-network-ego0              | True          | 324       | 2514      | 1.0        | 77.0       | 15.518518518518519 | 15.570959005850767 | 1.003379219947424   | 4.9618138424821    | 0.04804494897374154   | 0.9519550510262584 | 0.4258750132177223            | 0.23295552356572546   | 0.5223624457077098  | True                      | 0.1417910447761194   | 22 | 0.06790123456790123   | 1.0                | 129.0              | 13.909090909090908     | 27.300635071819762 | 1.9627907567974994  | 56                      | 0.1728395061728395               |
| facebook-network-ego3437           | True          | 532       | 4812      | 1.0        | 107.0      | 18.090225563909776 | 14.664847676938885 | 0.810650349556472   | 5.91479634247714   | 0.034068221400960025  | 0.96593177859904   | 0.4488933226158351            | 0.22207842776444284   | 0.545768617282594   | True                      | 0.6804123711340206   | 32 | 0.06015037593984962   | 1.0                | 50.0               | 6.0                    | 9.315266692284613  | 1.5525444487141022  | 435                     | 0.8176691729323309               |
| facebook-network-ego1684           | True          | 775       | 14006     | 1.0        | 136.0      | 36.144516129032255 | 28.476378855199318 | 0.7878478370976536  | 3.762673140082822  | 0.046698341251979664  | 0.9533016587480203 | 0.45225878166971445           | 0.3268349056797533    | 0.4713855751563139  | True                      | 0.006640106241699867 | 17 | 0.02193548387096774   | 1.0                | 223.0              | 44.705882352941174     | 62.501764680969565 | 1.3980657889164245  | 22                      | 0.02838709677419355              |
| facebook-network-ego1912           | True          | 744       | 30023     | 1.0        | 293.0      | 80.70698924731182  | 64.25341111081488  | 0.7961319299611344  | 3.630416680544916  | 0.10862313492235777   | 0.8913768650776422 | 0.7000214679657459            | 0.5026087042032253    | 0.6379667606225469  | True                      | 0.36415362731152207  | 45 | 0.06048387096774194   | 1.0                | 232.0              | 23.333333333333332     | 45.70010940905941  | 1.9585761175311176  | 41                      | 0.05510752688172043              |
| facebook-network-ego107            | True          | 1034      | 26749     | 1.0        | 253.0      | 51.73887814313346  | 47.02619707281583  | 0.9089141233932403  | 4.88993981083405   | 0.05008603886072939   | 0.9499139611392706 | 0.5045088189930924            | 0.4315692408853532    | 0.5264047980773338  | True                      | 0.03958333333333333  | 9  | 0.008704061895551257  | 10.0               | 307.0              | 55.55555555555556      | 94.95539888693943  | 1.7091971799649097  | 554                     | 0.5357833655705996               |

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



## Scripts

### Script 1

- Same as [Report 5](./report5.md), considering only the **Median K-Boundary Raw Contributions (LAPIN-on + Extraction of clusters until the end)**.



## Experience 9 (One network per family)

[Open Folder](../results/real-world/experience9/results_2026-05-23_12-38-55-140706/)

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                  | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.01438570601336112    | 0.004897996062934789   | 0.00948770995042633    | 2.937059529758272  | 0.008394112902265497   | 6.457799151480094           | 0.054207495177678235   | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.0035397587392402567  | 0.0008197903486553481  | 0.0027199683905849087  | 4.317882913657505  | 0.0017034846788267822  | 6.457799151480094           | 0.011000761913486935   | True             |
| network_family_03 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.00014051937967359449 | 0.00011388446551794506 | 2.663491415564943e-05  | 1.233876622544736  | 0.00012650286340253527 | 6.457799151480094           | 0.0008169300839406946  | True             |
| network_family_04 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 6.002690056865324e-05  | 4.3565505635533715e-05 | 1.6461394933119523e-05 | 1.3778538706938126 | 5.113807070087104e-05  | 6.457799151480094           | 0.000330239389580414   | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.991572094677042e-05  | 1.5119887617540192e-05 | 4.795833329230229e-06  | 1.317187101554029  | 1.7352909339285443e-05 | 6.457799151480094           | 0.00011206160320694853 | True             |
| network_family_06 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.006022762344880977   | 0.005668143736515978   | 0.0003546186083649991  | 1.06256344666781   | 0.005842763272772686   | 6.457799151480094           | 0.03773139170521051    | True             |
| network_family_07 | cora                               | 7  | False                       | 123                     | 123                               | 0.0014272644046179927  | 0.0011103937035788424  | 0.00031687070103915025 | 1.285367883497415  | 0.0012588984900419988  | 6.457799151480094           | 0.00812971360079279    | True             |
| network_family_08 | facebook-network-ego698            | 9  | False                       | 18                      | 18                                | 4.734806803854546e-05  | 3.1498427514717355e-05 | 1.5849640523828106e-05 | 1.5031883104774835 | 3.8618514848114366e-05 | 6.457799151480094           | 0.00024939061241757433 | True             |
| network_family_09 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 8.410582162852648e-06  | 8.013293256600162e-06  | 3.972889062524859e-07  | 1.0495787304333657 | 8.209534781561542e-06  | 6.457799151480094           | 5.3015526746414444e-05 | True             |
| network_family_10 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.3691255577654217e-06 | 3.0495462920868827e-06 | 3.1957926567853897e-07 | 1.1047956761659266 | 3.2053555734518272e-06 | 6.457799151480094           | 2.06995425024292e-05   | True             |
| network_family_11 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.7141851318097886e-05 | 1.8629538583949107e-05 | 3.851231273414878e-05  | 3.067271422778572  | 3.2627079610176386e-05 | 6.457799151480094           | 0.00021069912702187054 | True             |
| network_family_12 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.994146059893706e-06  | 5.650729825612765e-06  | 1.3434162342809413e-06 | 1.2377420750487325 | 6.286654893131432e-06  | 6.457799151480094           | 4.059795463451234e-05  | True             |
| network_family_13 | facebook-network-ego1912           | 45 | False                       | 56                      | 56                                | 6.379573842856358e-11  | 5.670438444315199e-12  | 5.812529998424838e-11  | 11.25058301135795  | 1.9019721548140587e-11 | 6.457799151480094           | 1.2282554167496993e-10 | True             |
| network_family_14 | facebook-network-ego107            | 9  | False                       | 68                      | 68                                | 0.0005686779807201585  | 0.0003925967817426963  | 0.0001760811989774622  | 1.4485039286258437 | 0.0004725051799490343  | 6.457799151480094           | 0.0030513435501448227  | True             |

### Sensitivity Analysis

| Group                           | Threshold      | Property                             | #Networks | Spearman Correlation | Pearson Correlation   | Abs Spearman Correlation (Sort Criterion) |
|---------------------------------|----------------|--------------------------------------|-----------|----------------------|-----------------------|-------------------------------------------|
| Non-overlapping and Overlapping | Normalized c_K | Min Community Size                   | 14        | 0.8588524480978449   | 0.31208952294562375   | 0.8588524480978449                        |
| Non-overlapping and Overlapping | Normalized c_K | **K**                                | 14        | -0.791625057980383   | -0.4564636633114558   | 0.791625057980383                         |
| Non-overlapping and Overlapping | Normalized c_K | **Degree Assortativity**             | 14        | -0.7582417582417583  | -0.7931752580647775   | 0.7582417582417583                        |
| Non-overlapping and Overlapping | Normalized c_K | Community Size CV                    | 14        | -0.7538461538461538  | -0.5558911474220116   | 0.7538461538461538                        |
| Non-overlapping and Overlapping | Normalized c_K | Global Clustering Coefficient        | 14        | -0.6747252747252748  | -0.4585152341146059   | 0.6747252747252748                        |
| Non-overlapping and Overlapping | Normalized c_K | Overlap Fraction                     | 14        | -0.6266414452860405  | -0.3099360943254341   | 0.6266414452860405                        |
| Non-overlapping and Overlapping | Normalized c_K | Nodes Without Community              | 14        | -0.5609262375406879  | -0.19238911656417     | 0.5609262375406879                        |
| Non-overlapping and Overlapping | Normalized c_K | **Average Degree**                   | 14        | -0.49890109890109896 | -0.3487428881386482   | 0.49890109890109896                       |
| Non-overlapping                 | Normalized c_K | **K**                                | 7         | -0.9549937104572925  | -0.5044594976112955   | 0.9549937104572925                        |
| Non-overlapping                 | Normalized c_K | **Degree Assortativity**             | 7         | -0.8928571428571429  | -0.9266414933027981   | 0.8928571428571429                        |
| Non-overlapping                 | Normalized c_K | Min Community Size                   | 7         | 0.7857142857142859   | 0.18031052248479496   | 0.7857142857142859                        |
| Non-overlapping                 | Normalized c_K | Community Size CV                    | 7         | -0.642857142857143   | -0.5687231584864857   | 0.642857142857143                         |
| Non-overlapping                 | Normalized c_K | **Average Degree**                   | 7         | -0.6071428571428572  | -0.42372202186252267  | 0.6071428571428572                        |
| Overlapping                     | Normalized c_K | Nodes Fraction Without Community     | 7         | 0.7857142857142859   | 0.4731173325410245    | 0.7857142857142859                        |
| Overlapping                     | Normalized c_K | Min Community Size                   | 7         | 0.5345224838248489   | 0.7837454456192526    | 0.5345224838248489                        |
| Overlapping                     | Normalized c_K | **K**                                | 7         | -0.4684874806016907  | -0.35803549442376925  | 0.4684874806016907                        |
| Overlapping                     | Normalized c_K | Community Proportion                 | 7         | -0.39285714285714296 | -0.32101084413375847  | 0.39285714285714296                       |
| Overlapping                     | Normalized c_K | Community Size CV                    | 7         | -0.3571428571428572  | 0.18114535139184232   | 0.3571428571428572                        |
| Overlapping                     | Normalized c_K | **Degree Assortativity**             | 7         | -0.3214285714285715  | 0.3189989970257345    | 0.3214285714285715                        |
| Overlapping                     | Normalized c_K | Degree Std                           | 7         | -0.3214285714285715  | 0.35897571848102794   | 0.3214285714285715                        |
| Overlapping                     | Normalized c_K | Nodes Without Community              | 7         | 0.3214285714285715   | 0.7939840905399307    | 0.3214285714285715                        |
| Overlapping                     | Normalized c_K | Degree Hub Ratio                     | 7         | 0.21428571428571433  | 0.321636320752317     | 0.21428571428571433                       |
| Overlapping                     | Normalized c_K | **Average Degree**                   | 7         | -0.1785714285714286  | 0.2604434268608927    | 0.1785714285714286                        |


## Experience 10 (Networks grouped by degree assortativity, average degree, and K)

[Open Folder](../results/real-world/experience10/results_2026-05-23_16-58-58-002155)

### Range Definitions

#### Degree Assortativity (Primary)

| Category                | Range                |
|-------------------------|----------------------|
| Strongly Disassortative | `r < -0.30`          |
| Disassortative          | `-0.30 <= r < -0.10` |
| Near-Neutral            | `-0.10 <= r < 0.10`  |
| Moderately Assortative  | `0.10 <= r < 0.35`   |
| Highly Assortative      | `r >= 0.35`          |

#### Average Degree (Secondary)

| Category                  | Range             |
|---------------------------|-------------------|
| Low Average Degree        | `a < 15`          |
| Medium Average Degree     | `15 <= a < 35`    |
| Large Average Degree      | `35 <= a < 65`    |
| Very Large Average Degree | `a >= 65`         |

#### K (Tertiary)

| Category     | Range           |
|--------------|-----------------|
| Low K        | `K <= 5`        |
| Medium K     | `6 <= K <= 20`  |
| Large K      | `21 <= K <= 40` |
| Very Large K | `K > 40`        |

---

### Network Families

| Combination                                                                    | Name              |
|--------------------------------------------------------------------------------|-------------------|
| Strongly Disassortative + Low Average Degree + Low K                           | Network Family 1  |
| Strongly Disassortative + Low Average Degree + Medium K                        | -                 |
| Strongly Disassortative + Low Average Degree + Large K                         | -                 |
| Strongly Disassortative + Low Average Degree + Very Large K                    | -                 |
| Strongly Disassortative + Medium Average Degree + Low K                        | -                 |
| Strongly Disassortative + Medium Average Degree + Medium K                     | -                 |
| Strongly Disassortative + Medium Average Degree + Large K                      | -                 |
| Strongly Disassortative + Medium Average Degree + Very Large K                 | -                 |
| Strongly Disassortative + Large Average Degree + Low K                         | -                 |
| Strongly Disassortative + Large Average Degree + Medium K                      | -                 |
| Strongly Disassortative + Large Average Degree + Large K                       | -                 |
| Strongly Disassortative + Large Average Degree + Very Large K                  | -                 |
| Strongly Disassortative + Very Large Average Degree + Low K                    | -                 |
| Strongly Disassortative + Very Large Average Degree + Medium K                 | -                 |
| Strongly Disassortative + Very Large Average Degree + Large K                  | -                 |
| Strongly Disassortative + Very Large Average Degree + Very Large K             | -                 |
| Disassortative + Low Average Degree + Low K                                    | Network Family 2  |
| Disassortative + Low Average Degree + Medium K                                 | -                 |
| Disassortative + Low Average Degree + Large K                                  | -                 |
| Disassortative + Low Average Degree + Very Large K                             | -                 |
| Disassortative + Medium Average Degree + Low K                                 | Network Family 3  |
| Disassortative + Medium Average Degree + Medium K                              | -                 |
| Disassortative + Medium Average Degree + Large K                               | -                 |
| Disassortative + Medium Average Degree + Very Large K                          | -                 |
| Disassortative + Large Average Degree + Low K                                  | -                 |
| Disassortative + Large Average Degree + Medium K                               | -                 |
| Disassortative + Large Average Degree + Large K                                | -                 |
| Disassortative + Large Average Degree + Very Large K                           | -                 |
| Disassortative + Very Large Average Degree + Low K                             | -                 |
| Disassortative + Very Large Average Degree + Medium K                          | -                 |
| Disassortative + Very Large Average Degree + Large K                           | -                 |
| Disassortative + Very Large Average Degree + Very Large K                      | -                 |
| Near-Neutral + Low Average Degree + Low K                                      | -                 |
| Near-Neutral + Low Average Degree + Medium K                                   | Network Family 4  |
| Near-Neutral + Low Average Degree + Large K                                    | -                 |
| Near-Neutral + Low Average Degree + Very Large K                               | -                 |
| Near-Neutral + Medium Average Degree + Low K                                   | -                 |
| Near-Neutral + Medium Average Degree + Medium K                                | -                 |
| Near-Neutral + Medium Average Degree + Large K                                 | -                 |
| Near-Neutral + Medium Average Degree + Very Large K                            | Network Family 5  |
| Near-Neutral + Large Average Degree + Low K                                    | -                 |
| Near-Neutral + Large Average Degree + Medium K                                 | -                 |
| Near-Neutral + Large Average Degree + Large K                                  | -                 |
| Near-Neutral + Large Average Degree + Very Large K                             | -                 |
| Near-Neutral + Very Large Average Degree + Low K                               | -                 |
| Near-Neutral + Very Large Average Degree + Medium K                            | -                 |
| Near-Neutral + Very Large Average Degree + Large K                             | -                 |
| Near-Neutral + Very Large Average Degree + Very Large K                        | -                 |
| Moderately Assortative + Low Average Degree + Low K                            | -                 |
| Moderately Assortative + Low Average Degree + Medium K                         | Network Family 6  |
| Moderately Assortative + Low Average Degree + Large K                          | -                 |
| Moderately Assortative + Low Average Degree + Very Large K                     | -                 |
| Moderately Assortative + Medium Average Degree + Low K                         | -                 |
| Moderately Assortative + Medium Average Degree + Medium K                      | Network Family 7  |
| Moderately Assortative + Medium Average Degree + Large K                       | Network Family 8  |
| Moderately Assortative + Medium Average Degree + Very Large K                  | -                 |
| Moderately Assortative + Large Average Degree + Low K                          | -                 |
| Moderately Assortative + Large Average Degree + Medium K                       | Network Family 9  |
| Moderately Assortative + Large Average Degree + Large K                        | -                 |
| Moderately Assortative + Large Average Degree + Very Large K                   | -                 |
| Moderately Assortative + Very Large Average Degree + Low K                     | -                 |
| Moderately Assortative + Very Large Average Degree + Medium K                  | -                 |
| Moderately Assortative + Very Large Average Degree + Large K                   | -                 |
| Moderately Assortative + Very Large Average Degree + Very Large K              | -                 |
| Highly Assortative + Low Average Degree + Low K                                | -                 |
| Highly Assortative + Low Average Degree + Medium K                             | -                 |
| Highly Assortative + Low Average Degree + Large K                              | -                 |
| Highly Assortative + Low Average Degree + Very Large K                         | -                 |
| Highly Assortative + Medium Average Degree + Low K                             | -                 |
| Highly Assortative + Medium Average Degree + Medium K                          | -                 |
| Highly Assortative + Medium Average Degree + Large K                           | -                 |
| Highly Assortative + Medium Average Degree + Very Large K                      | -                 |
| Highly Assortative + Large Average Degree + Low K                              | -                 |
| Highly Assortative + Large Average Degree + Medium K                           | Network Family 10 |
| Highly Assortative + Large Average Degree + Large K                            | -                 |
| Highly Assortative + Large Average Degree + Very Large K                       | -                 |
| Highly Assortative + Very Large Average Degree + Low K                         | -                 |
| Highly Assortative + Very Large Average Degree + Medium K                      | -                 |
| Highly Assortative + Very Large Average Degree + Large K                       | -                 |
| Highly Assortative + Very Large Average Degree + Very Large K                  | Network Family 11 |

### Network Family 1 (Strongly Disassortative + Low Average Degree + Low K)

#### Range
- Strongly Disassortative: `r < -0.30`
- Low Average Degree: `a < 15`
- Low K: `K <= 5`

| Network             | Set   | Degree Assortativity | Average Degree | K |
|---------------------|-------|----------------------|----------------|---|
| zachary-karate-club | Train | -0.4756              | 4.5882         | 2 |

### Network Family 2 (Disassortative + Low Average Degree + Low K)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Low Average Degree: `a < 15`
- Low K: `K <= 5`

| Network                 | Set   | Degree Assortativity | Average Degree | K |
|-------------------------|-------|----------------------|----------------|---|
| books-about-us-politics | Train | -0.1279              | 8.4000         | 3 |

### Network Family 3 (Disassortative + Medium Average Degree + Low K)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Medium Average Degree: `15 <= a < 35`
- Low K: `K <= 5`

| Network            | Set   | Degree Assortativity | Average Degree | K |
|--------------------|-------|----------------------|----------------|---|
| us-political-blogs | Train | -0.2213              | 27.3552        | 2 |

### Network Family 4 (Near-Neutral + Low Average Degree + Medium K)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`
- Medium K: `6 <= K <= 20`

| Network                 | Set   | Degree Assortativity | Average Degree | K |
|-------------------------|-------|----------------------|----------------|---|
| cora                    | Train | -0.0714              | 4.0797         | 7 |
| facebook-network-ego698 | Train | 0.0125               | 11.0000        | 9 |

### Network Family 5 (Near-Neutral + Medium Average Degree + Very Large K)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`
- Very Large K: `K > 40`

| Network       | Set   | Degree Assortativity | Average Degree | K  |
|---------------|-------|----------------------|----------------|----|
| email-eu-core | Train | -0.0257              | 32.5842        | 42 |

### Network Family 6 (Moderately Assortative + Low Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Low Average Degree: `a < 15`
- Medium K: `6 <= K <= 20`

| Network                   | Set   | Degree Assortativity | Average Degree | K  |
|---------------------------|-------|----------------------|----------------|----|
| american-college-football | Train | 0.1624               | 10.6609        | 12 |

### Network Family 7 (Moderately Assortative + Medium Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`
- Medium K: `6 <= K <= 20`

| Network                 | Set   | Degree Assortativity | Average Degree | K  |
|-------------------------|-------|----------------------|----------------|----|
| facebook-network-ego414 | Train | 0.3039               | 22.8649        | 7  |

### Network Family 8 (Moderately Assortative + Medium Average Degree + Large K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`
- Large K: `21 <= K <= 40`

| Network                  | Set   | Degree Assortativity | Average Degree | K  |
|--------------------------|-------|----------------------|----------------|----|
| facebook-network-ego0    | Train | 0.2330               | 15.5185        | 22 |
| facebook-network-ego3437 | Train | 0.2221               | 18.0902        | 32 |

### Network Family 9 (Moderately Assortative + Large Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`
- Medium K: `6 <= K <= 20`

| Network                            | Set   | Degree Assortativity | Average Degree | K  |
|------------------------------------|-------|----------------------|----------------|----|
| facebook-network-ego1684           | Train | 0.3268               | 36.1445        | 17 |
| socio-patterns-primary-school-day1 | Train | 0.1729               | 49.9915        | 11 |

### Network Family 10 (Highly Assortative + Large Average Degree + Medium K)

#### Range
- Highly Assortative: `r >= 0.35`
- Large Average Degree: `35 <= a < 65`
- Medium K: `6 <= K <= 20`

| Network                 | Set   | Degree Assortativity | Average Degree | K |
|-------------------------|-------|----------------------|----------------|---|
| facebook-network-ego107 | Train | 0.4316               | 51.7389        | 9 |

### Network Family 11 (Highly Assortative + Very Large Average Degree + Very Large K)

#### Range
- Highly Assortative: `r >= 0.35`
- Very Large Average Degree: `a >= 65`
- Very Large K: `K > 40`

| Network                  | Set   | Degree Assortativity | Average Degree | K  |
|--------------------------|-------|----------------------|----------------|----|
| facebook-network-ego1912 | Train | 0.5026               | 80.7070        | 45 |

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                  | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.014385706013361121   | 0.00489799606293479    | 0.009487709950426332   | 2.9370595297582716 | 0.008394112902265499   | 6.457799151480093           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.0035397587392402576  | 0.0008197903486553482  | 0.0027199683905849096  | 4.317882913657506  | 0.0017034846788267827  | 6.457799151480093           | 0.011000761913486937   | True             |
| network_family_03 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.006022762344880978   | 0.005668143736515979   | 0.0003546186083649991  | 1.06256344666781   | 0.005842763272772687   | 6.457799151480093           | 0.03773139170521051    | True             |
| network_family_04 | cora                               | 7  | False                       | 123                     | 123                               | 0.001427264404617993   | 0.0011103937035788426  | 0.00031687070103915025 | 1.285367883497415  | 0.001258898490041999   | 6.457799151480093           | 0.00812971360079279    | True             |
| network_family_04 | facebook-network-ego698            | 9  | False                       | 18                      | 18                                | 4.734806803854547e-05  | 3.149842751471736e-05  | 1.5849640523828106e-05 | 1.5031883104774835 | 3.861851484811437e-05  | 6.457799151480093           | 0.0002493906124175744  | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.9915720946770424e-05 | 1.5119887617540195e-05 | 4.795833329230229e-06  | 1.317187101554029  | 1.7352909339285446e-05 | 6.457799151480093           | 0.00011206160320694854 | True             |
| network_family_06 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.0001405193796735945  | 0.00011388446551794507 | 2.6634914155649443e-05 | 1.233876622544736  | 0.0001265028634025353  | 6.457799151480093           | 0.0008169300839406946  | True             |
| network_family_07 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 8.410582162852648e-06  | 8.013293256600164e-06  | 3.972889062524842e-07  | 1.0495787304333655 | 8.209534781561544e-06  | 6.457799151480093           | 5.3015526746414444e-05 | True             |
| network_family_08 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.369125557765422e-06  | 3.049546292086883e-06  | 3.1957926567853897e-07 | 1.1047956761659266 | 3.2053555734518276e-06 | 6.457799151480093           | 2.06995425024292e-05   | True             |
| network_family_08 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.714185131809789e-05  | 1.8629538583949107e-05 | 3.8512312734148785e-05 | 3.0672714227785725 | 3.2627079610176386e-05 | 6.457799151480093           | 0.00021069912702187052 | True             |
| network_family_09 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 6.0026900568653244e-05 | 4.356550563553372e-05  | 1.6461394933119523e-05 | 1.3778538706938126 | 5.113807070087104e-05  | 6.457799151480093           | 0.000330239389580414   | True             |
| network_family_09 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.994146059893707e-06  | 5.650729825612766e-06  | 1.3434162342809413e-06 | 1.2377420750487325 | 6.286654893131432e-06  | 6.457799151480093           | 4.0597954634512334e-05 | True             |
| network_family_10 | facebook-network-ego107            | 9  | False                       | 68                      | 68                                | 0.0005686779807201585  | 0.00039259678174269634 | 0.00017608119897746214 | 1.4485039286258434 | 0.0004725051799490343  | 6.457799151480093           | 0.0030513435501448223  | True             |
| network_family_11 | facebook-network-ego1912           | 45 | False                       | 56                      | 56                                | 6.379573842856359e-11  | 5.6704384443152e-12    | 5.812529998424839e-11  | 11.25058301135795  | 1.901972154814059e-11  | 6.457799151480093           | 1.2282554167496995e-10 | True             |

### Thresholds by Network Family

| Network Family    | #Networks | #Valid Thresholds | Median Normalized Threshold | Median Raw Threshold   | Median gap_K           | Median ratio_K     | Threshold              |
|-------------------|-----------|-------------------|-----------------------------|------------------------|------------------------|--------------------|------------------------|
| network_family_01 | 1         | 1                 | 0.008394112902265499        | 0.05420749517767824    | 0.009487709950426332   | 2.9370595297582716 | 0.05420749517767824    |
| network_family_02 | 1         | 1                 | 0.0017034846788267827       | 0.011000761913486937   | 0.0027199683905849096  | 4.317882913657506  | 0.011000761913486937   |
| network_family_03 | 1         | 1                 | 0.005842763272772687        | 0.03773139170521051    | 0.0003546186083649991  | 1.06256344666781   | 0.03773139170521051    |
| network_family_04 | 2         | 2                 | 0.0006487585024450567       | 0.004189552106605182   | 0.00016636017078148918 | 1.394278096987449  | 0.004189552106605182   |
| network_family_05 | 1         | 1                 | 1.7352909339285446e-05      | 0.00011206160320694854 | 4.795833329230229e-06  | 1.317187101554029  | 0.00011206160320694854 |
| network_family_06 | 1         | 1                 | 0.0001265028634025353       | 0.0008169300839406946  | 2.6634914155649443e-05 | 1.233876622544736  | 0.0008169300839406946  |
| network_family_07 | 1         | 1                 | 8.209534781561544e-06       | 5.3015526746414444e-05 | 3.972889062524842e-07  | 1.0495787304333655 | 5.3015526746414444e-05 |
| network_family_08 | 2         | 2                 | 1.7916217591814107e-05      | 0.00011569933476214986 | 1.941594599991366e-05  | 2.0860335494722495 | 0.00011569933476214986 |
| network_family_09 | 2         | 2                 | 2.8712362797001234e-05      | 0.00018541867210746318 | 8.902405583700231e-06  | 1.3077979728712725 | 0.00018541867210746318 |
| network_family_10 | 1         | 1                 | 0.0004725051799490343       | 0.0030513435501448223  | 0.00017608119897746214 | 1.4485039286258434 | 0.0030513435501448223  |
| network_family_11 | 1         | 1                 | 1.901972154814059e-11       | 1.2282554167496995e-10 | 5.812529998424839e-11  | 11.25058301135795  | 1.2282554167496995e-10 |

## Experience 11 (Networks grouped by degree assortativity and average degree)

[Open Folder](../results/real-world/experience11/results_2026-05-23_14-35-43-611177/)

### Range Definitions

#### Degree Assortativity (Primary)

| Category                | Range                |
|-------------------------|----------------------|
| Strongly Disassortative | `r < -0.30`          |
| Disassortative          | `-0.30 <= r < -0.10` |
| Near-Neutral            | `-0.10 <= r < 0.10`  |
| Moderately Assortative  | `0.10 <= r < 0.35`   |
| Highly Assortative      | `r >= 0.35`          |

#### Average Degree (Secondary)

| Category                  | Range             |
|---------------------------|-------------------|
| Low Average Degree        | `a < 15`          |
| Medium Average Degree     | `15 <= a < 35`    |
| Large Average Degree      | `35 <= a < 65`    |
| Very Large Average Degree | `a >= 65`         |

---

### Network Families

| Combination                                             | Name              |
|---------------------------------------------------------|-------------------|
| Strongly Disassortative + Low Average Degree            |	Network Family 1  |
| Disassortative + Low Average Degree  			          | Network Family 2  |
| Near-Neutral + Low Average Degree			              | Network Family 4  |
| Moderately Assortative + Low Average Degree	          | Network Family 6  |
| Highly Assortative + Low Average Degree                 | -                 |
| Strongly Disassortative + Medium Average Degree         | -                 |
| Disassortative + Medium Average Degree   		          | Network Family 3  |
| Near-Neutral + Medium Average Degree			          | Network Family 5  |
| Moderately Assortative + Medium Average Degree          |	Network Family 7  |
| Highly Assortative + Medium Average Degree              | -                 |
| Strongly Disassortative + Large Average Degree          | -                 |
| Disassortative + Large Average Degree                   | -                 |
| Near-Neutral + Large Average Degree                     | -                 |
| Moderately Assortative + Large Average Degree   		  |	Network Family 8  |
| Highly Assortative + Large Average Degree               | Network Family 9  |
| Strongly Disassortative + Very Large Average Degree     | -                 |
| Disassortative + Very Large Average Degree              | -                 |
| Near-Neutral + Very Large Average Degree                | -                 |
| Moderately Assortative + Very Large Average Degree      | -                 |
| Highly Assortative + Very Large Average Degree          | Network Family 10 |

### Network Family 1 (Strongly Disassortative + Low Average Degree)

#### Range
- Strongly Disassortative: `r < -0.30`
- Low Average Degree: `a < 15`

| Network             | Set   | Average Degree | Degree Assortativity |
|---------------------|-------|----------------|----------------------|
| zachary-karate-club | Train | 4.5882         | -0.4756              |

### Network Family 2 (Disassortative + Low Average Degree)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Low Average Degree: `a < 15`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| books-about-us-politics | Train | 8.4000         | -0.1279              |

### Network Family 3 (Disassortative + Medium Average Degree)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Medium Average Degree: `15 <= a < 35`

| Network            | Set   | Average Degree | Degree Assortativity |
|--------------------|-------|----------------|----------------------|
| us-political-blogs | Train | 27.3552        | -0.2213              |

### Network Family 4 (Near-Neutral + Low Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| cora                     | Train | 4.0797         | -0.0714              |
| facebook-network-ego698  | Train | 11.0000        | 0.0125               |

### Network Family 5 (Near-Neutral + Medium Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| email-eu-core           | Train | 32.5842        | -0.0257              |

### Network Family 6 (Moderately Assortative + Low Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Low Average Degree: `a < 15`

| Network                   | Set   | Average Degree | Degree Assortativity |
|---------------------------|-------|----------------|----------------------|
| american-college-football | Train | 10.6609        | 0.1624               |

### Network Family 7 (Moderately Assortative + Medium Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego0    | Train | 15.5185        | 0.2330               |
| facebook-network-ego3437 | Train | 18.0902        | 0.2221               |
| facebook-network-ego414  | Train | 22.8649        | 0.3039               |

### Network Family 8 (Moderately Assortative + Large Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                            | Set   | Average Degree | Degree Assortativity |
|------------------------------------|-------|----------------|----------------------|
| facebook-network-ego1684           | Train | 36.1445        | 0.3268               |
| socio-patterns-primary-school-day1 | Train | 49.9915        | 0.1729               |

### Network Family 9 (Highly Assortative + Large Average Degree)

#### Range
- Highly Assortative: `r >= 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| facebook-network-ego107 | Train | 51.7389        | 0.4316               |

### Network Family 10 (Highly Assortative + Very Large Average Degree)

#### Range
- Highly Assortative: `r >= 0.35`
- Very Large Average Degree: `a >= 65`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego1912 | Train | 80.7070        | 0.5026               |

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                  | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.014385706013361121   | 0.00489799606293479    | 0.009487709950426332   | 2.9370595297582716 | 0.008394112902265499   | 6.457799151480093           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.0035397587392402576  | 0.0008197903486553482  | 0.0027199683905849096  | 4.317882913657506  | 0.0017034846788267827  | 6.457799151480093           | 0.011000761913486937   | True             |
| network_family_03 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.006022762344880978   | 0.005668143736515979   | 0.0003546186083649991  | 1.06256344666781   | 0.005842763272772687   | 6.457799151480093           | 0.03773139170521051    | True             |
| network_family_04 | cora                               | 7  | False                       | 123                     | 123                               | 0.001427264404617993   | 0.0011103937035788426  | 0.00031687070103915025 | 1.285367883497415  | 0.001258898490041999   | 6.457799151480093           | 0.00812971360079279    | True             |
| network_family_04 | facebook-network-ego698            | 9  | False                       | 18                      | 18                                | 4.734806803854547e-05  | 3.149842751471736e-05  | 1.5849640523828106e-05 | 1.5031883104774835 | 3.861851484811437e-05  | 6.457799151480093           | 0.0002493906124175744  | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.9915720946770424e-05 | 1.5119887617540195e-05 | 4.795833329230229e-06  | 1.317187101554029  | 1.7352909339285446e-05 | 6.457799151480093           | 0.00011206160320694854 | True             |
| network_family_06 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.0001405193796735945  | 0.00011388446551794507 | 2.6634914155649443e-05 | 1.233876622544736  | 0.0001265028634025353  | 6.457799151480093           | 0.0008169300839406946  | True             |
| network_family_07 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.369125557765422e-06  | 3.049546292086883e-06  | 3.1957926567853897e-07 | 1.1047956761659266 | 3.2053555734518276e-06 | 6.457799151480093           | 2.06995425024292e-05   | True             |
| network_family_07 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 8.410582162852648e-06  | 8.013293256600164e-06  | 3.972889062524842e-07  | 1.0495787304333655 | 8.209534781561544e-06  | 6.457799151480093           | 5.3015526746414444e-05 | True             |
| network_family_07 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.714185131809789e-05  | 1.8629538583949107e-05 | 3.8512312734148785e-05 | 3.0672714227785725 | 3.2627079610176386e-05 | 6.457799151480093           | 0.00021069912702187052 | True             |
| network_family_08 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.994146059893707e-06  | 5.650729825612766e-06  | 1.3434162342809413e-06 | 1.2377420750487325 | 6.286654893131432e-06  | 6.457799151480093           | 4.0597954634512334e-05 | True             |
| network_family_08 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 6.0026900568653244e-05 | 4.356550563553372e-05  | 1.6461394933119523e-05 | 1.3778538706938126 | 5.113807070087104e-05  | 6.457799151480093           | 0.000330239389580414   | True             |
| network_family_09 | facebook-network-ego107            | 9  | False                       | 68                      | 68                                | 0.0005686779807201585  | 0.00039259678174269634 | 0.00017608119897746214 | 1.4485039286258434 | 0.0004725051799490343  | 6.457799151480093           | 0.0030513435501448223  | True             |
| network_family_10 | facebook-network-ego1912           | 45 | False                       | 56                      | 56                                | 6.379573842856359e-11  | 5.6704384443152e-12    | 5.812529998424839e-11  | 11.25058301135795  | 1.901972154814059e-11  | 6.457799151480093           | 1.2282554167496995e-10 | True             |

### Thresholds by Network Family

| Network Family    | #Networks | #Valid Thresholds | Median Normalized Threshold | Median Raw Threshold   | Median gap_K           | Median ratio_K     | Threshold              |
|-------------------|-----------|-------------------|-----------------------------|------------------------|------------------------|--------------------|------------------------|
| network_family_01 | 1         | 1                 | 0.008394112902265499        | 0.05420749517767824    | 0.009487709950426332   | 2.9370595297582716 | 0.05420749517767824    |
| network_family_02 | 1         | 1                 | 0.0017034846788267827       | 0.011000761913486937   | 0.0027199683905849096  | 4.317882913657506  | 0.011000761913486937   |
| network_family_03 | 1         | 1                 | 0.005842763272772687        | 0.03773139170521051    | 0.0003546186083649991  | 1.06256344666781   | 0.03773139170521051    |
| network_family_04 | 2         | 2                 | 0.0006487585024450567       | 0.004189552106605182   | 0.00016636017078148918 | 1.394278096987449  | 0.004189552106605182   |
| network_family_05 | 1         | 1                 | 1.7352909339285446e-05      | 0.00011206160320694854 | 4.795833329230229e-06  | 1.317187101554029  | 0.00011206160320694854 |
| network_family_06 | 1         | 1                 | 0.0001265028634025353       | 0.0008169300839406946  | 2.6634914155649443e-05 | 1.233876622544736  | 0.0008169300839406946  |
| network_family_07 | 3         | 3                 | 8.209534781561544e-06       | 5.3015526746414444e-05 | 3.972889062524842e-07  | 1.1047956761659266 | 5.3015526746414444e-05 |
| network_family_08 | 2         | 2                 | 2.8712362797001234e-05      | 0.00018541867210746318 | 8.902405583700231e-06  | 1.3077979728712725 | 0.00018541867210746318 |
| network_family_09 | 1         | 1                 | 0.0004725051799490343       | 0.0030513435501448223  | 0.00017608119897746214 | 1.4485039286258434 | 0.0030513435501448223  |
| network_family_10 | 1         | 1                 | 1.901972154814059e-11       | 1.2282554167496995e-10 | 5.812529998424839e-11  | 11.25058301135795  | 1.2282554167496995e-10 |

## Experience 12

### Structural Properties of Networks in Test Set 

| Network                            | Ground-Truth? | Nodes LCC | Edges LCC | Min Degree | Max Degree | Average Degree     | Degree Std         | Degree CV           | Degree Hub Ratio   | Density               | Sparsity           | Global Clustering Coefficient | Degree Assortativity  | Average Clustering  | Overlapping Ground-Truth? | Overlap Fraction   | K  | Community Proportion | Min Community Size | Max Community Size | Average Community Size | Community Size Std | Community Size CV   | Nodes Without Community | Nodes Fraction Without Community |
|------------------------------------|---------------|-----------|-----------|------------|------------|--------------------|--------------------|---------------------|--------------------|-----------------------|--------------------|-------------------------------|-----------------------|---------------------|---------------------------|--------------------|----|----------------------|--------------------|--------------------|------------------------|--------------------|---------------------|-------------------------|----------------------------------|
| word-adjacencies                   | True          | 112       | 425       | 1.0        | 49.0       | 7.589285714285714  | 6.8819565249517245 | 0.9067989774054037  | 6.456470588235294  | 0.06837194337194337   | 0.9316280566280566 | 0.15693497881746177           | -0.1293478534390013   | 0.17284007981036792 | False                     | 0.0                | 2  | 0.017857142857142856 | 54.0               | 58.0               | 56.0                   | 2.8284271247461903 | 0.05050762722761054 | 0                       | 0.0                              |
| socio-patterns-primary-school-day2 | True          | 238       | 5539      | 8.0        | 88.0       | 46.54621848739496  | 19.892007130129983 | 0.42736032650035527 | 1.8905939700306913 | 0.19639754636031628   | 0.8036024536396837 | 0.46816525721161883           | 0.21681961190098284   | 0.559558532849634   | False                     | 0.0                | 11 | 0.046218487394957986 | 10.0               | 26.0               | 21.636363636363637     | 4.177863742936747  | 0.19309454274077403 | 0                       | 0.0                              |
| citeseer                           | True          | 2110      | 3668      | 1.0        | 99.0       | 3.476777251184834  | 3.9983615708750007 | 1.1500194812631204  | 28.47464558342421  | 0.0016485430304337763 | 0.9983514569695662 | 0.12523609451489803           | 0.0071366166694059475 | 0.17106997537906155 | False                     | 0.0                | 6  | 0.002843601895734597 | 115.0              | 532.0              | 351.6666666666667      | 145.89402546597535 | 0.41486452739139906 | 0                       | 0.0                              |
| facebook-network-ego348            | True          | 224       | 3192      | 1.0        | 99.0       | 28.5               | 22.417561981665038 | 0.7865811221636856  | 3.473684210526316  | 0.12780269058295965   | 0.8721973094170403 | 0.4902791105177521            | 0.22269166051622483   | 0.5442814709697877  | True                      | 0.8532110091743119 | 14 | 0.0625               | 4.0                | 201.0              | 40.357142857142854     | 55.757175658049945 | 1.3815937331198218  | 6                       | 0.026785714285714284             |
| facebook-network-ego686            | True          | 168       | 1656      | 1.0        | 77.0       | 19.714285714285715 | 16.068767957698487 | 0.8150824326368797  | 3.905797101449275  | 0.11804961505560307   | 0.8819503849443969 | 0.45355939944054346           | 0.08406304044981644   | 0.5337913395248177  | True                      | 0.8035714285714286 | 14 | 0.08333333333333333  | 4.0                | 101.0              | 34.42857142857143      | 30.88617885003006  | 0.8971089292539851  | 0                       | 0.0                              |
| facebook-network-ego3980           | True          | 44        | 138       | 1.0        | 18.0       | 6.2727272727272725 | 4.206106504106863  | 0.6705387180460217  | 2.8695652173913047 | 0.14587737843551796   | 0.854122621564482  | 0.44404332129963897           | 0.05297863564191894   | 0.4547680965795939  | True                      | 0.0                | 11 | 0.25                 | 1.0                | 21.0               | 4.0                    | 5.932958789676531  | 1.4832396974191326  | 0                       | 0.0                              |

---

### Experience 10-based

| Network                            | Average Degree | Degree Assortativity | K  | Combination                                                   | Assigned Family     | Calibrated? |
|------------------------------------|----------------|----------------------|----|---------------------------------------------------------------|---------------------|-------------|
| word-adjacencies                   | 7.5893         | -0.1293              | 2  | Disassortative + Low Average Degree + Low K                   | `network_family_02` | Yes         |
| socio-patterns-primary-school-day2 | 46.5462        | 0.2168               | 11 | Moderately Assortative + Large Average Degree + Medium K      | `network_family_09` | Yes         |
| citeseer                           | 3.4768         | 0.0071               | 6  | Near-Neutral + Low Average Degree + Medium K                  | `network_family_04` | Yes         |
| facebook-network-ego348            | 28.5000        | 0.2227               | 14 | Moderately Assortative + Medium Average Degree + Medium K     | `network_family_07` | Yes         |
| facebook-network-ego686            | 19.7143        | 0.0841               | 14 | Near-Neutral + Medium Average Degree + Medium K               | `network_family_05` | Approx.     |
| facebook-network-ego3980           | 6.2727         | 0.0530               | 11 | Near-Neutral + Low Average Degree + Medium K                  | `network_family_04` | Yes         |

### Experience 11-based

| Network                            | Average Degree | Degree Assortativity | Combination                                    | Assigned Family     | Calibrated? |
|------------------------------------|----------------|----------------------|------------------------------------------------|---------------------|-------------|
| word-adjacencies                   | 7.5893         | -0.1293              | Disassortative + Low Average Degree            | `network_family_02` | Yes         |
| socio-patterns-primary-school-day2 | 46.5462        | 0.2168               | Moderately Assortative + Large Average Degree  | `network_family_08` | Yes         |
| citeseer                           | 3.4768         | 0.0071               | Near-Neutral + Low Average Degree              | `network_family_04` | Yes         |
| facebook-network-ego348            | 28.5000        | 0.2227               | Moderately Assortative + Medium Average Degree | `network_family_07` | Yes         |
| facebook-network-ego686            | 19.7143        | 0.0841               | Near-Neutral + Medium Average Degree           | `network_family_05` | Yes         |
| facebook-network-ego3980           | 6.2727         | 0.0530               | Near-Neutral + Low Average Degree              | `network_family_04` | Yes         |



---
---
---


## Experience 13 (Networks grouped by ground-truth type, degree assortativity, and average degree)

[Open Folder](../results/real-world/experience13/results_2026-05-23_22-54-46-593669/)

### Range Definitions

#### Ground-Truth Type (Primary)

| Category        | Range                               |
|-----------------|-------------------------------------|
| Non-Overlapping | `Overlapping Ground-Truth? = False` |
| Overlapping     | `Overlapping Ground-Truth? = True`  |

#### Degree Assortativity (Secondary)

| Category                | Range                |
|-------------------------|----------------------|
| Strongly Disassortative | `r < -0.30`          |
| Disassortative          | `-0.30 <= r < -0.10` |
| Near-Neutral            | `-0.10 <= r < 0.10`  |
| Moderately Assortative  | `0.10 <= r < 0.35`   |
| Highly Assortative      | `r >= 0.35`          |

#### Average Degree (Tertiary)

| Category                  | Range          |
|---------------------------|----------------|
| Low Average Degree        | `a < 15`       |
| Medium Average Degree     | `15 <= a < 35` |
| Large Average Degree      | `35 <= a < 65` |
| Very Large Average Degree | `a >= 65`      |

---

### Network Families

| Combination                                                                    | Name              |
|--------------------------------------------------------------------------------|-------------------|
| Non-Overlapping + Strongly Disassortative + Low Average Degree                 | Network Family 1  |
| Non-Overlapping + Strongly Disassortative + Medium Average Degree              | -                 |
| Non-Overlapping + Strongly Disassortative + Large Average Degree               | -                 |
| Non-Overlapping + Strongly Disassortative + Very Large Average Degree          | -                 |
| Non-Overlapping + Disassortative + Low Average Degree                          | Network Family 2  |
| Non-Overlapping + Disassortative + Medium Average Degree                       | Network Family 3  |
| Non-Overlapping + Disassortative + Large Average Degree                        | -                 |
| Non-Overlapping + Disassortative + Very Large Average Degree                   | -                 |
| Non-Overlapping + Near-Neutral + Low Average Degree                            | Network Family 4  |
| Non-Overlapping + Near-Neutral + Medium Average Degree                         | Network Family 5  |
| Non-Overlapping + Near-Neutral + Large Average Degree                          | -                 |
| Non-Overlapping + Near-Neutral + Very Large Average Degree                     | -                 |
| Non-Overlapping + Moderately Assortative + Low Average Degree                  | Network Family 6  |
| Non-Overlapping + Moderately Assortative + Medium Average Degree               | -                 |
| Non-Overlapping + Moderately Assortative + Large Average Degree                | Network Family 7  |
| Non-Overlapping + Moderately Assortative + Very Large Average Degree           | -                 |
| Non-Overlapping + Highly Assortative + Low Average Degree                      | -                 |
| Non-Overlapping + Highly Assortative + Medium Average Degree                   | -                 |
| Non-Overlapping + Highly Assortative + Large Average Degree                    | -                 |
| Non-Overlapping + Highly Assortative + Very Large Average Degree               | -                 |
| Overlapping + Strongly Disassortative + Low Average Degree                     | -                 |
| Overlapping + Strongly Disassortative + Medium Average Degree                  | -                 |
| Overlapping + Strongly Disassortative + Large Average Degree                   | -                 |
| Overlapping + Strongly Disassortative + Very Large Average Degree              | -                 |
| Overlapping + Disassortative + Low Average Degree                              | -                 |
| Overlapping + Disassortative + Medium Average Degree                           | -                 |
| Overlapping + Disassortative + Large Average Degree                            | -                 |
| Overlapping + Disassortative + Very Large Average Degree                       | -                 |
| Overlapping + Near-Neutral + Low Average Degree                                | Network Family 8  |
| Overlapping + Near-Neutral + Medium Average Degree                             | -                 |
| Overlapping + Near-Neutral + Large Average Degree                              | -                 |
| Overlapping + Near-Neutral + Very Large Average Degree                         | -                 |
| Overlapping + Moderately Assortative + Low Average Degree                      | -                 |
| Overlapping + Moderately Assortative + Medium Average Degree                   | Network Family 9  |
| Overlapping + Moderately Assortative + Large Average Degree                    | Network Family 10 |
| Overlapping + Moderately Assortative + Very Large Average Degree               | -                 |
| Overlapping + Highly Assortative + Low Average Degree                          | -                 |
| Overlapping + Highly Assortative + Medium Average Degree                       | -                 |
| Overlapping + Highly Assortative + Large Average Degree                        | Network Family 11 |
| Overlapping + Highly Assortative + Very Large Average Degree                   | Network Family 12 |

### Network Family 1 (Non-Overlapping + Strongly Disassortative + Low Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Strongly Disassortative: `r < -0.30`
- Low Average Degree: `a < 15`

| Network             | Set   | Average Degree | Degree Assortativity |
|---------------------|-------|----------------|----------------------|
| zachary-karate-club | Train | 4.5882         | -0.4756              |

### Network Family 2 (Non-Overlapping + Disassortative + Low Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Disassortative: `-0.30 <= r < -0.10`
- Low Average Degree: `a < 15`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| books-about-us-politics | Train | 8.4000         | -0.1279              |

### Network Family 3 (Non-Overlapping + Disassortative + Medium Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Disassortative: `-0.30 <= r < -0.10`
- Medium Average Degree: `15 <= a < 35`

| Network            | Set   | Average Degree | Degree Assortativity |
|--------------------|-------|----------------|----------------------|
| us-political-blogs | Train | 27.3552        | -0.2213              |

### Network Family 4 (Non-Overlapping + Near-Neutral + Low Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`

| Network | Set   | Average Degree | Degree Assortativity |
|---------|-------|----------------|----------------------|
| cora    | Train | 4.0797         | -0.0714              |

### Network Family 5 (Non-Overlapping + Near-Neutral + Medium Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`

| Network       | Set   | Average Degree | Degree Assortativity |
|---------------|-------|----------------|----------------------|
| email-eu-core | Train | 32.5842        | -0.0257              |

### Network Family 6 (Non-Overlapping + Moderately Assortative + Low Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Moderately Assortative: `0.10 <= r < 0.35`
- Low Average Degree: `a < 15`

| Network                   | Set   | Average Degree | Degree Assortativity |
|---------------------------|-------|----------------|----------------------|
| american-college-football | Train | 10.6609        | 0.1624               |

### Network Family 7 (Non-Overlapping + Moderately Assortative + Large Average Degree)

#### Range
- Non-Overlapping: `Overlapping Ground-Truth? = False`
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                            | Set   | Average Degree | Degree Assortativity |
|------------------------------------|-------|----------------|----------------------|
| socio-patterns-primary-school-day1 | Train | 49.9915        | 0.1729               |

### Network Family 8 (Overlapping + Near-Neutral + Low Average Degree)

#### Range
- Overlapping: `Overlapping Ground-Truth? = True`
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| facebook-network-ego698 | Train | 11.0000        | 0.0125               |

### Network Family 9 (Overlapping + Moderately Assortative + Medium Average Degree)

#### Range
- Overlapping: `Overlapping Ground-Truth? = True`
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego0    | Train | 15.5185        | 0.2330               |
| facebook-network-ego3437 | Train | 18.0902        | 0.2221               |
| facebook-network-ego414  | Train | 22.8649        | 0.3039               |

### Network Family 10 (Overlapping + Moderately Assortative + Large Average Degree)

#### Range
- Overlapping: `Overlapping Ground-Truth? = True`
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego1684 | Train | 36.1445        | 0.3268               |

### Network Family 11 (Overlapping + Highly Assortative + Large Average Degree)

#### Range
- Overlapping: `Overlapping Ground-Truth? = True`
- Highly Assortative: `r >= 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                 | Set   | Average Degree | Degree Assortativity |
|-------------------------|-------|----------------|----------------------|
| facebook-network-ego107 | Train | 51.7389        | 0.4316               |

### Network Family 12 (Overlapping + Highly Assortative + Very Large Average Degree)

#### Range
- Overlapping: `Overlapping Ground-Truth? = True`
- Highly Assortative: `r >= 0.35`
- Very Large Average Degree: `a >= 65`

| Network                  | Set   | Average Degree | Degree Assortativity |
|--------------------------|-------|----------------|----------------------|
| facebook-network-ego1912 | Train | 80.7070        | 0.5026               |

---

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                  | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.014385706013361121   | 0.00489799606293479    | 0.009487709950426332   | 2.9370595297582716 | 0.008394112902265499   | 6.457799151480093           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.0035397587392402576  | 0.0008197903486553482  | 0.0027199683905849096  | 4.317882913657506  | 0.0017034846788267827  | 6.457799151480093           | 0.011000761913486937   | True             |
| network_family_03 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.006022762344880978   | 0.005668143736515979   | 0.0003546186083649991  | 1.06256344666781   | 0.005842763272772687   | 6.457799151480093           | 0.03773139170521051    | True             |
| network_family_04 | cora                               | 7  | False                       | 123                     | 123                               | 0.001427264404617993   | 0.0011103937035788426  | 0.00031687070103915025 | 1.285367883497415  | 0.001258898490041999   | 6.457799151480093           | 0.00812971360079279    | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.9915720946770424e-05 | 1.5119887617540195e-05 | 4.795833329230229e-06  | 1.317187101554029  | 1.7352909339285446e-05 | 6.457799151480093           | 0.00011206160320694854 | True             |
| network_family_06 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.0001405193796735945  | 0.00011388446551794507 | 2.6634914155649443e-05 | 1.233876622544736  | 0.0001265028634025353  | 6.457799151480093           | 0.0008169300839406946  | True             |
| network_family_07 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 6.0026900568653244e-05 | 4.356550563553372e-05  | 1.6461394933119523e-05 | 1.3778538706938126 | 5.113807070087104e-05  | 6.457799151480093           | 0.000330239389580414   | True             |
| network_family_08 | facebook-network-ego698            | 9  | False                       | 18                      | 18                                | 4.734806803854547e-05  | 3.149842751471736e-05  | 1.5849640523828106e-05 | 1.5031883104774835 | 3.861851484811437e-05  | 6.457799151480093           | 0.0002493906124175744  | True             |
| network_family_09 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.369125557765422e-06  | 3.049546292086883e-06  | 3.1957926567853897e-07 | 1.1047956761659266 | 3.2053555734518276e-06 | 6.457799151480093           | 2.06995425024292e-05   | True             |
| network_family_09 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 8.410582162852648e-06  | 8.013293256600164e-06  | 3.972889062524842e-07  | 1.0495787304333655 | 8.209534781561544e-06  | 6.457799151480093           | 5.3015526746414444e-05 | True             |
| network_family_09 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.714185131809789e-05  | 1.8629538583949107e-05 | 3.8512312734148785e-05 | 3.0672714227785725 | 3.2627079610176386e-05 | 6.457799151480093           | 0.00021069912702187052 | True             |
| network_family_10 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.994146059893707e-06  | 5.650729825612766e-06  | 1.3434162342809413e-06 | 1.2377420750487325 | 6.286654893131432e-06  | 6.457799151480093           | 4.0597954634512334e-05 | True             |
| network_family_11 | facebook-network-ego107            | 9  | False                       | 68                      | 68                                | 0.0005686779807201585  | 0.00039259678174269634 | 0.00017608119897746214 | 1.4485039286258434 | 0.0004725051799490343  | 6.457799151480093           | 0.0030513435501448223  | True             |
| network_family_12 | facebook-network-ego1912           | 45 | False                       | 56                      | 56                                | 6.379573842856359e-11  | 5.6704384443152e-12    | 5.812529998424839e-11  | 11.25058301135795  | 1.901972154814059e-11  | 6.457799151480093           | 1.2282554167496995e-10 | True             |

### Thresholds by Network Family

| Network Family    | #Networks | #Valid Thresholds | Median Normalized Threshold | Median Raw Threshold   | Median gap_K           | Median ratio_K     | Threshold              |
|-------------------|-----------|-------------------|-----------------------------|------------------------|------------------------|--------------------|------------------------|
| network_family_01 | 1         | 1                 | 0.008394112902265499        | 0.05420749517767824    | 0.009487709950426332   | 2.9370595297582716 | 0.05420749517767824    |
| network_family_02 | 1         | 1                 | 0.0017034846788267827       | 0.011000761913486937   | 0.0027199683905849096  | 4.317882913657506  | 0.011000761913486937   |
| network_family_03 | 1         | 1                 | 0.005842763272772687        | 0.03773139170521051    | 0.0003546186083649991  | 1.06256344666781   | 0.03773139170521051    |
| network_family_04 | 1         | 1                 | 0.001258898490041999        | 0.00812971360079279    | 0.00031687070103915025 | 1.285367883497415  | 0.00812971360079279    |
| network_family_05 | 1         | 1                 | 1.7352909339285446e-05      | 0.00011206160320694854 | 4.795833329230229e-06  | 1.317187101554029  | 0.00011206160320694854 |
| network_family_06 | 1         | 1                 | 0.0001265028634025353       | 0.0008169300839406946  | 2.6634914155649443e-05 | 1.233876622544736  | 0.0008169300839406946  |
| network_family_07 | 1         | 1                 | 5.113807070087104e-05       | 0.000330239389580414   | 1.6461394933119523e-05 | 1.3778538706938126 | 0.000330239389580414   |
| network_family_08 | 1         | 1                 | 3.861851484811437e-05       | 0.0002493906124175744  | 1.5849640523828106e-05 | 1.5031883104774835 | 0.0002493906124175744  |
| network_family_09 | 3         | 3                 | 8.209534781561544e-06       | 5.3015526746414444e-05 | 3.972889062524842e-07  | 1.1047956761659266 | 5.3015526746414444e-05 |
| network_family_10 | 1         | 1                 | 6.286654893131432e-06       | 4.0597954634512334e-05 | 1.3434162342809413e-06 | 1.2377420750487325 | 4.0597954634512334e-05 |
| network_family_11 | 1         | 1                 | 0.0004725051799490343       | 0.0030513435501448223  | 0.00017608119897746214 | 1.4485039286258434 | 0.0030513435501448223  |
| network_family_12 | 1         | 1                 | 1.901972154814059e-11       | 1.2282554167496995e-10 | 5.812529998424839e-11  | 11.25058301135795  | 1.2282554167496995e-10 |

---

### Test Network Assignment

| Network                            | Overlapping Ground-Truth? | Average Degree | Degree Assortativity | Combination                                                        | Assigned Family     | Calibrated? |
|------------------------------------|---------------------------|----------------|----------------------|--------------------------------------------------------------------|---------------------|-------------|
| word-adjacencies                   | False                     | 7.5893         | -0.1293              | Non-Overlapping + Disassortative + Low Average Degree              | `network_family_02` | Yes         |
| socio-patterns-primary-school-day2 | False                     | 46.5462        | 0.2168               | Non-Overlapping + Moderately Assortative + Large Average Degree    | `network_family_07` | Yes         |
| citeseer                           | False                     | 3.4768         | 0.0071               | Non-Overlapping + Near-Neutral + Low Average Degree                | `network_family_04` | Yes         |
| facebook-network-ego348            | True                      | 28.5000        | 0.2227               | Overlapping + Moderately Assortative + Medium Average Degree       | `network_family_09` | Yes         |
| facebook-network-ego686            | True                      | 19.7143        | 0.0841               | Overlapping + Near-Neutral + Medium Average Degree                 | `network_family_08` | Approx.     |
| facebook-network-ego3980           | True                      | 6.2727         | 0.0530               | Overlapping + Near-Neutral + Low Average Degree                    | `network_family_08` | Yes         |
