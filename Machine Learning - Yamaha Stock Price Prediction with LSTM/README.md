# Yamaha Stock Price Prediction with LSTM

Machine Learning project focused on **time series forecasting of stock prices** using a **Long Short-Term Memory (LSTM) neural network**.

The goal of this project is to analyze historical financial data and build a model capable of predicting future closing prices of **Yamaha Corporation stock**.

This project demonstrates the use of **deep learning for financial time-series prediction**, including data preprocessing, feature engineering, model training, and evaluation.

---

# Project Overview

Financial markets produce large volumes of sequential data. Traditional machine learning models often struggle with temporal dependencies, which makes **recurrent neural networks (RNNs)** — especially **LSTM models** — well suited for this task.

In this project:

* historical stock market data is collected and prepared
* multiple financial indicators are merged into a single dataset
* correlations between variables are analyzed
* an **LSTM neural network** is trained to predict stock closing prices
* predictions are compared with real market data

---

# Dataset

The project uses historical daily stock data for **Yamaha Corporation**, including:

* Open price
* Close price
* High price
* Low price
* Trading volume

Additional explanatory variables were included from market indices to improve model performance.

Data sources include:

* **Stooq**
* historical financial datasets

The dataset spans approximately **2010 – 2021**.

---

# Machine Learning Model

The prediction model is based on a **Long Short-Term Memory (LSTM)** neural network.

LSTM networks are designed to learn patterns in **sequential data** and are commonly used in:

* stock price prediction
* financial forecasting
* speech recognition
* natural language processing

### Model architecture

The implemented architecture includes:

* **LSTM layer (20 neurons)**
* **Dropout layer** (to reduce overfitting)
* **Dense output layer**

The model is trained to predict the **next closing price based on previous observations**.

---

# Technologies Used

**Programming language**

* Python

**Libraries**

* pandas
* numpy
* matplotlib
* seaborn
* tensorflow / keras
* scikit-learn

**Development environment**

* Jupyter Notebook

---

# Data Analysis

Before training the model, several steps were performed:

### Data preprocessing

* merging multiple financial datasets
* handling missing values
* formatting time-series data
* dataset normalization

### Correlation analysis

Correlation heatmaps were generated to understand relationships between:

* stock prices
* financial indices
* derived indicators

Strong correlations were observed between variables representing the same market index (Open, Close, High, Low).

---

# Model Training

The dataset was split into:

* **training set**
* **validation set**
* **test set**

A sliding window approach was used:

```
look_back = 20
```

This means the model uses **20 previous observations** to predict the next value.

The network was trained for multiple epochs while monitoring:

* training loss
* validation loss

---

# Results

The trained model successfully captures the **general trend of the stock price**.

Observations:

* predictions follow the overall market direction
* the model produces smoother curves than real data
* sharp spikes and drops are harder to predict

This behavior is typical for **LSTM forecasting models applied to financial time series**.

---

# Visualization

The project includes visual comparisons between:

* **actual stock prices**
* **model predictions**

Blue line → real market values
Red line → predicted values

These plots help visually evaluate prediction quality.

---

# Hyperparameter Testing

Additional experiments were conducted to explore the impact of:

* look-back window size
* model architecture
* training parameters

Model performance can be evaluated using metrics such as:

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² score

---

# Key Learnings

This project demonstrates:

* working with **financial time series data**
* data preprocessing for machine learning
* implementing **LSTM neural networks**
* evaluating deep learning models
* visualizing prediction performance

---

Project created as part of a **machine learning study project** focused on financial data analysis and time-series prediction.

