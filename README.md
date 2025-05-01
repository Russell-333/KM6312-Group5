**Tweets Analysis on TikTok being banned in the USA**

Objectives: Topic Modelling & Time series analysis & Sentiment Analysis 

**I. Data scrapping**

    Scrap twitter's data using Selenium & ChromeDriver

**II. Data combination**:

    Data deduplication and consolidation

**III. Data cleaning & annotation**

    1. Text preprocessing
    2. Annotate comments using TextBlob and Vader
    
**IV. Topic modelling**

    1. TF-IDF Feature Extraction
    2. NMF Topic Modelling
    3. Top Keywords Identification
    4. Topic Assignment
    5. Topic Visualization

**V. Time series analysis**  

**VI. Model building**

Feature extraction methods:
    1. TF-IDF
    2. Word2Vec embeddings

> Machine Learning Models (TF-IDF)

    * Logistic Regression
    * Support Vector Machine(SVM)
    * XGBoost Classifier

> Deep Learning Models (Word2Vec embeddings)

    * LSTM
    * CNN
    * RNN

**How to Run**

1) Clone the git project & move the dataset "Sentiment_Labelled_Comments.csv" and "Sentiment_Labelled_Comments.xlsx" to the code folder.

2) Install dependency file list </br>
```
pip install -r requirements.txt 
```

**Folder and Files descriptions**

```
code
│   1.Data_Scrapping.py 
|   2.Data_Combination.ipynb
|   3.Text_Annotation.ipynb
|   4.Topic_Modelling.ipynb
|   5.Time_Series.ipynb
|   6.Sentiment_Analysis.ipynb   
│   │ 
└───data
│   └───raw_data    : Scrapped data 
│   │   │   ...
|   └───cleaned_data  : Preprocessed data
|   │   │   ...
└───└───
README.md
requirements.txt
```
