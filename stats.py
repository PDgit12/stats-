import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Data Exploration Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            color: #333333;
            background-color: #FF0000; /* Red background color */
        }
        h1 {
            color: #0066cc;
        }
        .st-bk.st-c3, .st-bm.st-bh, .st-bj.st-bm, .st-bm.st-c1, .st-c7.st-c3 {
            background-color: #e0e0e0;
        }
        .st-c2.st-c3, .st-c2.st-c1, .st-bm.st-c2 {
            color: #333333;
        }
        .st-c3.st-c1 {
            background-color: #f0f2f6;
        }
        .st-bv.st-c1 {
            background-color: #d9d9d9;
        }
        .st-bv.st-c2, .st-bu.st-c2 {
            background-color: #f0f2f6;
        }
        .st-bv.st-c3 {
            background-color: #c0c0c0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Data Exploration Dashboard")
    st.write("Upload a CSV file to get started!")

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded data into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Show summary statistics
        st.header("Summary Statistics")
        st.dataframe(df.describe())

        # Data Visualization
        st.header("Data Visualization")

        # Display a sample of the data
        if st.checkbox("Show Sample Data"):
            num_samples = st.slider("Number of Samples", min_value=1, max_value=len(df), value=10)
            st.dataframe(df.sample(num_samples))

        # Choose columns for plot
        plot_columns = st.multiselect("Select Columns for Plotting", df.columns)

        if len(plot_columns) > 1:  # Ensure at least two columns are selected
            # Choose plot type
            plot_type = st.selectbox("Select Plot Type", ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"])

            if plot_type == "Line Plot":
                st.subheader("Line Plot")
                numeric_columns = [col for col in plot_columns if df[col].dtype in [int, float]]
                if len(numeric_columns) < 2:
                    st.warning("Select at least two numeric columns for the Line Plot.")
                else:
                    st.line_chart(df[numeric_columns])

            elif plot_type == "Bar Plot":
                st.subheader("Bar Plot")
                # Check and filter numeric data for the bar chart
                numeric_columns = [col for col in plot_columns if df[col].dtype in [int, float]]
                if len(numeric_columns) > 0:
                    st.bar_chart(df[numeric_columns])
                else:
                    st.warning("No suitable numeric columns selected for the Bar Plot.")

            elif plot_type == "Scatter Plot":
                st.subheader("Scatter Plot")
                numeric_columns = [col for col in plot_columns if df[col].dtype in [int, float]]
                if len(numeric_columns) < 2:
                    st.warning("Select at least two numeric columns for the Scatter Plot.")
                else:
                    if len(numeric_columns) == 2:
                        # Two numeric columns, create scatter plot
                        fig = plt.figure()
                        plt.scatter(df[numeric_columns[0]], df[numeric_columns[1]])
                        plt.xlabel(numeric_columns[0])
                        plt.ylabel(numeric_columns[1])
                        st.pyplot(fig)
                    else:
                        # More than two numeric columns, create scatter plot matrix
                        fig = pd.plotting.scatter_matrix(df[numeric_columns], alpha=0.7)
                        st.pyplot(fig)

            elif plot_type == "Histogram":
                st.subheader("Histogram")
                numeric_columns = [col for col in plot_columns if df[col].dtype in [int, float]]
                if len(numeric_columns) < 1:
                    st.warning("Select at least one numeric column for the Histogram.")
                else:
                    for col in numeric_columns:
                        st.write(f"**Histogram for '{col}' column:**")
                        fig = plt.figure()
                        plt.hist(df[col], bins='auto')
                        plt.xlabel(col)
                        plt.ylabel("Frequency")
                        st.pyplot(fig)

        else:
            st.warning("Select at least two columns for the Scatter Plot, Bar Plot, Line Plot, or Histogram.")

if __name__ == "__main__":
    main()
