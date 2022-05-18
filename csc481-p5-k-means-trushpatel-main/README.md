[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7809917&assignment_repo_type=AssignmentRepo)
# CSC481 - Artificial Intelligence

### Machine Learning - The k-means algorithm

[![Points badge](../../blob/badges/.github/badges/points.svg)](../../actions)

## Introduction

The k-means algorithm is a simple but powerful unsupervised learning tool. In this programming assignment, you will implement a generic version of k-means that will take a set of arbitrary vectors of continuous values and perform k-means on them.

As a reminder, the algorithm is as follows:

1. select *k* vectors from *s* as the estimate of the means <img src="https://render.githubusercontent.com/render/math?math=\mu_1, ... \mu_k">.
2. create *k* empty sets, <img src="https://render.githubusercontent.com/render/math?math=g_1, ... g_k">.
3. for each vector, *v*, in the *s* put *v* in the set <img src="https://render.githubusercontent.com/render/math?math=g_j"> where *v* is closest to <img src="https://render.githubusercontent.com/render/math?math=\mu_j">
4. compute <img src="https://render.githubusercontent.com/render/math?math=\mu_1, ... \mu_k"> by taking the means of <img src="https://render.githubusercontent.com/render/math?math=g_1, ... g_k">
5. repeat until the means stop changing.


You'll be working with 2 data sets. The [plot_data](plot_data.ipynb) jupyter notebook has examples of reading in the files and plotting 2D comparisons of the data sets using python.

## Implementation

Your implementation may not use any libraries that have already implemented kmeans. You must implement the k-means algorithm yourself. You do not have to use python, but you must submit your source code of the language that you use, and you must visualize your results, and put this visualization in your report.


## Submission

Please submit the kmeans clustering code that you wrote as well as any helper code you wrote to visualize your results. Also, create a report of the tasks. This may be in a jupyter notebook or a markdown file posted to this repository.

## Tasks

### Task 1

Implement k-means for a vector of dimension 1.
Test your implementation on the vector \[1,2,3,7,8,9,15,16,17\]  
If you run it multiple times, do you end up with the same final means each time?

### Task 2

Extend your implementation to work with up to at least 4 dimensions.
Test your implementation on all of the features of the iris data set.  
If you run it multiple times, do you end up with the same final means each time?

### Task 3

Test your implementation on the aggregation.csv data set. Run *k-means* using 2 through 11 means, compute the sum of squared differences from the closest mean, and plot the sum as a function of *k*. What number of *k* is at the elbow of the plot? How far away is the elbow from the number of actual classes (7)?


### Finished?

Please make sure that you understand all of the code you wrote. Make sure that all of your code and report of your tasks and tests is submitted, then modify the [autograding.json](.github/classroom/autograding.json) file so that the tests pass.




