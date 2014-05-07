[&laquo; Brian Karfunkel home](http://bkfunk.github.io)

Rating Wikipedia
===========

What makes a good Wikipedia page?

Using data on ratings for Wikipedia pages, I try to explore that question.

Wikimedia provides a one-year dump of all ratings on Wikipedia, from July 22, 2011 up to July 22, 2012. This file contains almost 50 million records of almost 12 million unique ratings (NB: there are 4 dimensions for each rating, so one person rating an article will provide up to 4 data points).

The file (approx 441.6 MB gzipped) is hosted here:
http://datahub.io/dataset/wikipedia-article-ratings/resource/8a218330-6ac3-40d1-ae0d-4224f57db214

## Cleaning Data
The first step was cleaning the ratings data. The iPython Notebook showing all the cleaning code and output is [here][cleaning notebook]. In addition to reshaping the data so that each rating has one observation, rather than four, I cut the data to a sample of some TK,000 ratings for 10,000 pages.

## Exploring Data
My exploratory analysis is documented [here][exploring notebook]. I start by looking at the ratings themselves:
+ __How is the number of ratings distributed across pages and versions (revisions) of pages?__
  
  As with a lot of data dealing with popularity (e.g. population of cities), the data appear to follow [Zipf's law](https://en.wikipedia.org/wiki/Zipf's_law) insofar as a small number of pages get a huge number of ratings, but the number of ratings quickly drops off, ending with a long right tail. Here is a chart illustrating the distribution:
![Chart of distribution of ratings per page (in sample)][ratings per page chart]

+ __How is the value of ratings distributed across pages and versions?__

  Most ratings tend to be high on the 1-5 scale.
  ![Chart of distribution of rating values][rating values chart]
  However, given the rest of the distribution, there is a larger-than-expected frequency of low ratings (namely, `1`s). This bimodality, where there is a peak in the ratings distribution around __TK__ and then around __TK__, is relatively consistent across rating dimensions, and it becomes much more pronounced when looking at pages with high numbers of ratings. This could mean that having a higher `N`, and thus a theoretically more reliable measure of the true ratings distribution, results in a clearer picture of a fundamental, bimodal pattern. However, it could also mean that pages with many ratings are in some way different; for example, pages with higher ratings could be more *controversial*, leading some to simply give low ratings because they disagree with the *content of the page itself*, rather than judging the completeness, trustworthiness, objectivity, or quality of writing.
  
+ __How consistent are the ratings for a single page or version?__


[cleaning notebook]:
[exploring notebook]:
[ratings per page chart]:summary/ratings_per_page_chart.png "Distribution of Ratings perPage"
[rating values chart]:summary/dist_of_ratings_and_dims.png "Distribution of Rating Values and Dimensions Rated"


