import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Function to load data based on the selected market option
# st.set_page_config(initial_sidebar_state="auto", theme="light")

def load_data(market_option):
    if market_option == "GASTRO":
        return pd.read_csv("Final_GASTRO.csv")
    elif market_option == "LUPUS":
        return pd.read_csv("Final_LUPUS.csv")

# Function to filter columns based on selected drugs
def filter_columns(df, selected_drugs, common_columns):
    drug_columns = []
    for drug in selected_drugs:
        drug_columns.extend([
            f"{drug}_CONSULTING", f"{drug}_EDUCATION", f"{drug}_FOOD&BEVERAGE",
            f"{drug}_GENERAL", f"{drug}_SPEAKER", f"{drug}_TRAVEL",
            f"{drug}_Claims", f"{drug}_Patients"  # Added columns
        ])
    available_columns = [col for col in common_columns + drug_columns if col in df.columns]
    return df[available_columns]

# Function to generate visualizations based on summed values for selected drugs
def generate_visualizations(df, selected_drugs):
    for drug in selected_drugs:
        # Define possible columns for the drug
        columns = {
            'CONSULTING': f"{drug}_CONSULTING",
            'EDUCATION': f"{drug}_EDUCATION",
            'FOOD&BEVERAGE': f"{drug}_FOOD&BEVERAGE",
            'GENERAL': f"{drug}_GENERAL",
            'SPEAKER': f"{drug}_SPEAKER",
            'TRAVEL': f"{drug}_TRAVEL",
            'CLAIMS': f"{drug}_Claims",
            'PATIENTS': f"{drug}_Patients"  # Added columns
        }
        
        # Filter out columns that do not exist in the DataFrame
        available_columns = {label: col for label, col in columns.items() if col in df.columns}
        
        if available_columns:
            # Display available columns
            st.write(f"Available columns for {drug}:")
            st.write(list(available_columns.values()))
            
            # Calculate totals for available columns
            totals = df[list(available_columns.values())].sum()
            
            # Donut Chart
            fig_pie, ax_pie = plt.subplots(figsize=(10, 8))  # Increase figure size
            wedges, texts = ax_pie.pie(
                totals, labels=None, autopct=None, startangle=140,
                pctdistance=0.85, shadow=True, wedgeprops=dict(width=0.3)
            )
            ax_pie.set_title(f"Distribution of Payments for {drug}")
            
            # Add a legend outside the chart
            ax_pie.legend(wedges, totals.index, title="Payment Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            st.pyplot(fig_pie)
            plt.close(fig_pie)  # Close the figure to avoid overlap
            
            # Bar Graph
            fig_bar, ax_bar = plt.subplots(figsize=(10, 8))  # Increase figure size
            ax_bar.bar(totals.index, totals.values, color='skyblue')
            ax_bar.set_xlabel('Payment Type')
            ax_bar.set_ylabel('Total Amount')
            ax_bar.set_title(f"Total Payments for {drug}")
            ax_bar.tick_params(axis='x', rotation=45)  # Rotate x-axis labels if needed
            st.pyplot(fig_bar)
            plt.close(fig_bar)  # Close the figure to avoid overlap

# Main function to run the Streamlit app
def main():
    # Add logo and video
    st.image("logo.png", width=500)  # Adjust the path and size as needed
    # st.video("E:\Roche Project docs - SASTRA\CMS Data UI\Introduction to YAALI.mp4")  # Adjust the path as needed
    st.link_button("Play Video", "https://drive.google.com/file/d/15T68XeTxSJ68qm0D75wSEj09H7Rdt_tQ/view")

    st.title("CMS - Open Payments Data Explorer")

    market_option = st.selectbox("Select Market Option", ["GASTRO", "LUPUS"])
    df = load_data(market_option)

    drugs = {
        "GASTRO": [
            "SKYRIZI", "ENTYVIO", "STELARA", "INFLECTRA", 
            "HUMIRA", "ZEPOSIA", "SIMPONI", "RENFLEXIS", "REMICADE", "CIMZIA"
        ],
        "LUPUS": [
            "SAPHNELO", "LUPKYNIS", "BENLYSTA"
        ]
    }

    common_columns = [
        'NPI', 'Provider Last Name', 'Provider First Name',
        'Provider Middle Name', 'Provider First Line Business Mailing Address',
        'Provider Second Line Business Mailing Address',
        'Provider Business Mailing Address City Name',
        'Provider Business Mailing Address State Name',
        'Provider Business Mailing Address Postal Code',
        'Primary_Classification', 'Primary_Specialization', 'Definition',
        'Notes', 'Display Name', 'Section', 'Secondary_Classification',
        'Secondary_Specialization', 'Definition.1', 'Notes.1', 'Display Name.1',
        'Section.1'
    ]

    all_drugs_option = "All"
    selected_drugs = st.multiselect(
        "Select Drugs", [all_drugs_option] + drugs[market_option], default=[]  # Default is empty to avoid auto-selecting all
    )

    # Handle "Select All" option
    if all_drugs_option in selected_drugs:
        selected_drugs = drugs[market_option]

    if selected_drugs:
        filtered_df = filter_columns(df, selected_drugs, common_columns)
        st.write(filtered_df)
        generate_visualizations(filtered_df, selected_drugs)

if __name__ == "__main__":
    main()
