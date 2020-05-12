# EmoNet

## Audio-only Emotion Detection using Federated Learning

Contributors: Adar Arnon and John Keck

## Proposal

- <https://docs.google.com/presentation/d/1_KhNUIATO6hUClqAUfZ_jjpc9R3Ij_ds4bHnsRWE4tg/edit?usp=sharing>

## Work Documentation

- EmoNet is a federated learning system for emotion detection using audio features (MFCCs). The system consists of a server and a client, the server acting as a centralized source-of-truth for the most recently updated model and the client acting as a public-facing webpage for any user to run an inference or submit for model improvement. The system allows for boostrapping an audio-only model with user-provided, self-labeled data.

EmoNet is hosted on Google Cloud Platform and can be accessed at https://emonet.xyz.

- [EmoNet Server](https://github.com/robertjkeck2/EmoNet/blob/master/server/README.md)
- [EmoNet Client](https://github.com/robertjkeck2/EmoNet/blob/master/client/README.md)
- [Colab Notebook](https://colab.research.google.com/drive/1AgWEyEiKl-YAieNpqscEeUpXSH_77I8i?authuser=0)

## Datasets

- [RAVDESS](https://github.com/robertjkeck2/EmoNet/tree/master/data/RAVDESS)
- [SAVEE](https://github.com/robertjkeck2/EmoNet/tree/master/data/SAVEE)

## References

- <https://arxiv.org/pdf/1503.02531.pdf>
- <https://arxiv.org/ftp/arxiv/papers/1802/1802.06209.pdf>
- <https://personal.utdallas.edu/~john.hansen/Publications/CP-ICASSP13-KaushikSangwanHansen-Sentiment-0008485.pdf>
- <https://github.com/shaharpit809/Audio-Sentiment-Analysis>
- <https://arxiv.org/pdf/1904.08138v1.pdf>
- <https://zenodo.org/record/1188976>
- <https://github.com/MITESHPUTHRANNEU/Speech-Emotion-Analyzer>
- <https://github.com/tyiannak/pyAudioAnalysis>
- <https://github.com/pyannote/pyannote-audio>
- <http://kahlan.eps.surrey.ac.uk/savee/Database.html>
- <https://github.com/laugustyniak/awesome-sentiment-analysis>
- <http://www.robots.ox.ac.uk/~vgg/research/cross-modal-emotions/>
- <http://www.robots.ox.ac.uk/~vgg/demo/theconversation/>
- <https://sentic.net/benchmarking-multimodal-sentiment-analysis.pdf>
- <https://github.com/PiotrSobczak/speech-emotion-recognition>
- <https://sail.usc.edu/iemocap/>
- <http://immortal.multicomp.cs.cmu.edu/raw_datasets/processed_data/>
- https://en.wikipedia.org/wiki/Mel-frequency_cepstrum

## Citations

- Livingstone SR, Russo FA (2018) The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal expressions in North American English. PLoS ONE 13(5): e0196391. https://doi.org/10.1371/journal.pone.0196391.
- S. Haq and P.J.B. Jackson, "Multimodal Emotion Recognition", In W. Wang (ed), Machine Audition: Principles, Algorithms and Systems, IGI Global Press, ISBN 978-1615209194, chapter 17, pp. 398-423, 2010.
- S. Haq and P.J.B. Jackson. "Speaker-Dependent Audio-Visual Emotion Recognition", In Proc. Int'l Conf. on Auditory-Visual Speech Processing, pages 53-58, 2009.
- S. Haq, P.J.B. Jackson, and J.D. Edge. Audio-Visual Feature Selection and Reduction for Emotion Classification. In Proc. Int'l Conf. on Auditory-Visual Speech Processing, pages 185-190, 2008
- C. Busso, M. Bulut, C.C. Lee, A. Kazemzadeh, E. Mower, S. Kim, J.N. Chang, S. Lee, and S.S. Narayanan, "IEMOCAP: Interactive emotional dyadic motion capture database," Journal of Language Resources and Evaluation, vol. 42, no. 4, pp. 335-359, December 2008.
