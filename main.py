import pandas as pd
import csv
from datetime import datetime
from dataEntry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt


class Csv:
    Csv_File = "FinanceData.csv"
    Columns = ["Date", "Amount", "Category", "Description"]
    format = "%d-%m-%Y"
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.Csv_File)
        except FileNotFoundError:
            data_frame = pd.DataFrame(columns = cls.Columns)
            data_frame.to_csv(cls.Csv_File, index = False)
            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date" : date,
            "Amount" : amount,
            "Category" : category,
            "Description" : description,
        }
        with open(cls.Csv_File, mode = "a", newline = "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = cls.Columns)
            writer.writerow(new_entry)
        print("Entry added successfully!")
    
    @classmethod
    def get_transactions(cls,start_date, end_date):
        data_frame = pd.read_csv("FinanceData.csv")
        data_frame["Date"] = pd.to_datetime(data_frame["Date"], format = Csv.format)
        start_date = datetime.strptime(start_date, Csv.format)
        end_date = datetime.strptime(end_date, Csv.format)
        
        mask = (data_frame["Date"] >= start_date) & (data_frame["Date"] <= end_date)
        filter_data_frame = data_frame.loc[mask]    #locate the rows that matches the mask
        
        if filter_data_frame.empty:
            print("No transactions found in the date range.")
        else:
            print(f"Transactions from {start_date.strftime(Csv.format)} to {end_date.strftime(Csv.format)}")
            print(filter_data_frame.to_string(index = False, formatters={"Date": lambda x: x.strftime(Csv.format)}))
        
        total_inc = filter_data_frame[filter_data_frame["Category"] == "Income"]["Amount"].sum()
        total_exp = filter_data_frame[filter_data_frame["Category"] == "Expense"]["Amount"].sum()
        
        print("\nSummary: ")
        print(f"Total Income:  ${total_inc:.2f}")
        print(f"Total Expense:  ${total_exp:.2f}")
        print(f"Net Savings:  ${(total_inc - total_exp):.2f}")
    
        return filter_data_frame
        

def add():
    Csv.initialize_csv()
    date = get_date("Enter the date (DD-MM-YYYY) or 'Enter' for today's date: ", allow_default = True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    Csv.add_entry(date, amount, category, description)
    
def plot_transactions(data_frame):
    if data_frame is None:
        raise ValueError("The data_frame provided is None.")
          
    data_frame.set_index("Date", inplace = True)
    
    inc_data_frame = data_frame[data_frame["Category"] == "Income"].resample("D").sum().reindex(data_frame.index, fill_value = 0)
    exp_data_frame = data_frame[data_frame["Category"] == "Expense"].resample("D").sum().reindex(data_frame.index, fill_value = 0)
    
    plt.figure(figsize=(10,6))
    plt.plot(inc_data_frame.index, inc_data_frame["Amount"], label = "Income", color = "b")
    plt.plot(exp_data_frame.index, exp_data_frame["Amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Tracker")
    plt.legend()
    plt.grid(True)
    plt.show()
    
def main():
    while True:
        print("1. Add a transaction")
        print("2. View transactions and summary in a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (DD-MM-YYYY): ")
            end_date = get_date("Enter the end date (DD-MM-YYYY): ")
            data_frame = Csv.get_transactions(start_date, end_date)
            if input("Do you want to see a plot of the transactions? (y/n): ").lower() == "y":
                plot_transactions(data_frame)
        elif choice == "3":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            
if __name__ == "__main__":
    main()
            

        