# Vizziest - Making **Vis**ualization Ea**siest** for Everyone

**Pairing visualization tasks with proper languages, libraries and tools**

MIDS W210.6 Fall 2019 Capstone Project Repository - ucbiyyq-w210-jcgy

Team Members: [Jeffrey Braun](mailto:jbraun@ischool.berkeley.edu), [Chi Iong Ansjory](mailto:ansjory@ischool.berkeley.edu), [Yuqing (Grace) Lin](mailto:ylin@ischool.berkeley.edu), [Yang Yang Qian](yangyang.qian@ischool.berkeley.edu)

## Problem Statement

People wanting to create data visualizations are faced with reading through and vetting multiple search results to find the guidance they need to create a visualization that fits their need. While they will eventually find an answer, it takes time and energy.

## Mission Statement

Vizziest takes the time, frustration, and guesswork out of finding actionable guidance for creating the data visualization that best meets the user’s business requirements.

Our hypothesis is that given a problem domain such as visualization, we can create models on top of knowledge repositories to generate more helpful, targeted advice than a user would get from a generalized search engine. Once developed, this approach can generalize to other problem domains, for example, predicting data science models most appropriate for a user's business need.

## Impact

Our earlier [survey](https://www.mysurveygizmo.com/s3/5231057/Creating-Data-Visualizations) of data scientists and business analysts with [results](https://drive.google.com/file/d/1oUGaKxJ1l6I_gCochS7xaTQvEle4b9OJ/view?usp=sharing) indicated that, on average, they create 8.2 data visualizations per month. Assuming they spend 15 minutes per visualization searching for code examples and guidance for each visualization, that means they spend 24.6 hours per year finding answers. The goal of Vizziest is to dramatically reduce this time.

## MVP/Key Features

**User** *enters* general description of desired viz task, optional filters

**Vizziest** *presents* ideas for type of vizs that may accomplish **user**'s goal

**User** *selects* desired type of viz

**Vizziest** *predicts* the question from its knowledge corpus that most closely *matches* **user** requirements

**Vizziest** *examines* the answers associated with the questions, *predicts* and *displays* the best answers based on factors like actionability (instruction steps, sample output, code, pros/cons/cautions, etc.)

**Vizziest** *captures* **user** feedback if **Vizziest** fails to recommend an answer the **user** *likes*

## Overall Architecture

It is a simple and straightforward 3-tier architecture. The top layer is the UX frontend with text input UI taking from user, Recommender with user interaction, and result output UI returning to user. The middle layer is the ML/AI machine with tokenizer/parser to process text input from user and feed the tokens to predictor. The model builder takes the data files post data/feature engineering from bottom layer, interacts with predictor within ML/AI engine and recommender from UI/backend interaction. The bottom layer is data files (badges, post, tag, users) collected from Stack Overflow and processed through the data pipeline.

## Data Pipeline

Starting with Stack Overflow [data](https://docs.google.com/spreadsheets/d/1xn4ECk20CwKSk25AcO76Y9frnklSlEfxmWK58LW31bA/edit?usp=sharing), which is large corpus with rick Q&A feature possibilities. The initial audience focus is people with some development skills. Additional data sources to be considered are Stack Exchange Data Science community, Github with developer focused, and Reddit with power user focused.

Our development and deployment environment is [Google Cloud Platform](https://console.cloud.google.com). GCP commands via [Cloud SDK](https://cloud.google.com/sdk/) for individual instance access are:

```
gcloud projects list
gcloud config set project w210-jcgy-254100
gcloud config list
gcloud compute regions list
gcloud config set compute/zone us-east1-b
gcloud compute ssh --ssh-flag="-L 8896:127.0.0.1:8896" --ssh-flag="-L 6006:127.0.0.1:6006" [yangyq|yqian|jbraun|ansjory|yqlin]@instance-1
conda activate w210
git status
git pull --all
cd /mnt/disks/disk-1-w210-data/data/
jupyter notebook
```

## Data/Feature Engineering

There are two sources to get our data. One is directly download from Stack Overflow website. Those files are XML files and Python scripts were written to get the keys, create dictionaries, and then parse them to CSV files. Given the size of the dataset, we also wrote scripts to split and combine the files to usable format. We also obtained the data from Google BigQuery. Then we [filter](https://docs.google.com/document/d/1FlyOfoKquoQ9H7dW6dW9FXpEt-RV4gE_Vzbdk8LYIKE/edit) data and use parsed tags data to set to only visualization related topics, narrowing them down to around [700k](https://drive.google.com/drive/u/0/folders/10JDNEzLMDvlUYBtTPThrj2Qqz0L7I9ei) questions and then [450k](https://drive.google.com/drive/u/0/folders/1BG3flmbfoqNO_B2wRBvhDamrDLgD1Hgk) questions. We cleaned up and reorganized the question and answer bodies to make them human readable. As the tags in the original questions data are not separated by spaces, we have to use one-hot encoding to get usable tag features. We further extract more features for answers dataset to include author reputation, badges, codes and instruction steps.

## Mockup & UI, Backend Connection

UI mockup tool [Balsamiq](https://balsamiq.com/) is used to design, storyboard, and user-test our frontend UI.

URL domain name [vizziest.info](http://vizziest.info) was acquired from domain.com for 1-year period. Following configurations are required on the GCP VM instance based on this [tutorial](https://stories.mlh.io/launch-your-first-website-with-domain-com-and-google-cloud-platform-b0d72c448b6f):
- Check "Allow HTTP Traffic" under Firewall rule when creating the VM instance
- Redirect port 80 traffic using iptables firewall rule
```
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3000
```
- Connect our domain to Google Cloud DNS
  - Create zone under Network Services with Zone type as "Public", Zone name as "Vizziest", and DNS name as "vizziest.info"
  - Add record set with Resource Record Type as "A", IPv4 Address as "External IP" of VM instance
  - Under domain.com, change Nameserver to the following:
    ```
    ns-cloud-d1.googledomains.com
    ns-cloud-d2.googledomains.com
    ```

Our web server is spawned from same GCP VM instance in data pipeline for easy user (frontend) and prediction (backend) data exchange. Our simple frontend web UI is a free-form style question input and answer output. The data connection from and to backend is through Flask and Jinja interacting with Python code. 

## Models

Latent Dirichlet Allocation ([LDA](https://medium.com/@lettier/how-does-lda-work-ill-explain-using-emoji-108abf40fa7d)), a topic modeling technique in NLP, is attempted during the initial EDA and expected to obtain fuzzy cluster membership recommendation. When we apply this technique on our viz post question dataset, we expect to identify top 10 to 50 "topics" based on LDA and try to extrapolate relationship between "topics" and chart types. However, we fail to associate each "topic" to a unique chart type selection.

Then we look into Term Frequency - Inverse Document Frequency (TF-IDF), a vector space model for cosine similarity, for question recommendation, with variation of Unigram, Bigram, and Word2vec. We would use the total number of documents in the corpus divided by the number of documents where the term appears. Then we use cosine similarity to calculate the distance between different documents and output the top questions with the highest similarity scores.

Then we will use Logistic Regression for answer recommendation based on features like comment counts, author reputation, and view counts. The numerator is total number of documents in the corpus and denominator is number of documents where the term appears. The set of documents in a collection then is viewed as a set of vectors in a vector space to find similarity between two documents.

We are also looking at the potential application of BERT model with [similarity measure](https://medium.com/the-artificial-impostor/news-topic-similarity-measure-using-pretrained-bert-model-1dbfe6a66f1d), [text classification](https://medium.com/swlh/a-simple-guide-on-using-bert-for-text-classification-bbf041ac8d04), and SQuAD approach.

## Model Evaluations

One major challenge that we face for all our models is the fact the we do not havea labeled data as "ground truth". Thus, we must rely on subjective evaluations to determine the effectiveness of our models. The [survey](https://forms.gle/BAvATVBemGCwXCmB6) incorporated models of TF-IDF, Unigram, Bigram and Word2vec is for respondents to choose the most similar questions so as to evaluate recommendation systems.

For this project, we limited our knowledge base to visualization-related question and answer posts in Stack Overflow. To evaluate our model, we will ask potential users to enter sample questions into Vizziest and into Stack Overflow's native search bar. The users will be asked to rank the userfulness of the top answers provided by Vizziest compared to the top answers provided by Stack Overflow.

## Testings

We asked 105 testers to identify the question most similar to questions in a test suite. To choose from, the testers were given questions recommended by our TF-IDF bigram, TF-IDF unigram, and word2vec models, as well as the top answer returned by Stack Overflow's search bar. The TF-IDF unigram model results were rated most highly by the testers, and well above the results from Stack Overflow's search bar. We will perform similar tests once we have results from a BERT model.

## Additional Resources

* [Week 14 Presentation 3](https://docs.google.com/presentation/d/15oKzgl3USPItpqjKc6EadOLzsUdqpHfu3xeozCo-XxA/edit#slide=id.g7a70253d8d_0_18)
* [Week 10 Presentation 2](https://docs.google.com/presentation/d/1M5llKflCqmPuugS7w5dXMTWEy4Q2loXvacZyqIPS7W4/edit#slide=id.g64e6dbcd63_0_0)
* [Week 7 Communication and Storytelling Workshop](https://docs.google.com/presentation/d/1Dc3RShvwhcIsi3HX5cOaITeRkrjx0cbvw5ENN8EJ59k/edit?usp=sharing)
* [Week 5 Presentation 1](https://docs.google.com/presentation/d/1gIKujbJHFY7V9X2ZZIskhfv7tjDtLovV-u2LAL6eI1E/edit#slide=id.p)
* [Week 4 Project Writeup](https://docs.google.com/document/d/1R3Gx72YorSwzzPwlFmFwitgEcGAbYN2VXmzLjm_4NVc/edit?usp=sharing) with [Revised Project Scope](https://drive.google.com/open?id=1rNXevUmSY0ZNaLx80u638e4V4dZk71a66spoaqABluU)
* [Vizziest Task List Sheet](https://docs.google.com/spreadsheets/d/1sDwbgM8OFQyg-vm2y0Fxh65E7CKBu4WI5oaMcItEZuA/edit?usp=sharing)
* [Initial Task List Sheet and Feedback List](https://docs.google.com/spreadsheets/d/19ff4Nb30oHjf4JloauIVDLaRFCyLj3CD4S25JKwEFF0/edit#gid=0)
