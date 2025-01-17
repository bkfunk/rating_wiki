[&laquo; Brian Karfunkel home](http://bkfunk.github.io)

Rating Wikipedia
================

__Overview__
------------

What makes a good Wikipedia page?

Using data on ratings for Wikipedia pages, I try to explore that question.

### About the data
Wikimedia provides a one-year dump of all ratings on Wikipedia, from July 22, 2011 up to July 22, 2012. This file contains almost 50 million records of almost 12 million unique ratings (NB: there are 4 dimensions for each rating, so one person rating an article will provide up to 4 data points).

The file (approx 441.6 MB gzipped) is hosted here:
http://datahub.io/dataset/wikipedia-article-ratings/resource/8a218330-6ac3-40d1-ae0d-4224f57db214

There are 4 dimensions on which a page could be rated:

1. Trustworthy (`trust` in my cleaned dataset)
2. Objective (`obj`)
3. Complete (`comp`)
4. Well-written (`writ`)

A user could rate _any_ or _all_ dimensions for each page. In the data provided, in addition to the values for each rating dimension, we have:

- Timestamp when the rating was submitted
- `page_id` and page title, identifying the page being rated
- `rev_id` identifying the particular version (i.e. "revision") of the page that was rated
- An indicator variable (`1` or `0`) indicating whether the user rating the page was logged in (the actual user's identity is anonymized out of the data)

Given the anonymized data, it is impossible to know whether users were able to rate a page more than once, but given the fact that most of the ratings come from non-logged-in users, it is certainly possible.

### Motivating questions

My goal for this analysis was to first analyze the ratings data itself to see whether the ratings seemed to provide a useful measure of page quality. Then, I wanted to combine the ratings data with data on the actual page versions rated to look at how different kinds of edits affect the page's rating. Namely, is there a way to quantify which edits do the most to improve a page in any or all of the four rating dimensions? For example, are big edits (based on number of characters edited) better than small edits? Do small edits improve score for quality of writing (`writ`), while big edits improve completeness (`comp`)? Are logged-in users better editors than anonymous users?

If there were a way to identify particularly helpful edits in terms of improving article quality, then Wikipedia could:

- **Give feedback** to editors to help them learn to make the most effective edits, and give editors a sense of quantified accomplishment to keep them engaged
- **Highlight pages** in particular need of quality improvements for editors that are particularly good at providing such improvements (for example, prioritizing articles that are poorly written for editors that are good at revising prose and copyediting)
- Create more bots to make certain **algorithmic edits**
- **Identify editors** that are malicious or that consistently degrade page quality

**Cleaning Data**
-----------------
The first step was cleaning the ratings data. The iPython Notebook showing all the cleaning code and output is [here][cleaning notebook]. In addition to reshaping the data so that each rating has one observation, rather than four, I cut the data to a sample of some 79,000 ratings for 10,000 different pages.

**Exploring Data**
------------------
My exploratory analysis is documented [here][exploring notebook]. I start by looking at the ratings themselves.

#### 1. **How is the number of ratings distributed across pages and versions (revisions) of pages?**
  
In order for ratings to be any kind of measure of page quality, people have to actually rate pages. How many ratings to pages get in the year-long sample? And do some pages get significantly more than others?

As with a lot of data dealing with popularity (e.g. population of cities), the data appear to follow [Zipf's law](https://en.wikipedia.org/wiki/Zipf's_law) insofar as a small number of pages get a huge number of ratings, but the number of ratings quickly drops off, ending with a long right tail. Here is a chart illustrating the distribution:

> ###### _Figure 1_

> ![Chart of distribution of ratings per page (in sample)][ratings per page chart]

The average page in the sample has **7.85 ratings** in the year-long period (standard deviation of 42.1), though of course the sample is of pages with at least one rating in that period. The most-rated page in my sample is "The Hunger Games" with 2,713 ratings. The average page has **3.66 different versions** in the sample, with each version being rated an average of **1.63 times**.

#### 2. **How is the value of ratings distributed across pages and versions?**

Most ratings tend to be high on the 1-5 scale.
    
> ###### _Figure 2_

> ![Chart of distribution of rating values][rating values chart]

> The above chart shows the distribution of average rating value for each observation. The first plot is the distribution of `rating_all_mean`, which is the mean of the 4 rating dimensions _when all 4 dimensions are rated_ (and NA otherwise), while the second plot is the distribution of `rating_any_mean`, which is the mean of all rating dimensions _that are present_ (whether there is only 1 dimension rated, or 4, etc.). Note that, for both of these histograms (and all similar histograms below), each bin does **not** include the right-most boundary **_except_** the last, which includes ratings with means from 4.5 to 5, _inclusive_. The third plot shows the proportions of each rating observation that have 1, 2, 3, or 4 dimensions rated.
  
__Over 40% of observations have ratings that average 4.5 or greater on a scale of 5__. Furthermore, __almost 70% of users rated all 4 dimensions__, while about 25% rated only one dimension, and very few rated 2 or 3. When all four dimensions are rated, the **mean rating is 3.66**, with a **standard deviation of 1.34**, and the **median is 4.0**.
  
Given the rest of the distribution, there is a larger-than-expected frequency of low ratings (namely, `1`s). This bimodality, where there is a peak in the ratings distribution around `[4.5, 5]` and then around `[1, 1.5)`, is relatively consistent across rating dimensions.
  
> ###### _Figure 3_

> ![Chart of distribution of each rating dimension][rating dimension values chart]

While the rightmost peak (at rating value of 5) is lower for "Complete", __all 4 dimensions have another peak at a rating value of 1__.
  
Thus, it appears that raters __tend to rate pages at the extremes__, either very high or very low. This is true regardless of whether the user rates only 1 dimension or all 4 (see the [complete exploration][exploring notebook] for charts illustrating this).
  
#### 3. **Are rating dimensions meaningful?**
    
Is it worth asking users to rate 4 dimensions instead of simply giving each page a 1-5 rating? **Each dimension is highly correlated with each other dimension**, indicating that a user who gives a high rating to "Complete", for example, is very likely to give a high rating to "Well-written". Here is a table of Pearson correlations between each dimension:

> ###### _Table 1_

> | Correlation by Dimension  | Complete     | Objective    | Trustworthy  | Well-written |
|-----------------------------|--------------|--------------|--------------|--------------|
| Complete                    | 1.000000     | 0.715450     | 0.749500     | 0.764108     |
| Objective                   | **0.715450** | 1.000000     | 0.774930     | 0.738221     |
| Trustworthy                 | **0.749500** | **0.774930** | 1.000000     | 0.753312     |
| Well-written                | **0.764108** | **0.738221** | **0.753312** | 1.000000     |


But, the correlation is not perfect. So, though there is not a whole lot of new information in each dimension, there is some, and depending on the cost to the user to rate each dimension, it may still make sense to have separate categories.
    
The means for each dimension do generally differ significantly, however, using a paired difference test. For example, here are the p-values from a Wilcoxon test comparing each dimension to each other dimension:

> ###### _Table 2_

> | Wilcoxon Signed-Rank Test       | Complete     | Objective    | Trustworthy  | Well-written |
|-----------------------------------|--------------|--------------|--------------|--------------|
|                          Complete | X            | 0.000        | 0.000        | 0.000        |
|                         Objective | **0.000**    | X            | 0.000        | 0.153        |
|                       Trustworthy | **0.000**    | **0.000**    | X            | 0.000        |
|                      Well-written | **0.000**    | **0.153**    | **0.000**    | X            | 

> Figures reported are **p-values** from a Wilcoxon Signed-Rank test performed for each combination of rating dimensions.

All are significantly different with the exception of "Objective" and "Well-Written", which has a p-value of 0.153.

#### 4. **How consistent are the ratings for a single page or version?**

If ratings are indeed useful measures of page quality, and if page quality is something that is consistent for various users of Wikipedia, then we would hope that ratings cluster around the mean. That is, we would want most people to tend to give ratings that are close to a certain average. The bimodality reflected in #2 above might indicate that this is not the case, however.
    
There are many ways to measure the spread of data like this, but I will focus on the [_mean absolute deviation_ (MAD)](https://en.wikipedia.org/wiki/Absolute_deviation), which is simply the mean of the absolute value of the difference between each observation's value and the mean or median value. Given the fact that both the mean and median rating is quite high, and that rating values are truncated at 5, the distance from the point of central tendency (mean or median) can be higher for lower ratings. Thus it doesn't make as much sense to use the standard deviation, which weights bigger deviations more (since it's the square root of the mean _squared_ error). The MAD can be easily understood as the average difference between a particular rating and the mean/median for all ratings for that page/version.

> ###### _Table 3_

> | Distribution of MAD by Page                     | Count  | **Mean**  |  25%  |  50%  |  75%  |
|---------------------------------------------------|--------|-----------|-------|-------|-------|
| Abs. Dev. from Page Mean - Mean of All Dim.       | 49,712 | **0.956** | 0.395 | 0.820 | 1.333 |
| Abs. Dev. from Page Median - Mean of All Dim.     | 49,712 | **0.905** | 0.250 | 0.625 | 1.250 |
| Abs. Dev. from Page Mean - "Complete"             | 55,500 | **1.126** | 0.500 | 1.059 | 1.624 | 
| Abs. Dev. from Page Mean - "Objective"            | 53,265 | **1.103** | 0.500 | 1.000 | 1.500 | 
| Abs. Dev. from Page Mean - "Trustworthy"          | 56,986 | **1.117** | 0.500 | 0.981 | 1.509 | 
| Abs. Dev. from Page Mean - "Well-Written"         | 60,508 | **1.040** | 0.500 | 0.893 | 1.418 |

> Only pages with at least 2 ratings were included for this table. The computation for the above table is as follows: 1) Compute the mean/median rating for all observations for a given page; 2) for each observation, calculate the absolute value of the difference between that observation's rating for the particular dimension (or the mean of all dimensions). Thus, the `Mean` column constitutes the MAD for the given dimension. Note that for the first two rows, labeled `Mean of All Dim.`, all observations with less than all 4 dimensions rated are excluded; for the remaining rows, all non-missing ratings for that dimension are included, regardless of whether other dimensions were also rated in that observation.
  
> ----------------
> ###### _Table 4_

> | Distribution of MAD by Version                     | Count | **Mean**  |  25%  |  50%  |  75%  |
|------------------------------------------------------|-------|-----------|-------|-------|-------|
| Abs. Dev. from Version Mean - Mean of All Dim.       | 34515 | **0.817** | 0.275 | 0.649 | 1.200 |
| Abs. Dev. from Version Median - Mean of All Dim.     | 34515 | **0.758** | 0.125 | 0.500 | 1.125 |
| Abs. Dev. from Version Mean - "Complete"             | 37403 | **0.960** | 0.400 | 0.826 | 1.500 | 
| Abs. Dev. from Version Mean - "Objective"            | 36317 | **0.933** | 0.333 | 0.750 | 1.400 | 
| Abs. Dev. from Version Mean - "Trustworthy"          | 38216 | **0.958** | 0.333 | 0.800 | 1.484 | 
| Abs. Dev. from Version Mean - "Well-Written"         | 39920 | **0.902** | 0.333 | 0.722 | 1.333 |

> Only versions with at least 2 ratings were included for this table. See also note to Table 3 above.

Even though the sample only covers a year, it is of course possible that pages would differ significantly between ratings. However, when looking at _versions_ of pages, we see MADs that are smaller, but still relatively large in magnitude. To put this in perspective, consider a version of an article that has only 2 ratings; Table 4 indicates that the average of all 4 rating dimensions for those two ratings would tend to be about 1.6 points apart on a 1-5 scale, meaning that if one rating was a 5 (very high), on average the other rating would be a 3.4 (very mediocre, given the fact that most ratings are, in fact, 4s or 5s).

To further illustrate this, here are plots of the distributions of the _non-absolute_ differences between each observation and the average for that version:

> ###### _Figure 4_

> ![Chart of distribution of deviation from version average][diff version avg 2]

> ###### _Figure 5_

> ![Chart of distribution of deviation from version average][diff version avg 4]

> ###### _Figure 6_

> ![Chart of distribution of deviation from version average][diff version avg 6]

> <small>The cutoffs of 2, 4, and 6 were chosen because they represent 100%, 25%, and 10%, respectively, of the sample of versions with at least 2 ratings</small>.

Though there initially appears to be just a rightward skew to the distributions, as we get more ratings per version, the familiar bimodal pattern begins to show up again. Furthermore, the bimodality becomes much more pronounced when looking at versions with even higher numbers of ratings, and it is also more pronounced when looking at pages, rather than versions of pages (no doubt in part because pages tend to have higher numbers of ratings per page, and thus there is more information).
  
On the one hand, the fact that this bimodality is more clear with a higher `N` (i.e. more ratings per version) could indicate that we simply have more information and thus have clearer picture of what could be a fundamental, bimodal pattern. However, it could also mean that pages with many ratings are in some way different; for example, pages with higher ratings could be more *controversial*, leading some to simply give low ratings because they disagree with the *content of the page itself*, rather than judging the completeness, trustworthiness, objectivity, or quality of writing.

#### 5. Do different kinds of users rate pages differently?

In the dataset, the only information we have about the user rating the page is whether they are logged in or not. Still, given that most users are not logged in, being logged in could indicate that the user is more aware of the standards of Wikipedia, and thus is a better judge of article quality. It could also be that logged-in users are more invested in the quality of Wikipedia and thus will put more effort into providing a full and accurate rating. Still another option is that logged-in users are more likely to have edited the pages themselves, and thus may be either rating their own work or giving a low rating before deciding to edit the page.

> ###### _Figure 7_

> ![Chart of distribution of ratings based on logged-in status][logged in rating dist]

Here it appears that **logged-in users are less likely to give low ratings**. When I look at the MAD for logged-in vs. not logged-in users, the logged-in users have MADs that are significantly (p-value < 0.001) lower than users who are not logged in, meaning that not only are logged-in users less likely to give low ratings, but they tend to give ratings that are closer to ratings for other logged-in users.

#### 5. Do pages increase in quality over time?

In my [exploratory analysis][exploring notebook], I look at the rating history for the most frequently edited and rated pages, trying to find a pattern of improving quality over time. Here, for example, are plots of the history for three pages that have many versions and high numbers of ratings per version:

> ###### _Figure 8_

> ![Chart of page rating history: "Arithmetic Progression"][page rate hist 1]

> ###### _Figure 9_

> ![Chart of page rating history: "List of spells in Harry Potter"][page rate hist 2]

> ###### _Figure 10_

> ![Chart of page rating history: "United States Declaration of Independence"][page rate hist 3]

> The boxplot for each page shows the distribution of `rating_all_mean` (i.e. the mean rating when all 4 dimensions are recorded) for each version of the page in our dataset, indexed by version number (rather than, say, date the version was made). The blue line and circles trace the mean, while the red lines are the median.

There certainly does not appear to be a broad upward trend. Indeed, when I look at correlations for all pages in the data set, **there is almost no correlation between version number and rating value**:

> ###### _Table 5_

> | Correlation | Mean Rating, Any Dimensions | Mean Rating, All Dimensions | "Complete" | "Objective" | "Trustworthy" | "Well-Written" |
|-------------|--------------|-----------|-----------|-----------|-----------|----------|
| nth_version | 0.063059	 | 0.063983	 | 0.096140	 | 0.035822	 | 0.051972	 | 0.049783 |

It is possible that, if I can combine versions that, due to the edits being very minor, are essentially the same, that a different trend could emerge. But as of now, there is not much evidence that pages get better over time when quality is measured by user ratings.

**Next Steps**
-----------------

I am currently working on merging in data about the actual edits (and other data) from the MediaWiki API. Once I do that, I'll be able to see if certain kinds of edits affect ratings in different ways. For example:

- Do edits that change a bigger portion of the page have a bigger effect on ratings?
- Do minor edits have a different effect on ratings?
- Do edits by logged-in users have a more positive effect on ratings?
- Does adding links increase the rating for trustworthiness or objectivity?
- How are ratings correlated to length of the page? To number of links? To amount of data attached to infoboxes?




----------


[cleaning notebook]: Cleaning_Wiki_Ratings.html
[exploring notebook]: exploring_wiki_ratings.html
[ratings per page chart]: summary/ratings_per_page_chart.png "Distribution of Ratings per Page"
[rating values chart]: summary/dist_of_ratings_and_dims.png "Distribution of Rating Values and Dimensions Rated"
[rating dimension values chart]: summary/dist_of_each_dimension.png "Distribution of Each Rating Dimension"
[diff version avg 2]: summary/dev_from_version_avg_2.png "Distribution of Deviation from Version Average - 2+ ratings"
[diff version avg 4]: summary/dev_from_version_avg_4.png "Distribution of Deviation from Version Average - 4+ ratings"
[diff version avg 6]: summary/dev_from_version_avg_6.png "Distribution of Deviation from Version Average - 6+ ratings"
[logged in rating dist]: summary/logged_in_rating_dist.png "Distribution of Ratings based on Logged-In Status"
[page rate hist 1]: summary/page_rate_hist1.png "Chart of page rating history: Arithmetic Progression"
[page rate hist 2]: summary/page_rate_hist2.png "Chart of page rating history: List of spells in Harry Potter"
[page rate hist 3]: summary/page_rate_hist3.png "Chart of page rating history: United States Declaration of Independence"




