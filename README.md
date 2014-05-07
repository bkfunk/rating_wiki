[&laquo; Brian Karfunkel home](http://bkfunk.github.io)

Rating Wikipedia
===========

What makes a good Wikipedia page?

Using data on ratings for Wikipedia pages, I try to explore that question.

Wikimedia provides a one-year dump of all ratings on Wikipedia, from July 22, 2011 up to July 22, 2012. This file contains almost 50 million records of almost 12 million unique ratings (NB: there are 4 dimensions for each rating, so one person rating an article will provide up to 4 data points).

The file (approx 441.6 MB gzipped) is hosted here:
http://datahub.io/dataset/wikipedia-article-ratings/resource/8a218330-6ac3-40d1-ae0d-4224f57db214

There are 4 dimensions on which a page could be rated:
1. Trustworthy (`trust` in my cleaned dataset)
2. Objective (`obj`)
3. Complete (`comp`)
4. Well-written (`writ`)

A user could rate _any_ or _all_ dimensions for each page. In the data provided, in addition to the values for each rating dimension, we have:
* Timestamp when the rating was submitted
* `page_id` and page title, identifying the page being rated
* `rev_id` identifying the particular version (i.e. "revsion") of the page that was rated
* An indicator variable (`1` or `0`) indicating whether the user rating the page was logged in (the actual user's identity is anonymized out of the data)

Given the anonymized data, it is impossible to know whether users were able to rate a page more than once, but given the fact that most of the ratings come from non-logged-in users, it is certainly possible.

My goal for this analysis was to first analyze the ratings data itself to see whether the ratings seemed to provide a useful measure of page quality. Then, I wanted to combine the ratings data with data on the actual page versions rated to look at how different kinds of edits affect the page's rating. Namely, is there a way to quantify which edits do the most to improve a page in any or all of the four rating dimensions? For example, are big edits (based on number of characters edited) better than small edits? Do small edits improve score for quality of writing (`writ`), while big edits improve completeness (`comp`)? Are logged-in users better editors than anonymous users?

If there were a way to identify particularly helpful edits in terms of improving article quality, then Wikipedia could:
* Give feedback to editors to help them learn to make the most effective edits, and give editors a sense of quantified accomplishment to keep them engaged
* Highlight pages in particular need of quality improvements for editors that are particularly good at providing such improvements (for example, prioritizing articles that are poorly written for editors that are good at revising prose and copyediting)
* Create more bots to make certain algorithmic edits
* Identify editors that are malicious or that consistently degrade page quality

## Cleaning Data
The first step was cleaning the ratings data. The iPython Notebook showing all the cleaning code and output is [here][cleaning notebook]. In addition to reshaping the data so that each rating has one observation, rather than four, I cut the data to a sample of some 79,000 ratings for 10,000 different pages.

## Exploring Data
My exploratory analysis is documented [here][exploring notebook]. I start by looking at the ratings themselves:
+ __How is the number of ratings distributed across pages and versions (revisions) of pages?__
  
  As with a lot of data dealing with popularity (e.g. population of cities), the data appear to follow [Zipf's law](https://en.wikipedia.org/wiki/Zipf's_law) insofar as a small number of pages get a huge number of ratings, but the number of ratings quickly drops off, ending with a long right tail. Here is a chart illustrating the distribution:
![Chart of distribution of ratings per page (in sample)][ratings per page chart]

+ __How is the value of ratings distributed across pages and versions?__

  Most ratings tend to be high on the 1-5 scale.
  
  ![Chart of distribution of rating values][rating values chart]
  
  The above chart shows the distribution of average rating value for each observation. The first plot is the distribution of `rating_all_mean`, which is the mean of the 4 rating dimensions *when all 4 dimensions are rated* (and NA otherwise), while the second plot is the distribution of `rating_any_mean`, which is the mean of all rating dimensions *that are present* (whether there is only 1 dimension rated, or 4, etc.). Note that, for both of these histograms (and all similar histograms below), each bin does __not__ include the right-most boundary __*except*__ the last, which includes ratings with means from 4.5 to 5, *inclusive*. The third plot shows the proportions of each rating observation that have 1, 2, 3, or 4 dimensions rated.
  
  __Over 40% of observations have ratings that average 4.5 or greater on a scale of 5__. Furthermore, __almost 70% of users rated all 4 dimensions__, while about 25% rated only one dimension, and very few rated 2 or 3.
  
  Given the rest of the distribution, there is a larger-than-expected frequency of low ratings (namely, `1`s). This bimodality, where there is a peak in the ratings distribution around `[4.5, 5]` and then around `[1, 1.5)`, is relatively consistent across rating dimensions.
  
  ![Chart of distribution of each rating dimension][rating dimension values chart]
  
  
  
+ __How consistent are the ratings for a single page or version?__
Furthermore, the bimodality becomes much more pronounced when looking at pages with high numbers of ratings.
  
  
  This could mean that having a higher `N`, and thus a theoretically more reliable measure of the true ratings distribution, results in a clearer picture of a fundamental, bimodal pattern. However, it could also mean that pages with many ratings are in some way different; for example, pages with higher ratings could be more *controversial*, leading some to simply give low ratings because they disagree with the *content of the page itself*, rather than judging the completeness, trustworthiness, objectivity, or quality of writing.

[cleaning notebook]:
[exploring notebook]:
[ratings per page chart]:summary/ratings_per_page_chart.png "Distribution of Ratings perPage"
[rating values chart]:summary/dist_of_ratings_and_dims.png "Distribution of Rating Values and Dimensions Rated"
[rating dimension values chart]: 


