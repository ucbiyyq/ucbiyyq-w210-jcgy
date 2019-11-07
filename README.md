# Vizziest - Making **Vis**ualization Ea**siest** for Everyone

Pairing visualization tasks with proper languages, libraries and tools

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

## Data Pipeline

Starting with Stack Overflow [data](https://docs.google.com/spreadsheets/d/1xn4ECk20CwKSk25AcO76Y9frnklSlEfxmWK58LW31bA/edit?usp=sharing), which is large corpus with rick Q&A feature possibilities. The initial audience focus is people with some development skills. Additional data sources to be considered are Stack Exchange Data Science community, Github with developer focused, and Reddit with power user focused.

## Data/Feature Engineering

## Mockup, UI and Backend

## Models

## Model Evaluations

## Testings

## Reference

* Week 14 Presentation 3
* [Week 10 Presentation 2](https://docs.google.com/presentation/d/1M5llKflCqmPuugS7w5dXMTWEy4Q2loXvacZyqIPS7W4/edit#slide=id.g64e6dbcd63_0_0)
* [Week 7 Communication and Storytelling Workshop](https://docs.google.com/presentation/d/1Dc3RShvwhcIsi3HX5cOaITeRkrjx0cbvw5ENN8EJ59k/edit?usp=sharing)
* [Week 5 Presentation 1](https://docs.google.com/presentation/d/1gIKujbJHFY7V9X2ZZIskhfv7tjDtLovV-u2LAL6eI1E/edit#slide=id.p)
* [Week 4 Project Writeup](https://docs.google.com/document/d/1R3Gx72YorSwzzPwlFmFwitgEcGAbYN2VXmzLjm_4NVc/edit?usp=sharing) with [Revised Project Scope](https://drive.google.com/open?id=1rNXevUmSY0ZNaLx80u638e4V4dZk71a66spoaqABluU)
