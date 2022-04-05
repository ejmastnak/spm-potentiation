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

### Methods
The study measures potentiation in 55 subjects.

Potentiation-like states are activated with the exercise pattern described in TODO.
For each subject, the protocol produces a set of pre-exercise measurements and a set of post-exercise measurements.

Muscle response is measured with TMG.

TMG signals is analyzed with SPM and characteristic parameters.

Greater twitch amplitude and faster time to maximal contraction in the post-exercise set is interpreted as post-activation potentiation.

### Reference
- [Rise time](https://en.wikipedia.org/wiki/Rise_time)
- [Delay time](https://en.wikipedia.org/wiki/Signal_propagation_delay#Electronics)
- [Settling time](https://en.wikipedia.org/wiki/Settling_time)
