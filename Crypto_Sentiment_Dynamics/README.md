# Congruent or Polarized? Mining Opinion Dynamics towards Cryptocurrency on Twitter
## Abstract
This project examined the opinion polarity and sentiment dynamics toward cryptocurrency using 4.75 million relevant tweets, and revealed that ~73% of the subjective expressions are positive and the sentiment intensity is also stronger for crypto-favoring tweets. In addition, the relevant topics and frequently-mentioned words for the two sentiment classes are different. The positive tweets are talking about general and futuristic terms such as "technology", "mobile", and "millennium", while the negative tweets frequently mention "stop loss", ”bubble“, and "hack", which conveys a sense of pessimistic and insecurity.

## Research Question
1. RQ1: How polarized are people’s opinions towards cryptocurrency? (Overview)
2. RQ2: How does the polarity of cryptocurrency opinions on Twitter evolve over time? (Past)
3. RQ3: Can we effectively predict future opinion dynamics? (Future)

## Data
The raw data is 4.75 million relevant English tweets from Aug 21, 2019 to Nov 31, 2019. All these tweets contain at least one of the following keywords (case insensitive): BTC, bitcoin, crypto, ETH, memecoin. 

## Method
<img width="611" alt="image" src="https://user-images.githubusercontent.com/71967604/172021384-2ee19a60-ec8d-4c68-86e6-1584067df823.png">
See the notebook for more details.

## Findings
1. More positive sentiments toward cryptocurrency on Twitter and the polarity is non-trivial (73% positive vs. 27% negative). 
2. Positive tweets have ~1.5x stronger sentiment intensity than negative tweets.
3. The above sentiment patterns remain valid across the time
4. The relevant topics and frequently-mentioned words for the two sentiment classes are different.
5. Cryptocurrency is a complex topic and comprises of many sub-topics
6. It is difficult to predict future sentiment trends using merely its own historical values (as suggested by ARMA, FB Prophet and the Exponential Smoothing family)
