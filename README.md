# Cognitive Neuroscience

This repository holds the code used for analysis of an EEG experiment, used for the exam project in Cognitive Neuroscience at Aarhus university.

### Experimental design
The participant is presented with a classification/judgment task in an interference paradigm. For each trial, eight segments of either sentences or image sequences are presented with the last one either being semantically coherent or incoherent with the previous segments. Additionally there is music playing in the background with each segment, which has either a congruent or incongruent chord played on the last segment. The goal is to accurately classify whether the stimulus is coherent or incoherent. Eight types of trials are thus presented:

| Coherency (Stimulus) | Stimulus       | Congruency (Music) |
|----------------------|----------------|---------------------|
| Coherent             | Sentence       | Congruent           |
| Coherent             | Sentence       | Incongruent         |
| Coherent             | Image sequence | Congruent           |
| Coherent             | Image sequence | Incongruent         |
| Incoherent           | Sentence       | Congruent           |
| Incoherent           | Sentence       | Incongruent         |
| Incoherent           | Image sequence | Congruent           |
| Incoherent           | Image sequence | Incongruent         |

### Code overview
| File                               | Purpose                                                           |
| ---------------------------------- | ------------------------------------------------------------------|
| `Time_frequency_analysis.ipynb`                        | Time frequency analysis of EEG signal (cluster-based permutation test and plotting            |
