import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import chardet

# Custom functions
def about_df(df):
    if df.empty or df.shape[1] == 0:
        # Handle the case where the DataFrame is empty or has no columns
        st.warning("The DataFrame is empty or has no columns. No samples can be taken.")
        df_sample = pd.DataFrame()  # Empty DataFrame
        size = (0, 0)
        info = "No information available."
        columns = []
        missing_values = []
        stats = pd.DataFrame()  # Empty DataFrame
    else:
        df_sample = df.sample(min(10, len(df)))
        size = df.shape
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        columns = df.columns.tolist()
        missing_values = df.isnull().sum()
        stats = df.describe()

    return df_sample, size, info, columns, missing_values, stats

def customer_statistics(df):
    if df.empty or df.shape[1] == 0:
        st.warning("The DataFrame is empty or has no columns. Cannot calculate statistics.")
        return {}
    
    # Calculate the relevant statistics
    average_age = df.iloc[:, 1].mean()
    average_tenure = df.iloc[:, 3].mean()
    total_spend = df.iloc[:, 9].sum()
    average_support_calls = df.iloc[:, 5].mean()
    churn_rate = df.iloc[:, 11].mean() * 100
    payment_delay_std_dev = df.iloc[:, 6].std()

    # Create a dictionary to store the statistics
    statistics = {
        'Average Age': average_age,
        'Average Tenure': average_tenure,
        'Total Spend': total_spend,
        'Average Support Calls': average_support_calls,
        'Churn Rate (%)': churn_rate,
        'Payment Delay Std Dev': payment_delay_std_dev
    }

    return statistics

def future_insights(df):
    if df.empty or df.shape[1] == 0:
        st.warning("The DataFrame is empty or has no columns. Cannot generate future insights.")
        return {}

    # Projected insights
    average_monthly_spend = df.iloc[:, 9].mean()
    projected_total_spend_next_year = average_monthly_spend * 12 * len(df)

    churn_rate = df.iloc[:, 11].mean()
    projected_churn_next_year = churn_rate * len(df)

    average_support_calls = df.iloc[:, 5].mean()
    projected_support_calls_increase = average_support_calls * 1.1

    average_payment_delay = df.iloc[:, 6].mean()
    projected_payment_delay_increase = average_payment_delay * 1.05

    standard_and_basic_users = df[(df.iloc[:, 7] == 'Standard') | (df.iloc[:, 7] == 'Basic')]
    projected_upgrades = len(standard_and_basic_users) * 0.15

    average_tenure = df.iloc[:, 3].mean()
    projected_tenure_growth = average_tenure * 1.2

    insights = {
        'Projected Total Spend Next Year': projected_total_spend_next_year,
        'Projected Churn Next Year': projected_churn_next_year,
        'Projected Support Calls Increase': projected_support_calls_increase,
        'Projected Payment Delay Increase': projected_payment_delay_increase,
        'Projected Subscription Upgrades': projected_upgrades,
        'Projected Tenure Growth': projected_tenure_growth
    }

    return insights

def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title('Distribution of Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    return fig

def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Total Spend by Subscription Type')
    ax.set_xlabel('Subscription Type')
    ax.set_ylabel('Average Total Spend')
    return fig

def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    return fig

def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('Contract Length')['Total Spend'].sum().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], ax=ax)
    ax.set_title('Total Spend Distribution by Contract Length')
    ax.set_ylabel('')
    return fig

def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby('Gender')['Churn'].mean() * 100
    churn_rate_by_gender.plot(kind='bar', color='coral', ax=ax)
    ax.set_title('Churn Rate by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Churn Rate (%)')
    return fig

def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df['Gender'] == 'Male']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='blue', label='Male', ax=ax)
    df[df['Gender'] == 'Female']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='red', label='Female', ax=ax)
    ax.set_title('Age Distribution by Gender')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig

# Python main
if __name__ == "__main__":
    st.title("Customer Churn Dashboard😅")
    st.subheader("Data Analysis and Customer Insights")
    st.write("----------------------------------------------------------------------------------------")
    
    st.sidebar.title("Customers Analysis")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type='csv')

    df = pd.DataFrame()

    if uploaded_file is not None:
        try:
            rawdata = uploaded_file.read()
            result = chardet.detect(rawdata)
            charenc = result['encoding']
            df = pd.read_csv(io.StringIO(rawdata.decode(charenc)), encoding=charenc)
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty.")
        except pd.errors.ParserError:
            st.error("Error parsing the uploaded file. Please check the file format.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.sidebar.button("About Dataset"):
        st.subheader("About Dataset")
        df_sample, size, info, columns, missing_values, stats = about_df(df)

        st.subheader('DataFrame Sample:')
        st.write(df_sample)

        st.subheader('DataFrame Size:')
        st.write(size)

        st.subheader('DataFrame Info:')
        st.text(info)

        st.subheader('Column Names and Types:')
        st.write(columns)

        st.subheader('Missing Values:')
        st.write(missing_values)

        st.subheader('Statistics:')
        st.write(stats)

    if st.sidebar.button("Customer Statistics"):
        st.subheader('Customer Statistics:')
        customer_stats = customer_statistics(df)
        for key, value in customer_stats.items():
            st.write(f'{key}: {round(value, 2)}')

    if st.sidebar.button("Future Insights"):
        st.subheader("Future Insights")
        future_stats = future_insights(df)
        for key, value in future_stats.items():
            st.write(f'{key}: {round(value, 2)}')

    if st.sidebar.button("Dashboard"):
        st.subheader("Customer Dashboard")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Age Distribution")
            fig = age_distribution_graph(df)
            st.pyplot(fig)
        with col2:
            st.subheader("Avg Spend Sub Type")
            fig = avg_total_spend_subscription_type(df)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gender Distribution")
            fig = gender_distribution(df)
            st.pyplot(fig)
        with col2:
            st.subheader("T/Spend Contact Length")
            fig = total_spend_distribution_by_contract_length(df)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn Rate By Gender")
            fig = churn_rate_by_gender(df)
            st.pyplot(fig)
        with col2:
            st.subheader("Age Dist By Gender")
            fig = age_distribution_by_gender(df)
            st.pyplot(fig)
