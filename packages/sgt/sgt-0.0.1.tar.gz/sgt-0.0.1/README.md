# Sequence Graph Transform (SGT)

#### Maintained by: Chitta Ranjan, PhD (cran2367@gmail.com).


This is open source code repository for SGT. Sequence Graph Transform extracts the short- and long-term sequence features and embeds them in a finite-dimensional feature space. Importantly, SGT has low computation and can extract any amount of short- to long-term patterns without any increase in the computation. These properties are proved theoretically and demonstrated on real data in this paper: https://arxiv.org/abs/1608.03533.

If using this code or dataset, please cite the following:

[1] Ranjan, Chitta, Samaneh Ebrahimi, and Kamran Paynabar. "Sequence Graph Transform (SGT): A Feature Extraction Function for Sequence Data Mining." arXiv preprint arXiv:1608.03533 (2016).

@article{ranjan2016sequence,
  title={Sequence Graph Transform (SGT): A Feature Extraction Function for Sequence Data Mining},
  author={Ranjan, Chitta and Ebrahimi, Samaneh and Paynabar, Kamran},
  journal={arXiv preprint arXiv:1608.03533},
  year={2016}
}

## Quick validation of your code
Apply the algorithm on a sequence `BBACACAABA`. The parts of SGT, W<sup>(0)</sup> and W<sup>(\kappa)</sup>, in Algorithm 1 & 2 in [1], and the resulting SGT estimate will be (line-by-line execution of `main.R`):

```
alphabet_set <- c("A", "B", "C")  # Denoted by variable V in [1]
seq          <- "BBACACAABA"

kappa <- 5
###### Algorithm 1 ######
sgt_parts_alg1 <- f_sgt_parts(sequence = seq, kappa = kappa, alphabet_set_size = length(alphabet_set))
print(sgt_parts_alg1)
```

*Result*
```
$W0
   A B C
A 10 4 3
B 11 3 4
C  7 2 1

$W_kappa
            A            B            C
A 0.006874761 6.783349e-03 1.347620e-02
B 0.013521602 6.737947e-03 4.570791e-05
C 0.013521604 3.059162e-07 4.539993e-05
```

```
sgt <- f_SGT(W_kappa = sgt_parts_alg1$W_kappa, W0 = sgt_parts_alg1$W0, 
             Len = sgt_parts_alg1$Len, kappa = kappa)  # Set Len = NULL for length-sensitive SGT.
print(sgt)
```

*Result*
```
          A          B         C
A 0.3693614 0.44246287 0.5376371
B 0.4148844 0.46803816 0.1627745
C 0.4541361 0.06869332 0.2144920

```

Similarly, the execution for Algorithm-2 is shown in `main.R`.

## Illustration and use of the code
Open file `main.R` and execute line-by-line to understand the process. In this sample execution, we present SGT estimation from either of the two algorithms presented in [1]. The first part is for understanding the SGT computation process.

In the next part we demonstrate sequence clustering using SGT on a synthesized sample dataset. The sequence lengths in the dataset ranges between (45, 711) with a uniform distribution (hence, average length is ~365). Similar sequences in the dataset has some similar patterns, in turn common substrings. These common substrings can be of any length. Also, the order of the instances of these substrings is arbitrary and random in different sequences. For example, the following two sequences have common patterns. One common subtring in both is `QZTA` which is present arbitrarily in both sequences. The two sequences have other common substrings as well. Other than these commonlities there are significant amount of noise present in the sequences. On average, about 40% of the letters in all sequences in the dataset are noise.

```
AKQZTAEEYTDZUXXIRZSTAYFUIXCPDZUXMCSMEMVDVGMTDRDDEJWNDGDPSVPKJHKQBRKMXHHNLUBXBMHISQ
WEHGXGDDCADPVKESYQXGRLRZSTAYFUOQZTAWTBRKMXHHNWYRYBRKMXHHNPRNRBRKMXHHNPBMHIUSVXBMHI
WXQRZSTAYFUCWRZSTAYFUJEJDZUXPUEMVDVGMTOHUDZUXLOQSKESYQXGRCTLBRKMXHHNNJZDZUXTFWZKES
YQXGRUATSNDGDPWEBNIQZMBNIQKESYQXGRSZTTPTZWRMEMVDVGMTAPBNIRPSADZUXJTEDESOKPTLJEMZTD
LUIPSMZTDLUIWYDELISBRKMXHHNMADEDXKESYQXGRWEFRZSTAYFUDNDGDPKYEKPTSXMKNDGDPUTIQJHKSD
ZUXVMZTDLUINFNDGDPMQZTAPPKBMHIUQIUBMHIEKKJHK
```

```
SDBRKMXHHNRATBMHIYDZUXMTRMZTDLUIEKDEIBQZTAZOAMZTDLUILHGXGDDCAZEXJHKTDOOHGXGDDCAKZH
NEMVDVGMTIHZXDEROEQDEGZPPTDBCLBMHIJMMKESYQXGRGDPTNBRKMXHHNGCBYNDGDPKMWKBMHIDQDZUXI
HKVBMHINQZTAHBRKMXHHNIRBRKMXHHNDISDZUXWBOYEMVDVGMTNTAQZTA
```

Identifying similar sequences with good accuracy, and also low false positives (calling sequences similar when they are not) is difficult in such situations due to, 

1. _Different lengths of the sequences_: due to different lengths figuring out that two sequences have same inherent pattern is not straightforward. Normalizing the pattern features by the sequence length is a non-trivial problem.

2. _Commonalities are not in order_: as shown in the above example sequences, the common substrings are anywhere. This makes methods such as alignment-based approaches infeasible.

3. _Significant amount of noise_: a good amount of noise is a nemesis to most sequence similarity algorithms. It often results into high false positives.

### SGT Clustering

The dataset here is a good example for the above challenges. We run clustering on the dataset in `main.R`. The sequences in the dataset are from 5 (=K) clusters. We use this ground truth about the number of clusters as input to our execution below. Although, in reality, the true number of clusters is unknown for a data, here we are demonstrating the SGT implementation. Regardless, using the _random search procedure_ discussed in Sec.SGT-ALGORITHM in [1], we could find the number of clusters as equal to 5. For simplicity it has been kept out of this demonstration.

> Other state-of-the-art sequence clustering methods had significantly poorer performance even with the number of true clusters (K=5). HMM had good performance but significantly higher computation time.


```
## The dataset contains all roman letters, A-Z.
dataset <- read.csv("dataset.csv", header = T, stringsAsFactors = F)

sgt_parts_sequences_in_dataset <- f_SGT_for_each_sequence_in_dataset(sequence_dataset = dataset, 
                                                                     kappa = 5, alphabet_set = LETTERS, 
                                                                     spp = NULL, sgt_using_alphabet_positions = T)
  
  
input_data <- f_create_input_kmeans(all_seq_sgt_parts = sgt_parts_sequences_in_dataset, 
                                    length_normalize = T, 
                                    alphabet_set_size = 26, 
                                    kappa = 5, trace = TRUE, 
                                    inv.powered = T)
K = 5
clustering_output <- f_kmeans(input_data = input_data, K = K, alphabet_set_size = 26, trace = T)

cc <- f_clustering_accuracy(actual = c(strtoi(dataset[,1])), pred = c(clustering_output$class), K = K, type = "f1")
print(cc)
```
*Result*
```
$cc
Confusion Matrix and Statistics

          Reference
Prediction  a  b  c  d  e
         a 50  0  0  0  0
         b  0 66  0  0  0
         c  0  0 60  0  0
         d  0  0  0 55  0
         e  0  0  0  0 68

Overall Statistics
                                     
               Accuracy : 1          
                 95% CI : (0.9877, 1)
    No Information Rate : 0.2274     
    P-Value [Acc > NIR] : < 2.2e-16  
                                     
                  Kappa : 1          
 Mcnemar's Test P-Value : NA         

Statistics by Class:

                     Class: a Class: b Class: c Class: d Class: e
Sensitivity            1.0000   1.0000   1.0000   1.0000   1.0000
Specificity            1.0000   1.0000   1.0000   1.0000   1.0000
Pos Pred Value         1.0000   1.0000   1.0000   1.0000   1.0000
Neg Pred Value         1.0000   1.0000   1.0000   1.0000   1.0000
Prevalence             0.1672   0.2207   0.2007   0.1839   0.2274
Detection Rate         0.1672   0.2207   0.2007   0.1839   0.2274
Detection Prevalence   0.1672   0.2207   0.2007   0.1839   0.2274
Balanced Accuracy      1.0000   1.0000   1.0000   1.0000   1.0000

$F1
F1 
 1 
```

As we can see the clustering result is accurate with no false-positives. The f1-score is 1.0.

> Note: Do not run function `f_clustering_accuracy` when `K` is larger (> 7), because it does a permutation operation which will become expensive.

### PCA on SGT & Clustering

For demonstrating PCA on SGT for dimension reduction and then performing clustering, we added another code snippet. PCA becomes more important on datasets where SGT's are sparse. A sparse SGT is present when the alphabet set is large but the observed sequences contain only a few of those alphabets. For example, the alphabet set for sequence dataset of music listening history will have thousands to millions of songs, but a single sequence will have only a few of them

```
######## Clustering on Principal Components of SGT features ########
num_pcs <- 5  # Number of principal components we want
input_data_pcs <- f_pcs(input_data = input_data, PCs = num_pcs)$input_data_pcs

clustering_output_pcs <- f_kmeans(input_data = input_data_pcs, K = K, alphabet_set_size = sqrt(num_pcs), trace = F)

cc <- f_clustering_accuracy(actual = c(strtoi(dataset[,1])), pred = c(clustering_output_pcs$class), K = K, type = "f1")  
print(cc)
```

*Result*
```
$cc
Confusion Matrix and Statistics

          Reference
Prediction  a  b  c  d  e
         a 50  0  0  0  0
         b  0 66  0  0  0
         c  0  0 60  0  0
         d  0  0  0 55  0
         e  0  0  0  0 68

Overall Statistics
                                     
               Accuracy : 1          
                 95% CI : (0.9877, 1)
    No Information Rate : 0.2274     
    P-Value [Acc > NIR] : < 2.2e-16  
                                     
                  Kappa : 1          
 Mcnemar's Test P-Value : NA         

Statistics by Class:

                     Class: a Class: b Class: c Class: d Class: e
Sensitivity            1.0000   1.0000   1.0000   1.0000   1.0000
Specificity            1.0000   1.0000   1.0000   1.0000   1.0000
Pos Pred Value         1.0000   1.0000   1.0000   1.0000   1.0000
Neg Pred Value         1.0000   1.0000   1.0000   1.0000   1.0000
Prevalence             0.1672   0.2207   0.2007   0.1839   0.2274
Detection Rate         0.1672   0.2207   0.2007   0.1839   0.2274
Detection Prevalence   0.1672   0.2207   0.2007   0.1839   0.2274
Balanced Accuracy      1.0000   1.0000   1.0000   1.0000   1.0000

$F1
F1 
 1 
 ```

The clustering result remains accurate upon clustering the PCs on the SGT of sequences.


-----------------------
#### Comments:
1. Simplicity: SGT's is simple to implement. There is no numerical optimization or other solution search algorithm required to estimate SGT. This makes it deterministic and powerful.
2. Length sensitive: The length sensitive version of SGT can be easily tried by changing the marked arguments in `main.R`.

#### Note:
1. Small alphabet set: If the alphabet set is small (< 4), SGT's performance may not be good. This is because the feature space becomes too small.
2. Faster implementation: The provided code is a research level code, not optimized for the best of speed. Significant speed improvements can be made, e.g. multithreading the SGT estimation for sequences in a dataset.

#### Additional resource:
Python implementation: Please refer to 

https://github.com/datashinobi/Sequence-Graph-transform

Thanks to Yassine for providing the Python implementation.