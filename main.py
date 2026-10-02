import csv 
import os 
from datetime import datetime 
import pandas as pd 

class ExpenseTracker :
    
    def __init__(self , filename ="expenses.csv") :
       self.filename = filename
       self.create_file()
    
    # function to create the data folder and csv file if do not exist
    def create_file(self) :
        
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder) :
            os.makedirs(folder)
            
        if not os.path.exists(self.filename) :
            with open(self.filename , mode = "w" , newline = "" , encoding="utf-8")as file :
                writer = csv.writer(file)
                writer.writerow(["ExpenseID" , "Date" , "Category" ,"Description" , "Amount"])
              
    # function to validate date format YYYY-MM-DD  
    def validate_date(self,date_text) :
        try :
            datetime.strptime(date_text , "%Y-%m-%d")
            return True
        except ValueError :
            return False
        
    # function to generate Expense ID for each data entry
    def get_next_expense_id(self) :
        try :
            with open(self.filename , mode = "r" , newline= "" ,encoding="utf-8") as file :
                reader = list(csv.reader(file))
                if len(reader) <= 1 :
                    return 1
                last_row = reader[-1]
                return int(last_row[0]) +1
        except Exception :
            return 1
     
    # function to add a new expense record to the csv file   
    def add_expense(self) :
        
        try :
            expense_id = self.get_next_expense_id()
        
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date == "" :
                date = datetime.now().strftime("%Y-%m-%d")
            elif not self.validate_date(date) :
                print("Invalid date format ! Use YYYY-MM-DD.") 
                return
            category = input("Enter category : ").strip().title()
            description = input("Enter description : ").strip()
            amount = float(input("Enter amount : $").strip())
        
            if amount <= 0 :
                print("Amount must be greate than 0.")
                return
        
            with open(self.filename , mode="a" , newline="" , encoding = "utf-8") as file :
                writer = csv.writer(file)
                writer.writerow([expense_id , date , category ,description,amount])
            
            print(f"Expense added successfully ! Expense ID = {expense_id}")
        
        except ValueError :
            print("Invalid amount ! Please enter a numeric value.")
        except Exception as e :
            print("Error while adding expense:" , e)
    
    # function to display all expense records in tabular format      
    def view_expenses(self) :
        try:
            with open(self.filename , mode = "r" , newline = "" , encoding = "utf-8") as file :
                reader = list(csv.reader(file))
                
                if len(reader) <= 1 :
                    print("No expense found.")
                    return
                print("\n" + "="*90)
                
                for row in reader[1:]:
                    print("{:<10} {:<12} {:<15} {:30} ${:<10}".format(
                        row[0] , row[1] ,row[2],row[3],row[4]
                ))
        except FileNotFoundError :
            print("Expense file not found.")
        except Exception as e :
            print("Error while viewing expenses:" , e)
    
    # function to search for a single expense using Expense ID
    def search_by_id(self) :
        
        expense_id = input("Enter Expense ID to search: ").strip()
        found = False
        
        try :
            with open(self.filename, mode ="r" , newline="" , encoding="utf-8") as file :
                reader = csv.DictReader(file)
                
                for row in reader :
                    if row["ExpenseID"] == expense_id:
                        print("\nExpense Found")
                        print("-" * 50)
                        print(f"Expense ID : {row['ExpenseID']}")
                        print(f"Date       : {row['Date']}")
                        print(f"Category   : {row['Category']}")
                        print(f"Description : {row['Description']}")
                        print(f"Amount      : ${row['Amount']}")
                        found = True 
                        break 
                
                if not found :
                    print("Expense not found.")
        
        except Exception as e :
            print("Error while searching expense :" , e)
    
    # function to search and display all expenses for a given date
    def search_by_date(self) :
        
        date = input("Enter date to search (YYYY-MM-DD): ").strip()
        
        if not self.validate_date(date) :
            print('Invalid date format!')
            return
        found = False
        
        try :
            with open(self.filename , mode="r" , newline="" , encoding = "utf-8") as file :
                reader = csv.DictReader(file)
                
                print(f"\nExpense on {date}")
                print("=" * 80)
                print("{:<10} {:<12} {:<15} {:<25} ${:<10}".format(
                    "ID" ,"Date" , "Category" ,"Description" ,"Amount"
                ) )       
                print("=" * 80)
                
                for row in reader :
                    if row["Date"] == date :
                        print("{:<10} {:<12} {:<15} {:<25} ${:<10}".format(
                            row["ExpenseID"] , row["Date"] , row["Category"] ,row["Description"] , row["Amount"]
                        ))
                        found = True
                        
                if not found :
                    print("NO expense found for this date.")
        except Exception as e :
            print("Error while searching by date" , e)
    
    #  function to search and display all expense for a given category
    def search_by_category(self) :
        category = input("Enter category to search: ")
        found = False
        
        try :
            with open(self.filename,mode = "r" , newline="" , encoding= "utf-8") as file :
                reader = csv.DictReader(file)
                
                print(f"\nExpense in category : {category.title()}")
                print("="*80)
                print("{:<10} {:<12} {:<15} {:<25} {:<10}".format(
                    "ID" ,"Date" ,"Category" , "Description" ,"Amount"
                ))        
                print("="*80)
                for row in reader :
                    if row["Category"].lower() == category.lower() :
                        print("{:<10} {:<12} {:<15} {:<25} ${:<10}".format(
                            row["ExpenseID"] , row["Date"] , row["Category"] ,
                            row["Description"] , row["Amount"]
                        ))
                        found = True
                if not found :
                    print("NO expense found in this category.")
        except Exception as e :
            print("Error whil searching by category:" , e)
    # function to update an existing expense using Expense ID
    def update_expense(self) :
        expense_id = input("Enter Expense ID to update: ").strip()
        updated_rows = []
        found = False
        
        try :
            with open(self.filename , mode = "r" ,newline="" ,encoding="utf-8") as file :
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader :
                    if row["ExpenseID"] == expense_id:
                        found = True
                        print("\nCurrent Expense Details:")
                        print(row)
                        
                        new_date = input(f"Enter new data [{row['Date']}]: ").strip()
                        if new_date == "":
                            new_date = row["Date"]
                        elif not self.validate_date(new_date) :
                            print("Invalid date format Update cancelled.")
                            return
                        
                        
                        new_category = input(f"Enter new category [{row['Category']}]: ").strip()
                        if new_category == "":
                            new_category = row["Category"]
                        else :
                            new_category = new_category.title()
                            
                        new_description = input(f"Enter new description [{row['Description']}]").strip()
                        if new_description == "":
                            new_description = row["Description"]
                        
                        new_amount = input(f"Enter new amount [{row['Amount']}]")
                        if new_amount == "" :
                            new_amount = row["Amount"]
                        else :
                            try:
                                new_amount = float(new_amount)
                                if new_amount <= 0 :
                                    print("Amount must be greater than 0. Update cancelled")
                                    return 
                            except ValueError :
                                print("Invalid amount ! Update cancelled")
                                return
                        
                        row["Date"] = new_date
                        row["Category"] = new_category
                        row["Description"] = new_description
                        row["Amount"]=new_amount
                    
                    updated_rows.append(row)
                    
            if not found :
                print("Expense ID not found.")
                return
            
            with open(self.filename , mode= "w" , newline="" , encoding="utf-8") as file :
                writer = csv.DictWriter(file,fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)
                
            print('Expense updated successfully!')
            
        except Exception as e :
            print("Error while updating expense :" , e)
    
    # function to delete an expense record using Expense ID.
    def delete_expense(self) :
        expense_id = input("Enter Expense ID to delete: ").strip()
        updated_rows = []
        found = False
        
        try :
            with open(self.filename , mode="r" ,newline="" , encoding="utf-8") as file :
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                
                for row in reader :
                    if row["ExpenseID"] == expense_id:
                        found = True
                        continue
                    updated_rows.append(row)
                    
            if not found :
                print("Expense ID not found.")
                return
            
            with open(self.filename ,mode="w" , newline="",encoding="utf-8") as file :
                writer = csv.DictWriter(file,fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)
                
            print("Expense deleted successfully!")
        
        except Exception as e :
            print("Error while deleting expense :" , e)
    
    # function to calculate and display the total of all expenses.
    def show_total_expense(self) :
        total = 0
        
        try :
            with open(self.filename , mode = "r" , newline="" , encoding="utf-8") as file :
                reader = csv.DictReader(file)
                for row in reader :
                    total += float(row["Amount"])
            
            print(f"\nTotal Expense : ${total:.2f}")
        except Exception as e :
            print("Error while calculating total expense:" ,e)
    
    # function to show category-wise total expense using pandas
    def category_summary(self) :
        try :
            df = pd.read_csv(self.filename)   
            if df.empty :
                print("No expense data available.")
                return
            summary = df.groupby("Category")["Amount"].sum()
            
            print("\nCategory-wise Expense Summary")
            print("="*40)
            print(summary)
            
        except Exception as e :
            print("Error while generating category summary:",e)
     
    # Show month-wise total expense using pandas.       
    def monthly_summary(self) :
        try :
            df = pd.read_csv(self.filename)
            
            if df.empty :
                print("NO expense data available.")
                return
            
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.strftime("%Y-%m")
            
            summary = df.groupby("Month")["Amount"].sum()
            
            print("\nMonthly Expense Summary")
            print("="*40)
            print(summary)
        except Exception as e :
            print("Error while generating monthly summary:" ,e)
    
    # function to show a complete pandas-based expense report        
    def pandas_report(self) :
        try:
            df = pd.read_csv(self.filename)
            
            if df.empty :
                print("No expense data available.")
                return
            
            print("\nFully Expense Data")
            print("="*80)
            print(df)
            
            print("\nTotal Expense")
            print("=" * 40)
            print(f"${df['Amount'].sum():.2f}")
            
            
            
            print("\nCategory-wise Total")
            print("="*40)
            print(df.groupby('Category')["Amount"].sum())
            
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.strftime("%Y-%m")
            
            print("Monthly Total")
            print("=" *40)
            print(df.groupby("Month")["Amount"].sum())
            
            print("\nHighest Expense")
            print("=" * 40)
            max_row = df.loc[df["Amount"].idxmax()]
            print(max_row)
        
        except Exception as e :
            print("Error while generating pandas report:" , e)
            

def main() :
    tracker = ExpenseTracker()
    
    while True :
        print("\n"+"="*40)
        print("      EXPENSE TRACKER - VERSION 2")
        print("="*40)
        print("1. Add Expense ")
        print("2. View All Expenses")
        print("3. Search Expense by ID")
        print("4. Search Expense by Date")
        print("5. Search Expense by Category")
        print("6. Update Expense")
        print("7. Delete Expense")
        print("8. Show Total Expense")
        print("9. Category -wise Summary")
        print("10. Monthly Summary")
        print("11. Pandas Full Report")
        print("12. Exit")
        
        choice = input("Enter your  choice: ").strip()
        
        if choice == "1" :
            tracker.add_expense()
        elif choice == "2" :
            tracker.view_expenses()
        elif choice == "3" :
            tracker.search_by_id()
        elif choice == "4" :
            tracker.search_by_date()
        elif choice == "5" :
            tracker.search_by_category()
        elif choice == "6" :
            tracker.update_expense()
        elif choice == "7" :
            tracker.delete_expense()
        elif choice == "8" :
            tracker.show_total_expense()
        elif choice == "9" :
            tracker.category_summary()
        elif choice == "10" :
            tracker.monthly_summary()           
        elif choice == "11" :
            tracker.pandas_report()
        elif choice == "12" :
            print("Exiting Expense Tracker . Goodbye !")
            break
        else :
            print("Invalid choice ! Please enter a number between 1 and 12.")
21
if __name__ == "__main__" :
    main()                       
            
            
            
            
            
            