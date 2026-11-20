# Factory-to-Customer Shipping Route Efficiency Analysis

## Nassau Candy Distributor

A Streamlit dashboard for exploring Nassau Candy Distributor's sales and
shipping data, with an experimental machine-learning model that predicts
the recorded order-to-ship lead time.

## Project overview

This project explores shipment patterns across regions, states, and
shipping modes. It combines business-data analysis in a Streamlit
dashboard with an experimental Decision Tree regression model.

-   **Intern:** Arpita Gupta
-   **Role:** Data Science Intern
-   **Program:** Unified Mentor
-   **Project period:** 20 June 2026 -- 20 December 2026

## Live application

[Open the Streamlit
dashboard](https://arpitagupta1-nassau-candy-shipping-route-analysis-app-eghx3s.streamlit.app/)

## Repository contents

  -----------------------------------------------------------------------------
  File                                      Description
  ----------------------------------------- -----------------------------------
  `app.py`                                  Streamlit dashboard application

  `ml_model.py`                             Model training and evaluation
                                            workflow

  `requirements.txt`                        Python package dependencies

  `shipping_lead_time_model.pkl`            Saved Decision Tree model

  `actual_vs_predicted.png`                 Actual-versus-predicted evaluation
                                            plot

  `Nassau Candy Distributor.csv`            Project dataset

  `Arpita_Gupta_Final_Project_Report.pdf`   Final internship project report
  -----------------------------------------------------------------------------

## Dashboard features

-   Business performance overview and key metrics
-   Monthly sales trend
-   Sales analysis by region
-   Shipping-mode analysis
-   Top-product analysis
-   Data-quality review
-   Experimental shipping lead-time prediction

## Tools and technologies

Python, Pandas, NumPy, Streamlit, Matplotlib, Seaborn, Scikit-learn, and
Joblib.

## Run locally

1.  Install Python 3.10 or a compatible version.

2.  Clone the repository:

    ``` bash
    git clone https://github.com/arpitagupta1/Nassau-Candy-Shipping-Route-Analysis.git
    cd Nassau-Candy-Shipping-Route-Analysis
    ```

3.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Start the dashboard:

    ``` bash
    python -m streamlit run app.py
    ```

## Machine-learning evaluation

The project uses a Decision Tree Regressor to estimate the recorded
difference between `Order Date` and `Ship Date`.

  Metric                                  Result
  -------------------------------- -------------
  Training records                         8,155
  Testing records                          2,039
  Mean Absolute Error (MAE)          160.02 days
  Root Mean Squared Error (RMSE)     234.43 days
  R²                                      0.2229
  Baseline mean-model MAE            215.20 days

The Decision Tree performed better than the mean baseline on MAE, but
its predictive performance remains limited.

## Important data limitation

The dataset contains unusually long positive intervals between order and
ship dates:

-   Order Date range: 2 January 2024 -- 31 December 2025
-   Ship Date range: 30 June 2026 -- 28 June 2030
-   Recorded lead-time range: approximately 904--1,642 days

Therefore, the model predicts the **recorded order-to-ship interval in
this dataset**. It should not be interpreted as a validated estimate of
actual customer delivery time or real-world shipping performance. The
model is experimental and results should be interpreted in light of this
data limitation.

## Scope notes

The current application includes the dashboard analyses and experimental
prediction section listed above. A geographic factory route map and a
complete route-efficiency leaderboard are not included in the current
application.

## Author

Arpita Gupta\
Data Science Intern -- Unified Mentor
