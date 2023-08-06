Package **PairedCompCalc** implements probabilistic Bayesian analysis
of Paired-Comparison data collected from psycho-physical experiments.
Paired comparisons are used, for example,
to evaluate the subjective sound quality of two or more different hearing aids
or any other quality aspects of any multimedia presentations.

The analysis model estimates quality parameters numerically on an objective *interval scale*,
although the raw input data are *subjective*
and indicate only an *ordinal* judgment for each presented pair.

## Paired-comparison Experiments
In a paired-comparison test procedure, each presentation includes exactly two test items,
and the test participant indicates a binary or graded judgment
about which of the two items is better in terms of the *perceptual attribute*
being investigated.
The perceptual attribute might be, for example, *speech clarity*, *sound quality*,
or whatever is specified by the instructions to participants.
The paired-comparison procedure can be applied
even if the difference between tested objects is very subtle,
even so small that the difference is just barely notieable.

Data can be collected either in controlled *laboratory sessions*,
or by *Ecological Momentary Assessment (EMA)*, where each subject
evaluates the tested objects, e.g., hearing-aid programs,
while using them normally in real life.

This package does *not* include functions to administer the actual experiment;
it can only use existing results from an earlier experiment.
The package can analyse data from simple or quite complex experimental designs,
including the following features:

1. The experiment must include two or more **Test Objects** (A, B, C, etc.).
    The analysis results will show quality parameters for all objects,
    but the first object will always be used as a reference with quality = 0,
    because the zero point on the scale is arbitrary.

1. One or more distinct **Participant Groups** may be included.
    The analysis will show systematic differences between groups.

1. One or more **Perceptual Attributes** may be evaluated.
    The analysis will show correlations between different attributes.

1. Response data may be collected in one or more distinct **Test Conditions**.
    Each test condition may be a combination of categories from one or more *Test Factors*.
    For example, one test factor may be *Stimulus Type*,
    with categories *Speech*, or *Music*.
    Another test factor may be, e.g.,
    *Background*, with categories *Quiet*, or *Weak Noise*, or *Loud Noise*.
    The analysis will show quality differences between categories within each test factor.

1. The subjects' **Responses** may be either *binary*, e.g.,
    *B better than A*, or include an *ordinal grading* of the perceived difference, e.g.,
    *no difference*, *slightly better*, or *much better*.

1. The analysis model does not require anything about the number of
    replicated judgments for each pair, and the numbers may differ among subjects.
    Of course, the reliability is improved if there are
    many test participants, each giving many judgments
    for each pair of objects.
    The analysis estimates the *statistical credibility*
    of any observed quality differences,
    given the amount of collected data.
    The analysis also performs an approximate Likelihood-Ratio test for
    any significant differences among objects in the population
    from which the test participants were recruited.


The Bayesian model is hierarchical.
The package can estimate predictive distributions of results for
* a random individual in the group of test participants,
* a random individual in the population from which the participants were recruited,
* the mean quality parameters in the population.

## Package Documentation
General information and version history is given in the package doc-string that may be accessed by command
`help(PairedCompCalc)`.

Specific information about the organisation and accepted formats of input data files
is presented in the doc-string of module pc_data, accessible via `help(PairedCompCalc.pc_data)`.
The most flexible file format is Excel (xlsx), where each work-sheet row
contains data for one presentation and response.

After running an analysis, the logging output briefly explains
the analysis results presented in figures and tables.

## Usage
1. Install the most recent package version:
    `python3 -m pip install --upgrade PairedCompCalc`

1. Copy the template script `run_pc.py`, rename it, and
    edit the copy as suggested in the template, to specify
    - your experimental layout,
    - the top input data directory,
    - a directory where all output result files will be stored.

1. Run your edited script: `python3 run_my_pc.py`.

1. When planning an experiment, the statistical power can be crudely predicted,
    to estimate the number of test participants needed to get a desired statistical strength.
    Copy, edit, and run the script template `run_plan.py`

1. In the planning phase, complete analysis results may also be calculated
    for synthetic data generated from simulated experiments.
    Simulated experiments allow the same design variants as real experiments.
    Copy, edit, and run the script template `run_sim.py`.

## Requirements
This package requires Python 3.6 or newer, with Numpy, Scipy, and Matplotlib,
as well as a support package samppy, and openpyxl for reading xlsx files.
The pip installer will check and install the required packages if needed.

## References
A. Leijon, M. Dahlquist, and K. Smeds (2019).
Bayesian analysis of paired-comparison sound quality ratings.
*Manuscript in preparation*.

K. Smeds, F. Wolters, J. Larsson, P. Herrlin, and M. Dahlquist (2018).
Ecological momentary assessments for evaluation of hearing-aid preference.
*J Acoust Soc Amer* 143(3):1742–1742. [download](https://asa.scitation.org/doi/10.1121/1.5035685)

M. Dahlquist and A. Leijon (2003).
Paired-comparison rating of sound quality using MAP parameter estimation for data analysis.
In *First ISCA Tutorial and Research Workshop on Auditory Quality of Systems*,
Mont-Cenis, Germany. [download](https://www.isca-speech.org/archive_open/aqs2003/aqs3_079.html)

This Python package is a re-implementation and generalization of a similar MatLab package,
developed by Arne Leijon for *ORCA Europe, Widex A/S, Stockholm, Sweden*.
The MatLab development was financially supported by *Widex A/S, Denmark*.

