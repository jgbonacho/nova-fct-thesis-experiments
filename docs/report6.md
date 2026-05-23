# Report 6 - Add more networks and divide into train and test sets



## Table of Contents

- [Real-World Networks](#real-world-networks)
- [Scripts](#scripts)
- [Experience 9 (One network per family)](#experience-9-one-network-per-family)
- [Experience 10 (Networks grouped by degree assortativity and average degree)](#experience-10-networks-grouped-by-degree-assortativity-and-average-degree)
- [Experience 11 (Networks grouped by degree assortativity, average degree, and K)](#experience-11-networks-grouped-by-degree-assortativity-average-degree-and-k)
- [Experience 12](#experience-12)



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
| Facebook Ego-3980 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 52    | 146   | 4   | 44        | 138       | 0.8462            | Yes                       | 11     | Train |
| Facebook Ego-414 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 150   | 1693  | 2   | 148       | 1692      | 0.9867            | Yes                       | 7      | Train |
| Facebook Ego-686 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 168   | 1656  | 1   | 168       | 1656      | 1.0000            | Yes                       | 14     | Train |
| Facebook Ego-348 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 224   | 3192  | 1   | 224       | 3192      | 1.0000            | Yes                       | 14     | Train |
| Facebook Ego-0 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                         | Online Social                     | Yes           | 333   | 2519  | 5   | 324       | 2514      | 0.9730            | Yes                       | 22     | Train |
| Facebook Ego-3437 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 534   | 4813  | 2   | 532       | 4812      | 0.9963            | Yes                       | 32     | Train |
| Facebook Ego-1684 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 786   | 14024 | 4   | 775       | 14006     | 0.9860            | Yes                       | 17     | Train |
| Facebook Ego-698 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 61    | 270   | 3   | 40        | 220       | 0.6557            | Yes                       | 9      | Test  |
| Facebook Ego-1912 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                      | Online Social                     | Yes           | 747   | 30025 | 2   | 744       | 30023     | 0.9960            | Yes                       | 45     | Test  |
| Facebook Ego-107 Network [[6](https://snap.stanford.edu/data/egonets-Facebook.html)]                                                       | Online Social                     | Yes           | 1034  | 26749 | 1   | 1034      | 26749     | 1.0000            | Yes                       | 9      | Test  |

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
| facebook-network-ego3980           | True          | 44        | 138       | 1.0        | 18.0       | 6.2727272727272725 | 4.206106504106863  | 0.6705387180460217  | 2.8695652173913047 | 0.14587737843551796   | 0.854122621564482  | 0.44404332129963897           | 0.05297863564191894   | 0.4547680965795939  | True                      | 0.0                  | 11 | 0.25                  | 1.0                | 21.0               | 4.0                    | 5.932958789676531  | 1.4832396974191326  | 0                       | 0.0                              |
| facebook-network-ego414            | True          | 148       | 1692      | 1.0        | 57.0       | 22.864864864864863 | 12.951846268016066 | 0.5664519053387641  | 2.49290780141844   | 0.15554329840044126   | 0.8444567015995588 | 0.6457982767359352            | 0.3039224601932676    | 0.6793500241563419  | True                      | 0.2537313432835821   | 7  | 0.0472972972972973    | 7.0                | 55.0               | 24.285714285714285     | 21.63880993118834  | 0.8910098206959906  | 14                      | 0.0945945945945946               |
| facebook-network-ego686            | True          | 168       | 1656      | 1.0        | 77.0       | 19.714285714285715 | 16.068767957698487 | 0.8150824326368797  | 3.905797101449275  | 0.11804961505560307   | 0.8819503849443969 | 0.45355939944054346           | 0.08406304044981644   | 0.5337913395248177  | True                      | 0.8035714285714286   | 14 | 0.08333333333333333   | 4.0                | 101.0              | 34.42857142857143      | 30.88617885003006  | 0.8971089292539851  | 0                       | 0.0                              |
| facebook-network-ego348            | True          | 224       | 3192      | 1.0        | 99.0       | 28.5               | 22.417561981665038 | 0.7865811221636856  | 3.473684210526316  | 0.12780269058295965   | 0.8721973094170403 | 0.4902791105177521            | 0.22269166051622483   | 0.5442814709697877  | True                      | 0.8532110091743119   | 14 | 0.0625                | 4.0                | 201.0              | 40.357142857142854     | 55.757175658049945 | 1.3815937331198218  | 6                       | 0.026785714285714284             |
| facebook-network-ego0              | True          | 324       | 2514      | 1.0        | 77.0       | 15.518518518518519 | 15.570959005850767 | 1.003379219947424   | 4.9618138424821    | 0.04804494897374154   | 0.9519550510262584 | 0.4258750132177223            | 0.23295552356572546   | 0.5223624457077098  | True                      | 0.1417910447761194   | 22 | 0.06790123456790123   | 1.0                | 129.0              | 13.909090909090908     | 27.300635071819762 | 1.9627907567974994  | 56                      | 0.1728395061728395               |
| facebook-network-ego3437           | True          | 532       | 4812      | 1.0        | 107.0      | 18.090225563909776 | 14.664847676938885 | 0.810650349556472   | 5.91479634247714   | 0.034068221400960025  | 0.96593177859904   | 0.4488933226158351            | 0.22207842776444284   | 0.545768617282594   | True                      | 0.6804123711340206   | 32 | 0.06015037593984962   | 1.0                | 50.0               | 6.0                    | 9.315266692284613  | 1.5525444487141022  | 435                     | 0.8176691729323309               |
| facebook-network-ego1684           | True          | 775       | 14006     | 1.0        | 136.0      | 36.144516129032255 | 28.476378855199318 | 0.7878478370976536  | 3.762673140082822  | 0.046698341251979664  | 0.9533016587480203 | 0.45225878166971445           | 0.3268349056797533    | 0.4713855751563139  | True                      | 0.006640106241699867 | 17 | 0.02193548387096774   | 1.0                | 223.0              | 44.705882352941174     | 62.501764680969565 | 1.3980657889164245  | 22                      | 0.02838709677419355              |

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

[Open Folder](../results/real-world/experience9/results_2026-05-20_23-17-29-135362/)

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                   | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|-------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.013474631779406379   | 0.004587796618652595   | 0.008886835160753784    | 2.9370595297582716 | 0.007862497702075937   | 6.894437013745113           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.003315579058469454   | 0.0007678714603358617  | 0.0025477075981335923   | 4.317882913657505  | 0.0015955997410020913  | 6.894437013745113           | 0.011000761913486935   | True             |
| network_family_03 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.00013162001901148934 | 0.00010667194483354212 | 2.4948074177947224e-05  | 1.233876622544736  | 0.00011849119548296976 | 6.894437013745113           | 0.0008169300839406946  | True             |
| network_family_04 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 5.622528232332908e-05  | 4.0806418967359045e-05 | 1.5418863355970036e-05  | 1.3778538706938128 | 4.789939902591486e-05  | 6.894437013745113           | 0.000330239389580414   | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.8654420306511066e-05 | 1.4162316260539154e-05 | 4.492104045971912e-06   | 1.3171871015540293 | 1.6253916452284153e-05 | 6.894437013745113           | 0.00011206160320694853 | True             |
| network_family_06 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.0056413293040168365  | 0.005309169369328483   | 0.0003321599346883539   | 1.0625634466678102 | 0.005472729916886211   | 6.894437013745113           | 0.03773139170521051    | True             |
| network_family_07 | cora                               | 7  | False                       | 123                     | 123                               | 0.0013368730242519214  | 0.0010400703498319591  | 0.00029680267441996224  | 1.2853678834974152 | 0.0011791700445714373  | 6.894437013745113           | 0.008129713600792792   | True             |
| network_family_08 | facebook-network-ego3980           | 11 | False                       | 27                      | 27                                | 0.000563086250800279   | 0.00046345263965951914 | 9.963361114075981e-05   | 1.2149812140760636 | 0.0005108461698881292  | 6.894437013745113           | 0.0035219967420066422  | True             |
| network_family_09 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 7.877923932939047e-06  | 7.505796091815136e-06  | 3.7212784112391064e-07  | 1.0495787304333655 | 7.68960926624174e-06   | 6.894437013745113           | 5.301552674641446e-05  | True             |
| network_family_10 | facebook-network-ego686            | 14 | False                       | 36                      | 36                                | 7.660644930794983e-05  | 8.779684620698289e-05  | -1.1190396899033055e-05 | 0.8725421540467244 | 8.201100321513634e-05  | 6.894437013745113           | 0.0005654196961008055  | False            |
| network_family_11 | facebook-network-ego348            | 14 | False                       | 45                      | 45                                | 1.805603997986206e-05  | 1.7604500238246384e-05 | 4.5153974161567595e-07  | 1.0256491087792818 | 1.7828840683770437e-05 | 6.894437013745113           | 0.00012291981912235163 | True             |
| network_family_12 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.1557524022325917e-06 | 2.8564127017443515e-06 | 2.993397004882402e-07   | 1.1047956761659266 | 3.0023542837742225e-06 | 6.894437013745113           | 2.06995425024292e-05   | True             |
| network_family_13 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.352294875133897e-05  | 1.7449694328926956e-05 | 3.607325442241202e-05   | 3.0672714227785725 | 3.05607443511065e-05   | 6.894437013745113           | 0.00021069912702187054 | True             |
| network_family_14 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.551193433323493e-06  | 5.292858314657808e-06  | 1.2583351186656849e-06  | 1.2377420750487327 | 5.888509033235653e-06  | 6.894437013745113           | 4.059795463451234e-05  | True             |

### Sensitivity Analysis

| Group           | Threshold Mode | Threshold Label      | Property                         | N  | Spearman Correlation  | Pearson Correlation    | Abs Spearman Correlation |
|-----------------|----------------|----------------------|----------------------------------|----|-----------------------|------------------------|--------------------------|
| All             | k_boundary     | Normalized Threshold | Degree Assortativity             | 13 | -0.901098901098901    | -0.8834098671291699    | 0.901098901098901        |
| All             | k_boundary     | Normalized Threshold | K                                | 13 | -0.772420406005624    | -0.628957654436284     | 0.772420406005624        |
| All             | k_boundary     | Normalized Threshold | Min Community Size               | 13 | 0.7404084698829895    | 0.5130937770256254     | 0.7404084698829895       |
| All             | k_boundary     | Normalized Threshold | Nodes Without Community          | 13 | -0.7329699161351603   | -0.22422174471774728   | 0.7329699161351603       |
| All             | k_boundary     | Normalized Threshold | Nodes Fraction Without Community | 13 | -0.7267052159972528   | -0.2804073531177612    | 0.7267052159972528       |
| All             | k_boundary     | Normalized Threshold | Community Size CV                | 13 | -0.7087912087912087   | -0.699496712685139     | 0.7087912087912087       |
| All             | k_boundary     | Normalized Threshold | Overlap Fraction                 | 13 | -0.6640582146181793   | -0.38939124243336815   | 0.6640582146181793       |
| All             | k_boundary     | Normalized Threshold | Global Clustering Coefficient    | 13 | -0.6593406593406593   | -0.6604642871739118    | 0.6593406593406593       |
| All             | k_boundary     | Normalized Threshold | Average Degree                   | 13 | -0.5549450549450549   | -0.5034688848117569    | 0.5549450549450549       |
| All             | k_boundary     | Normalized Threshold | Degree Std                       | 13 | -0.40659340659340654  | -0.28659081554891813   | 0.40659340659340654      |
| All             | k_boundary     | Normalized Threshold | Community Size Std               | 13 | -0.3516483516483516   | 0.09559306925932706    | 0.3516483516483516       |
| All             | k_boundary     | Normalized Threshold | Average Clustering               | 13 | -0.2912087912087912   | -0.43118140670923233   | 0.2912087912087912       |
| All             | k_boundary     | Normalized Threshold | Edges LCC                        | 13 | -0.2802197802197803   | -0.11164311204840663   | 0.2802197802197803       |
| All             | k_boundary     | Normalized Threshold | Max Community Size               | 13 | -0.2692307692307692   | 0.3363546757863123     | 0.2692307692307692       |
| All             | k_boundary     | Normalized Threshold | Nodes LCC                        | 13 | -0.2582417582417582   | 0.1917495383977734     | 0.2582417582417582       |
| All             | k_boundary     | Normalized Threshold | Community Proportion             | 13 | -0.21978021978021978  | -0.0004973600380072601 | 0.21978021978021978      |
| All             | k_boundary     | Normalized Threshold | Min Degree                       | 13 | 0.21178618420050904   | -0.06816426832609057   | 0.21178618420050904      |
| All             | k_boundary     | Normalized Threshold | Max Degree                       | 13 | -0.1868131868131868   | 0.020664337985571882   | 0.1868131868131868       |
| All             | k_boundary     | Normalized Threshold | Degree CV                        | 13 | 0.12087912087912088   | 0.2386872923512264     | 0.12087912087912088      |
| All             | k_boundary     | Normalized Threshold | Average Community Size           | 13 | 0.09890109890109891   | 0.5187425295362768     | 0.09890109890109891      |
| All             | k_boundary     | Normalized Threshold | Degree Hub Ratio                 | 13 | 0.049450549450549455  | 0.30937454582667245    | 0.049450549450549455     |
| All             | k_boundary     | Normalized Threshold | Density                          | 13 | -0.049450549450549455 | -0.04396368995772857   | 0.049450549450549455     |
| All             | k_boundary     | Normalized Threshold | Sparsity                         | 13 | 0.049450549450549455  | 0.043963689957728584   | 0.049450549450549455     |



## Experience 10 (Networks grouped by degree assortativity and average degree)

[Open Folder](../results/real-world/experience10/results_2026-05-21_16-27-50-276433/)

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

### Network Family 1 (Strongly Disassortative + Low Average Degree)

#### Range
- Strongly Disassortative: `r < -0.30`
- Low Average Degree: `a < 15`

| Network             | Average Degree | Degree Assortativity |
|---------------------|----------------|----------------------|
| zachary-karate-club | 4.5882         | -0.4756              |

### Network Family 2 (Disassortative + Low Average Degree)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Low Average Degree: `a < 15`

| Network                 | Average Degree | Degree Assortativity |
|-------------------------|----------------|----------------------|
| books-about-us-politics | 8.4000         | -0.1279              |

### Network Family 3 (Disassortative + Medium Average Degree)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Medium Average Degree: `15 <= a < 35`

| Network            | Average Degree | Degree Assortativity |
|--------------------|----------------|----------------------|
| us-political-blogs | 27.3552        | -0.2213              |

### Network Family 4 (Near-Neutral + Low Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`

| Network                  | Average Degree | Degree Assortativity |
|--------------------------|----------------|----------------------|
| cora                     | 4.0797         | -0.0714              |
| facebook-network-ego3980 | 6.2727         | 0.0530               |

### Network Family 5 (Near-Neutral + Medium Average Degree)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`

| Network                 | Average Degree | Degree Assortativity |
|-------------------------|----------------|----------------------|
| email-eu-core           | 32.5842        | -0.0257              |
| facebook-network-ego686 | 19.7143        | 0.0841               |

### Network Family 6 (Moderately Assortative + Low Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Low Average Degree: `a < 15`

| Network                   | Average Degree | Degree Assortativity |
|---------------------------|----------------|----------------------|
| american-college-football | 10.6609        | 0.1624               |

### Network Family 7 (Moderately Assortative + Medium Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`

| Network                  | Average Degree | Degree Assortativity |
|--------------------------|----------------|----------------------|
| facebook-network-ego0    | 15.5185        | 0.2330               |
| facebook-network-ego3437 | 18.0902        | 0.2221               |
| facebook-network-ego414  | 22.8649        | 0.3039               |
| facebook-network-ego348  | 28.5000        | 0.2227               |

### Network Family 8 (Moderately Assortative + Large Average Degree)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`

| Network                            | Average Degree | Degree Assortativity |
|------------------------------------|----------------|----------------------|
| facebook-network-ego1684           | 36.1445        | 0.3268               |
| socio-patterns-primary-school-day1 | 49.9915        | 0.1729               |

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                   | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|-------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.013474631779406379   | 0.004587796618652595   | 0.008886835160753784    | 2.9370595297582716 | 0.007862497702075937   | 6.894437013745113           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.003315579058469454   | 0.0007678714603358617  | 0.0025477075981335923   | 4.317882913657505  | 0.0015955997410020913  | 6.894437013745113           | 0.011000761913486935   | True             |
| network_family_03 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.0056413293040168365  | 0.005309169369328483   | 0.0003321599346883539   | 1.0625634466678102 | 0.005472729916886211   | 6.894437013745113           | 0.03773139170521051    | True             |
| network_family_04 | cora                               | 7  | False                       | 123                     | 123                               | 0.0013368730242519214  | 0.0010400703498319591  | 0.00029680267441996224  | 1.2853678834974152 | 0.0011791700445714373  | 6.894437013745113           | 0.008129713600792792   | True             |
| network_family_04 | facebook-network-ego3980           | 11 | False                       | 27                      | 27                                | 0.000563086250800279   | 0.00046345263965951914 | 9.963361114075981e-05   | 1.2149812140760636 | 0.0005108461698881292  | 6.894437013745113           | 0.0035219967420066422  | True             |
| network_family_05 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.8654420306511066e-05 | 1.4162316260539154e-05 | 4.492104045971912e-06   | 1.3171871015540293 | 1.6253916452284153e-05 | 6.894437013745113           | 0.00011206160320694853 | True             |
| network_family_05 | facebook-network-ego686            | 14 | False                       | 36                      | 36                                | 7.660644930794983e-05  | 8.779684620698289e-05  | -1.1190396899033055e-05 | 0.8725421540467244 | 8.201100321513634e-05  | 6.894437013745113           | 0.0005654196961008055  | False            |
| network_family_06 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.00013162001901148934 | 0.00010667194483354212 | 2.4948074177947224e-05  | 1.233876622544736  | 0.00011849119548296976 | 6.894437013745113           | 0.0008169300839406946  | True             |
| network_family_07 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.1557524022325917e-06 | 2.8564127017443515e-06 | 2.993397004882402e-07   | 1.1047956761659266 | 3.0023542837742225e-06 | 6.894437013745113           | 2.06995425024292e-05   | True             |
| network_family_07 | facebook-network-ego348            | 14 | False                       | 45                      | 45                                | 1.805603997986206e-05  | 1.7604500238246384e-05 | 4.5153974161567595e-07  | 1.0256491087792818 | 1.7828840683770437e-05 | 6.894437013745113           | 0.00012291981912235163 | True             |
| network_family_07 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 7.877923932939047e-06  | 7.505796091815136e-06  | 3.7212784112391064e-07  | 1.0495787304333655 | 7.68960926624174e-06   | 6.894437013745113           | 5.301552674641446e-05  | True             |
| network_family_07 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.352294875133897e-05  | 1.7449694328926956e-05 | 3.607325442241202e-05   | 3.0672714227785725 | 3.05607443511065e-05   | 6.894437013745113           | 0.00021069912702187054 | True             |
| network_family_08 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.551193433323493e-06  | 5.292858314657808e-06  | 1.2583351186656849e-06  | 1.2377420750487327 | 5.888509033235653e-06  | 6.894437013745113           | 4.059795463451234e-05  | True             |
| network_family_08 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 5.622528232332908e-05  | 4.0806418967359045e-05 | 1.5418863355970036e-05  | 1.3778538706938128 | 4.789939902591486e-05  | 6.894437013745113           | 0.000330239389580414   | True             |

### Thresholds by Network Family

| Network Family    | #Networks | #Valid Thresholds | Median Normalized Threshold | Median Raw Threshold   | Median gap_K           | Median ratio_K     | Threshold              |
|-------------------|-----------|-------------------|-----------------------------|------------------------|------------------------|--------------------|------------------------|
| network_family_01 | 1         | 1                 | 0.007862497702075937        | 0.05420749517767824    | 0.008886835160753784   | 2.9370595297582716 | 0.05420749517767824    |
| network_family_02 | 1         | 1                 | 0.0015955997410020913       | 0.011000761913486935   | 0.0025477075981335923  | 4.317882913657505  | 0.011000761913486935   |
| network_family_03 | 1         | 1                 | 0.005472729916886211        | 0.03773139170521051    | 0.0003321599346883539  | 1.0625634466678102 | 0.03773139170521051    |
| network_family_04 | 2         | 2                 | 0.0008450081072297832       | 0.005825855171399717   | 0.00019821814278036103 | 1.2501745487867395 | 0.005825855171399717   |
| network_family_05 | 2         | 1                 | 1.6253916452284153e-05      | 0.00011206160320694853 | 4.492104045971912e-06  | 1.3171871015540293 | 0.00011206160320694853 |
| network_family_06 | 1         | 1                 | 0.00011849119548296976      | 0.0008169300839406946  | 2.4948074177947224e-05 | 1.233876622544736  | 0.0008169300839406946  |
| network_family_07 | 4         | 4                 | 1.2759224975006089e-05      | 8.796767293438304e-05  | 4.118337913697933e-07  | 1.077187203299646  | 8.796767293438304e-05  |
| network_family_08 | 2         | 2                 | 2.6893954029575258e-05      | 0.00018541867210746318 | 8.33859923731786e-06   | 1.3077979728712728 | 0.00018541867210746318 |



## Experience 11 (Networks grouped by degree assortativity, average degree, and K)

[Open Folder](../results/real-world/experience11/results_2026-05-21_17-43-41-217845/)

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

### Network Family 1 (Strongly Disassortative + Low Average Degree + Low K)

#### Range
- Strongly Disassortative: `r < -0.30`
- Low Average Degree: `a < 15`
- Low K: `K <= 5`

| Network             | Degree Assortativity | Average Degree | K |
|---------------------|----------------------|----------------|---|
| zachary-karate-club | -0.4756              | 4.5882         | 2 |

### Network Family 2 (Disassortative + Low Average Degree + Low K)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Low Average Degree: `a < 15`
- Low K: `K <= 5`

| Network                 | Degree Assortativity | Average Degree | K |
|-------------------------|----------------------|----------------|---|
| books-about-us-politics | -0.1279              | 8.4000         | 3 |

### Network Family 3 (Disassortative + Medium Average Degree + Low K)

#### Range
- Disassortative: `-0.30 <= r < -0.10`
- Medium Average Degree: `15 <= a < 35`
- Low K: `K <= 5`

| Network            | Degree Assortativity | Average Degree | K |
|--------------------|----------------------|----------------|---|
| us-political-blogs | -0.2213              | 27.3552        | 2 |

### Network Family 4 (Near-Neutral + Low Average Degree + Medium K)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Low Average Degree: `a < 15`
- Medium K: `6 <= K <= 20`

| Network                  | Degree Assortativity | Average Degree | K  |
|--------------------------|----------------------|----------------|----|
| cora                     | -0.0714              | 4.0797         | 7  |
| facebook-network-ego3980 | 0.0530               | 6.2727         | 11 |

### Network Family 5 (Near-Neutral + Medium Average Degree + Medium K)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`
- Medium K: `6 <= K <= 20`

| Network                 | Degree Assortativity | Average Degree | K  |
|-------------------------|----------------------|----------------|----|
| facebook-network-ego686 | 0.0841               | 19.7143        | 14 |

### Network Family 6 (Near-Neutral + Medium Average Degree + Very Large K)

#### Range
- Near-Neutral: `-0.10 <= r < 0.10`
- Medium Average Degree: `15 <= a < 35`
- Very Large K: `K > 40`

| Network       | Degree Assortativity | Average Degree | K  |
|---------------|----------------------|----------------|----|
| email-eu-core | -0.0257              | 32.5842        | 42 |

### Network Family 7 (Moderately Assortative + Low Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Low Average Degree: `a < 15`
- Medium K: `6 <= K <= 20`

| Network                   | Degree Assortativity | Average Degree | K  |
|---------------------------|----------------------|----------------|----|
| american-college-football | 0.1624               | 10.6609        | 12 |

### Network Family 8 (Moderately Assortative + Medium Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`
- Medium K: `6 <= K <= 20`

| Network                 | Degree Assortativity | Average Degree | K  |
|-------------------------|----------------------|----------------|----|
| facebook-network-ego414 | 0.3039               | 22.8649        | 7  |
| facebook-network-ego348 | 0.2227               | 28.5000        | 14 |

### Network Family 9 (Moderately Assortative + Medium Average Degree + Large K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Medium Average Degree: `15 <= a < 35`
- Large K: `21 <= K <= 40`

| Network                  | Degree Assortativity | Average Degree | K  |
|--------------------------|----------------------|----------------|----|
| facebook-network-ego0    | 0.2330               | 15.5185        | 22 |
| facebook-network-ego3437 | 0.2221               | 18.0902        | 32 |

### Network Family 10 (Moderately Assortative + Large Average Degree + Medium K)

#### Range
- Moderately Assortative: `0.10 <= r < 0.35`
- Large Average Degree: `35 <= a < 65`
- Medium K: `6 <= K <= 20`

| Network                            | Degree Assortativity | Average Degree | K  |
|------------------------------------|----------------------|----------------|----|
| facebook-network-ego1684           | 0.3268               | 36.1445        | 17 |
| socio-patterns-primary-school-day1 | 0.1729               | 49.9915        | 11 |

### Thresholds by Network

| Network Family    | Network                            | K  | First Contribution Removed? | Number of Contributions | Effective Number of Contributions | Normalized c_K         | Normalized c_K+1       | gap_K                   | ratio_K            | Normalized Threshold   | Global Normalization Factor | Raw Threshold          | Valid Threshold? |
|-------------------|------------------------------------|----|-----------------------------|-------------------------|-----------------------------------|------------------------|------------------------|-------------------------|--------------------|------------------------|-----------------------------|------------------------|------------------|
| network_family_01 | zachary-karate-club                | 2  | False                       | 19                      | 19                                | 0.013474631779406379   | 0.004587796618652595   | 0.008886835160753784    | 2.9370595297582716 | 0.007862497702075937   | 6.894437013745113           | 0.05420749517767824    | True             |
| network_family_02 | books-about-us-politics            | 3  | False                       | 6                       | 6                                 | 0.003315579058469454   | 0.0007678714603358617  | 0.0025477075981335923   | 4.317882913657505  | 0.0015955997410020913  | 6.894437013745113           | 0.011000761913486935   | True             |
| network_family_03 | us-political-blogs                 | 2  | False                       | 69                      | 69                                | 0.0056413293040168365  | 0.005309169369328483   | 0.0003321599346883539   | 1.0625634466678102 | 0.005472729916886211   | 6.894437013745113           | 0.03773139170521051    | True             |
| network_family_04 | cora                               | 7  | False                       | 123                     | 123                               | 0.0013368730242519214  | 0.0010400703498319591  | 0.00029680267441996224  | 1.2853678834974152 | 0.0011791700445714373  | 6.894437013745113           | 0.008129713600792792   | True             |
| network_family_04 | facebook-network-ego3980           | 11 | False                       | 27                      | 27                                | 0.000563086250800279   | 0.00046345263965951914 | 9.963361114075981e-05   | 1.2149812140760636 | 0.0005108461698881292  | 6.894437013745113           | 0.0035219967420066422  | True             |
| network_family_05 | facebook-network-ego686            | 14 | False                       | 36                      | 36                                | 7.660644930794983e-05  | 8.779684620698289e-05  | -1.1190396899033055e-05 | 0.8725421540467244 | 8.201100321513634e-05  | 6.894437013745113           | 0.0005654196961008055  | False            |
| network_family_06 | email-eu-core                      | 42 | False                       | 63                      | 63                                | 1.8654420306511066e-05 | 1.4162316260539154e-05 | 4.492104045971912e-06   | 1.3171871015540293 | 1.6253916452284153e-05 | 6.894437013745113           | 0.00011206160320694853 | True             |
| network_family_07 | american-college-football          | 12 | False                       | 43                      | 43                                | 0.00013162001901148934 | 0.00010667194483354212 | 2.4948074177947224e-05  | 1.233876622544736  | 0.00011849119548296976 | 6.894437013745113           | 0.0008169300839406946  | True             |
| network_family_08 | facebook-network-ego348            | 14 | False                       | 45                      | 45                                | 1.805603997986206e-05  | 1.7604500238246384e-05 | 4.5153974161567595e-07  | 1.0256491087792818 | 1.7828840683770437e-05 | 6.894437013745113           | 0.00012291981912235163 | True             |
| network_family_08 | facebook-network-ego414            | 7  | False                       | 27                      | 27                                | 7.877923932939047e-06  | 7.505796091815136e-06  | 3.7212784112391064e-07  | 1.0495787304333655 | 7.68960926624174e-06   | 6.894437013745113           | 5.301552674641446e-05  | True             |
| network_family_09 | facebook-network-ego0              | 22 | False                       | 43                      | 43                                | 3.1557524022325917e-06 | 2.8564127017443515e-06 | 2.993397004882402e-07   | 1.1047956761659266 | 3.0023542837742225e-06 | 6.894437013745113           | 2.06995425024292e-05   | True             |
| network_family_09 | facebook-network-ego3437           | 32 | False                       | 66                      | 66                                | 5.352294875133897e-05  | 1.7449694328926956e-05 | 3.607325442241202e-05   | 3.0672714227785725 | 3.05607443511065e-05   | 6.894437013745113           | 0.00021069912702187054 | True             |
| network_family_10 | facebook-network-ego1684           | 17 | False                       | 36                      | 36                                | 6.551193433323493e-06  | 5.292858314657808e-06  | 1.2583351186656849e-06  | 1.2377420750487327 | 5.888509033235653e-06  | 6.894437013745113           | 4.059795463451234e-05  | True             |
| network_family_10 | socio-patterns-primary-school-day1 | 11 | False                       | 22                      | 22                                | 5.622528232332908e-05  | 4.0806418967359045e-05 | 1.5418863355970036e-05  | 1.3778538706938128 | 4.789939902591486e-05  | 6.894437013745113           | 0.000330239389580414   | True             |

### Thresholds by Network Family

| Network Family    | #Networks | #Valid Thresholds | Median Normalized Threshold | Median Raw Threshold   | Median gap_K           | Median ratio_K     | Threshold              |
|-------------------|-----------|-------------------|-----------------------------|------------------------|------------------------|--------------------|------------------------|
| network_family_01 | 1         | 1                 | 0.007862497702075937        | 0.05420749517767824    | 0.008886835160753784   | 2.9370595297582716 | 0.05420749517767824    |
| network_family_02 | 1         | 1                 | 0.0015955997410020913       | 0.011000761913486935   | 0.0025477075981335923  | 4.317882913657505  | 0.011000761913486935   |
| network_family_03 | 1         | 1                 | 0.005472729916886211        | 0.03773139170521051    | 0.0003321599346883539  | 1.0625634466678102 | 0.03773139170521051    |
| network_family_04 | 2         | 2                 | 0.0008450081072297832       | 0.005825855171399717   | 0.00019821814278036103 | 1.2501745487867395 | 0.005825855171399717   |
| network_family_05 | 1         | 0                 |                             |                        |                        |                    |                        |
| network_family_06 | 1         | 1                 | 1.6253916452284153e-05      | 0.00011206160320694853 | 4.492104045971912e-06  | 1.3171871015540293 | 0.00011206160320694853 |
| network_family_07 | 1         | 1                 | 0.00011849119548296976      | 0.0008169300839406946  | 2.4948074177947224e-05 | 1.233876622544736  | 0.0008169300839406946  |
| network_family_08 | 2         | 2                 | 1.2759224975006089e-05      | 8.796767293438304e-05  | 4.118337913697933e-07  | 1.0376139196063237 | 8.796767293438304e-05  |
| network_family_09 | 2         | 2                 | 1.678154931744036e-05       | 0.00011569933476214988 | 1.818629706145013e-05  | 2.0860335494722495 | 0.00011569933476214988 |
| network_family_10 | 2         | 2                 | 2.6893954029575258e-05      | 0.00018541867210746318 | 8.33859923731786e-06   | 1.3077979728712728 | 0.00018541867210746318 |



## Experience 12

### Structural Properties

| Network                            | Ground-Truth? | Nodes LCC | Edges LCC | Min Degree | Max Degree | Average Degree    | Degree Std         | Degree CV           | Degree Hub Ratio   | Density               | Sparsity           | Global Clustering Coefficient | Degree Assortativity  | Average Clustering  | Overlapping Ground-Truth? | Overlap Fraction    | K  | Community Proportion | Min Community Size | Max Community Size | Average Community Size | Community Size Std | Community Size CV   | Nodes Without Community | Nodes Fraction Without Community |
|------------------------------------|---------------|-----------|-----------|------------|------------|-------------------|--------------------|---------------------|--------------------|-----------------------|--------------------|-------------------------------|-----------------------|---------------------|---------------------------|---------------------|----|----------------------|--------------------|--------------------|------------------------|--------------------|---------------------|-------------------------|----------------------------------|
| word-adjacencies                   | True          | 112       | 425       | 1.0        | 49.0       | 7.589285714285714 | 6.8819565249517245 | 0.9067989774054037  | 6.456470588235294  | 0.06837194337194337   | 0.9316280566280566 | 0.15693497881746177           | -0.1293478534390013   | 0.17284007981036792 | False                     | 0.0                 | 0  | 0.0                  |                    |                    |                        |                    |                     | 112                     | 1.0                              |
| socio-patterns-primary-school-day2 | True          | 238       | 5539      | 8.0        | 88.0       | 46.54621848739496 | 19.892007130129983 | 0.42736032650035527 | 1.8905939700306913 | 0.19639754636031628   | 0.8036024536396837 | 0.46816525721161883           | 0.21681961190098284   | 0.559558532849634   | False                     | 0.0                 | 11 | 0.046218487394957986 | 10.0               | 26.0               | 21.636363636363637     | 4.177863742936747  | 0.19309454274077403 | 0                       | 0.0                              |
| citeseer                           | True          | 2110      | 3668      | 1.0        | 99.0       | 3.476777251184834 | 3.9983615708750007 | 1.1500194812631204  | 28.47464558342421  | 0.0016485430304337763 | 0.9983514569695662 | 0.12523609451489803           | 0.0071366166694059475 | 0.17106997537906155 | False                     | 0.0                 | 6  | 0.002843601895734597 | 115.0              | 532.0              | 351.6666666666667      | 145.89402546597535 | 0.41486452739139906 | 0                       | 0.0                              |
| facebook-network-ego698            | True          | 40        | 220       | 1.0        | 29.0       | 11.0              | 5.808923286082348  | 0.5280839350983952  | 2.6363636363636362 | 0.28205128205128205   | 0.717948717948718  | 0.6560531840447865            | 0.012473574916280844  | 0.7249190619129633  | True                      | 0.59375             | 9  | 0.225                | 1.0                | 15.0               | 6.444444444444445      | 6.125991983163035  | 0.9505849629046089  | 8                       | 0.2                              |
| facebook-network-ego1912           | True          | 744       | 30023     | 1.0        | 293.0      | 80.70698924731182 | 64.25341111081488  | 0.7961319299611344  | 3.630416680544916  | 0.10862313492235777   | 0.8913768650776422 | 0.7000214679657459            | 0.5026087042032253    | 0.6379667606225469  | True                      | 0.36415362731152207 | 45 | 0.06048387096774194  | 1.0                | 232.0              | 23.333333333333332     | 45.70010940905941  | 1.9585761175311176  | 41                      | 0.05510752688172043              |
| facebook-network-ego107            | True          | 1034      | 26749     | 1.0        | 253.0      | 51.73887814313346 | 47.02619707281583  | 0.9089141233932403  | 4.88993981083405   | 0.05008603886072939   | 0.9499139611392706 | 0.5045088189930924            | 0.4315692408853532    | 0.5264047980773338  | True                      | 0.03958333333333333 | 9  | 0.008704061895551257 | 10.0               | 307.0              | 55.55555555555556      | 94.95539888693943  | 1.7091971799649097  | 554                     | 0.5357833655705996               |

---

### Experience 10-based

| Network                            | Average Degree | Degree Assortativity | Assigned Family                            | Family Description                             |
|------------------------------------|----------------|----------------------|--------------------------------------------|------------------------------------------------|
| word-adjacencies                   | 7.5893         | -0.1293              | `network_family_02`                        | Disassortative + Low Average Degree            |
| socio-patterns-primary-school-day2 | 46.5462        | 0.2168               | `network_family_08`                        | Moderately Assortative + Large Average Degree  |
| citeseer                           | 3.4768         | 0.0071               | `network_family_04`                        | Near-Neutral + Low Average Degree              |
| facebook-network-ego698            | 11.0000        | 0.0125               | `network_family_04`                        | Near-Neutral + Low Average Degree              |
| facebook-network-ego1912           | 80.7070        | 0.5026               | `network_family_08` (No calibrated family) | Highly Assortative + Very Large Average Degree |
| facebook-network-ego107            | 51.7389        | 0.4316               | `network_family_08` (No calibrated family) | Highly Assortative + Large Average Degree      |

### Experience 11-based

| Network                            | Average Degree | Degree Assortativity | K  | Assigned Family                            | Family Description                                            |
|------------------------------------|----------------|----------------------|----|--------------------------------------------|---------------------------------------------------------------|
| word-adjacencies                   | 7.5893         | -0.1293              | 2  | `network_family_02`                        | Disassortative + Low Average Degree + Low K                   |
| socio-patterns-primary-school-day2 | 46.5462        | 0.2168               | 11 | `network_family_10`                        | Moderately Assortative + Large Average Degree + Medium K      |
| citeseer                           | 3.4768         | 0.0071               | 6  | `network_family_04`                        | Near-Neutral + Low Average Degree + Medium K                  |
| facebook-network-ego698            | 11.0000        | 0.0125               | 9  | `network_family_04`                        | Near-Neutral + Low Average Degree + Medium K                  |
| facebook-network-ego1912           | 80.7070        | 0.5026               | 45 | `network_family_10` (No calibrated family) | Highly Assortative + Very Large Average Degree + Very Large K |
| facebook-network-ego107            | 51.7389        | 0.4316               | 9  | `network_family_10` (No calibrated family) | Highly Assortative + Large Average Degree + Medium K          |
