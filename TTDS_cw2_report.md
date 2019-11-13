# TTDS_cw2 report

This report consists of two projects. The first project is to calculating the following measures of six different IR systems: **P@10**, **R@50**, **r-precision**, **MAP**, **nDCG@10**, **nDCG10**, **nDCG20**. The second project is to build a text classification model for classifying text.

## IR EVALUATION

The following table is the score of each system on measures.

|      | p@10 | **R@50** | r-Precision | AP    | nDCG@10 | nDCG@20 |
| ---- | ---- | -------- | ----------- | ----- | ------- | ------- |
| s1   | 0.39 | 0.834    | 0.401       | 0.4   | 0.363   | 0.485   |
| s2   | 0.22 | 0.867    | 0.253       | 0.3   | 0.2     | 0.246   |
| s3   | 0.41 | 0.767    | 0.449       | 0.451 | 0.42    | 0.511   |
| s4   | 0.08 | 0.189    | 0.049       | 0.075 | 0.069   | 0.076   |
| s5   | 0.41 | 0.767    | 0.358       | 0.364 | 0.333   | 0.424   |
| s6   | 0.41 | 0.767    | 0.449       | 0.445 | 0.4     | 0.49    |

The following table is about the best system according to each measure.

|         |    P@10    | R@50  | r-Precision |  AP   | nDCG@10 | nDCG@20 |
| ------- | :--------: | :---: | :---------: | :---: | :-----: | :-----: |
| Best    | s3, s5, s6 |  s2   |   s3, s6    |  s3   |   s3    |   s3    |
| Value   |    0.41    | 0.867 |    0.449    | 0.451 |  0.420  |  0.511  |
| p-value |            |       |             |       |         |         |

我们假设table1中，排名第一的系统比排名第二的系统更好，为了验证这一假设，我们计算排名第一的系统与排名第二的系统的p-value，并将他们的值显示在table2中。通过table2可知，我们的假设正确。



 