## Quantitative detection of twitch potentiation
This study presents two complementary methods---statistical parametric mapping and conventional computation of characteristic scalar parameters---for reliably detecting and quantifying twitch potentiation in superficial muscles based on tensiomyography measurements of muscles immediately following short bursts of intense muscular activity.

Keywords: TMG, SPM, twitch potentiation, post-activation potentiation

### Definitions

#### What is twitch potentiation?

> A transient increase in muscle twitch amplitude and speed following intense muscular contraction.

[Source](https://www.atsjournals.org/doi/abs/10.1164/ajrccm.149.3.8118645)

Original: a transient augmentation of twitch tension following vigorous muscular contraction.

- What is statistical parametric mapping?

For our purposes, a technique leveraging the theory of random fields and statistical processes for practical detection of statistically-significant differences between continuous signals directly in the signal domain without dimensionality reduction.

More formally,

> Statistical parametric mapping is the application of Random Field Theory to make inferences about the topological features of statistical processes that are continuous functions of space or time.

[Source](http://www.scholarpedia.org/article/Statistical_parametric_mapping)

SPM has so far found its greatest application in neuroimaging for detecting regionally-specific brain activations, and we use it similarly here---on one-dimensional functions of time (i.e. TMG signals) instead of three-dimensional functions of space (i.e. brain scans)---to detect regionally-specific variations between pre-exercise and post-exercise muscle signals.

#### What are characteristic scalar parameters?

What we have called analysis by "conventional computation of characteristic scalar parameters" refers to...
  
> Reducing a TMG measurement into several characteristic scalar/zero-dimensional numbers (for example maximum twitch amplitude, time taken to reach maximum amplitude, and maximum rate of change of twitch amplitude over time) and using these zero-dimensional (i.e. scalar) numbers as a proxy summarizing the entire 1-dimensional TMG signal.

#### Tensiomyography
TMG is a non-invasive, superficial, mechanical technique that produces a 1 kHz, 1 ms time series signal of muscle displacement with respect to time.

### Introduction

Potentiation is temporary increase in muscle performance shortly following an intense burst of prior muscular activity.

This is interesting in its own right and as a means of improving athletic performance.

Conditioning/activation exercises also cause fatigue.
Fatigue and potentiation appear to be two different phenomenon that can coexist.
Striking a favorable balance between potentiation and fatigue should be of interest to sports scientists, coaches, and athletes alike.
Doing so requires a reliable means of detecting and quantifying potentiation, and this article offers one way of doing so.

#### Twitch potentiation

Post-activation potentiation is a rather broad and macroscopic term; we will prefer to speak in terms of twitch potentiation.
This requires defining a twitch...

Roughly, twitch potentiation is a specific subset of PAP, viewed at the more precise level of muscle fibers and action potentials.

Mechanisms for TP.

#### Functional signficance

And motivation for detecting and measuring TP

"All of these things require a way to reliably detect and quantify TP".

#### Measurement status 

Two-step process: measure muscle response, then detect potentiation from the measured muscle response.

Discuss characteristic parameters.

Discuss SPM.

### Methods

#### Participants

Note number of elite athletes

#### Study design

Describe TMG specs

Coherently describe potentiation protocol

TODO: Protocol figure

> For each subject, the protocol produces a set of pre-exercise measurements and a set of post-exercise measurements.

#### Analysis

Software used---add Python Numpy and SciPy

Data going in to this step data is 4 pre-ISQ and 4 post-ISQ TMG measurements for each athlete

TMG signals is analyzed with SPM and characteristic parameters.

Describe SPM analysis and discrete parameter analysis.

Greater twitch amplitude and faster time to maximal contraction in the post-exercise set is interpreted as post-activation potentiation.

### Results

Fine as is

### Statistics

For TMG twitch contraction parameters for each athlete

For each paramater for each athlete there are two samples:

- set of pre-ISQ parameter values
- set of post-ISQ parameter values

Goal: test if the two samples were drawn from different populations; this is a two-sample t-test for a difference in mean between the samples' populations.

A paired t-test (more generally a paired difference test) is 100 percent appropriate: the same subjects are tested before and after a conditioning exercise.

#### Null hypothesis

See https://github.com/0todd0000/spm1d/issues/163 for what null hypothesis is in context of SPM.

What's involved:
- A sample of a population
- A statistical model of the population

Null hypothesis: pre-conditioning and post-conditioning muscle responses are drawn from the same population.

Hypothesis testing requires constructing a statistical model of what the data would look like if chance or random processes alone were responsible for the results.
The hypothesis that chance alone is responsible for the results is called the null hypothesis.
The model of the result of the random process is called the distribution under the null hypothesis.
The obtained results are compared with the distribution under the null hypothesis, and the likelihood of finding the obtained results is thereby determined.[12]

A test statistic quantifies how far observed data departs from the distribution under the null hypothesis.

Steps in null hypothesis testing:
- Assume distribution for the population from which observed data is drawn
- Compute test statistic for observed data
- Compute threshold value of test statistic for test statistic will assume a larger value than threshold in e.g. 1 percent of data sets in which the null hypothesis holds.

Compare computed test statistic to threshold value; if computed statistic exceeds threshold value reject null hypothesis at significance level e.g. 1 percent.

#### SPM t statistic

The SPM t continuum is just a generalization of a 0D t-statistic associated with 0D datapoints to a 1D t-statistic associated with 1D signals.

SPM t is a 1D test statistic continuum, or a 1D statistical parametric map.

The t statistic has nothing to do with statistical testing by itself;
it is a function of only the pre- and post-conditioning TMG data from which it is produced.

A statistical test is used to quantify the probability that random Gaussian fields would produce a particular feature of the test statistic.

#### SPM inference and the meaning of t-star

t-star by itself has nothing to do with sample data; it is a function of a significance level alpha and of the assumed statistical model for the random data (Gaussian processes for this study.)

In a two-tailed t-test, the threshold t-star associated with a given alpha is the height for which the maximum absolute value of an SPM t-statistic generated by smooth, random (Gaussian) continua would exceed t-star with probability alpha (i.e. in alpha pecent or fewer of many repeated experiments).

[Reference: two-tailed vs. one-tailed](https://spm1d.org/doc/Theory/twotailed.html#label-theory-onetwotailed)

The p value specifies the probability that smooth random fields would produce a suprathreshold cluster as broad or broader than the observed cluster, where “broad” 

The probability (p) value associated with a given supra-threshold cluster indicates the probability that smooth, random Gaussian continua would produce a supra-threshold cluster as broad as the observed cluster,
where broad refers to the width of the supra-threshold cluster relative to the width of the whole SPM t continuum.

From a classical hypothesis testing perspective, the null hypothesis (that pre-conditioning and post-conditioning responses are drawn from the same population) is rejected at alpha if the SPM t-statistic generated from the pre- and post-conditioning muscle responses exceeds t-star.

#### Code to use

- One-tailed inferenced is appropriate for this experiment because of the *a priori* hypothesis that post-conditioning response is larger than pre-conditioning response.

  Two-tailed inference is in general more objective than one-tailed inference, and allows for difference between compared samples to be positive or negative.

- Alpha at 0.1 percent because why not, let's flex.

### Abbreviations

ISQ incline squat
TP  twitch potentiation
PAP post-activation potentiation
TMG tensiomyography
SPM statistical parametric mapping
RF  rectus femoris

### Reference

- [Rise time](https://en.wikipedia.org/wiki/Rise_time)
- [Delay time](https://en.wikipedia.org/wiki/Signal_propagation_delay#Electronics)
- [Settling time](https://en.wikipedia.org/wiki/Settling_time)

- [SPM](http://www.scholarpedia.org/article/Statistical_parametric_mapping)


See e.g. [https://stats.stackexchange.com/questions/354010/why-does-paired-t-test-show-not-significant](https://stats.stackexchange.com/questions/354010/why-does-paired-t-test-show-not-significant)

See `t.py` for where `SPM_T` objects are returned and `_spm.py` for `class SPM_T`


## Meta


### Completed
- Redo protocol plot
- TMG representative plot
- SPM representative plot
- Compute TMG parameter statistics in a given set for 8MPS files
- TMG and SPM analysis code...
  - By subject and set (8mps)
  - By subject across sets (1mps)
  - By set across subjects (1 mps)
