import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from matplotlib.ticker import FuncFormatter

# Login Window
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x180")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        self.label_username = ttk.Label(root, text="Username:", background="#f0f0f0", font=("Arial", 10))
        self.label_username.pack(pady=5)
        self.entry_username = ttk.Entry(root, font=("Arial", 10))
        self.entry_username.pack(pady=5)

        self.label_password = ttk.Label(root, text="Password:", background="#f0f0f0", font=("Arial", 10))
        self.label_password.pack(pady=5)
        self.entry_password = ttk.Entry(root, show="*", font=("Arial", 10))
        self.entry_password.pack(pady=5)

        self.login_button = ttk.Button(root, text="Login", command=self.login, style="Accent.TButton")
        self.login_button.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "123":
            self.root.destroy()  # Close login window
            main_app = MainApp()  # Open main application
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Main Application Window
class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sales Data Analytics")
        self.root.geometry("1200x600")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Custom style for buttons
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", font=("Arial", 10), background="#4CAF50", foreground="black")  # Green button with black font
        self.style.configure("Upload.TButton", font=("Arial", 10), background="#2196F3", foreground="black")  # Blue button with black font
        self.style.configure("Predict.TButton", font=("Arial", 10), background="#FF9800", foreground="black")  # Orange button with black font

        # Header
        self.header = ttk.Label(self.root, text="Sales Data Analytics", font=("Arial", 16, "bold"), background="#f0f0f0")
        self.header.pack(pady=10)

        # Left Side: Buttons
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.upload_button = ttk.Button(self.left_frame, text="Upload Sales Data", command=self.upload_data, style="Upload.TButton")
        self.upload_button.pack(pady=10, fill=tk.X)

        self.total_sales_button = ttk.Button(self.left_frame, text="Total Sales per Product", command=self.total_sales_per_product, style="Accent.TButton")
        self.total_sales_button.pack(pady=10, fill=tk.X)

        self.branch_sales_button = ttk.Button(self.left_frame, text="Branch-Wise Sales Distribution", command=self.branch_wise_sales, style="Accent.TButton")
        self.branch_sales_button.pack(pady=10, fill=tk.X)

        self.avg_price_button = ttk.Button(self.left_frame, text="Average Price Analysis", command=self.average_price_analysis, style="Accent.TButton")
        self.avg_price_button.pack(pady=10, fill=tk.X)

        self.predict_sales_button = ttk.Button(self.left_frame, text="Predict Next Week Sales", command=self.predict_sales, style="Predict.TButton")
        self.predict_sales_button.pack(pady=10, fill=tk.X)

        # Right Side: Data Display
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.right_frame, columns=("Date", "Branch Name", "Product Name", "Sold Quantity", "Price Per Unit", "Total Sales Amount"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Branch Name", text="Branch Name")
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Sold Quantity", text="Sold Quantity")
        self.tree.heading("Price Per Unit", text="Price Per Unit")
        self.tree.heading("Total Sales Amount", text="Total Sales Amount")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add alternating row colors
        self.tree.tag_configure("oddrow", background="#f9f9f9")  # Light gray for odd rows
        self.tree.tag_configure("evenrow", background="#ffffff")  # White for even rows

        self.data = None

        self.root.mainloop()

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.data = pd.read_excel(file_path)
                print("Columns in the uploaded file:", self.data.columns.tolist())  # Debugging: Print column names
                self.display_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(self.data.iterrows()):
            if i % 2 == 0:
                self.tree.insert("", tk.END, values=tuple(row[1]), tags=("evenrow",))
            else:
                self.tree.insert("", tk.END, values=tuple(row[1]), tags=("oddrow",))

    def total_sales_per_product(self):
        if self.data is not None:
            try:
                product_sales = self.data.groupby("product name")["total sales amount"].sum().reset_index()
                self.plot_bar_chart(product_sales, "product name", "total sales amount", "Total Sales per Product")
            except KeyError as e:
                messagebox.showerror("Column Error", f"Column not found: {e}. Please check your column names.")
        else:
            messagebox.showwarning("No Data", "Please upload data first.")

    def branch_wise_sales(self):
        if self.data is not None:
            try:
                branch_sales = self.data.groupby("branch name")["total sales amount"].sum().reset_index()
                self.plot_bar_chart(branch_sales, "branch name", "total sales amount", "Branch-Wise Sales Distribution")
            except KeyError as e:
                messagebox.showerror("Column Error", f"Column not found: {e}. Please check your column names.")
        else:
            messagebox.showwarning("No Data", "Please upload data first.")

    def average_price_analysis(self):
        if self.data is not None:
            try:
                avg_price = self.data.groupby("product name")["price per unit"].mean().reset_index()
                self.plot_bar_chart(avg_price, "product name", "price per unit", "Average Price per Product")
            except KeyError as e:
                messagebox.showerror("Column Error", f"Column not found: {e}. Please check your column names.")
        else:
            messagebox.showwarning("No Data", "Please upload data first.")

    def predict_sales(self):
        if self.data is not None:
            try:
                # Convert date column to datetime
                self.data["date"] = pd.to_datetime(self.data["date"])

                # Prepare data for prediction
                predictions = []
                for product in self.data["product name"].unique():
                    product_data = self.data[self.data["product name"] == product]
                    product_data = product_data.groupby("date").agg({
                        "total sales amount": "sum",
                        "sold quantity": "sum"
                    }).reset_index()

                    # Feature engineering: Extract day, month, year
                    product_data["day"] = product_data["date"].dt.day
                    product_data["month"] = product_data["date"].dt.month
                    product_data["year"] = product_data["date"].dt.year

                    # Train a Linear Regression model for sold quantity
                    X = product_data[["day", "month", "year"]]
                    y_quantity = product_data["sold quantity"]
                    model_quantity = LinearRegression()
                    model_quantity.fit(X, y_quantity)

                    # Predict for the next 7 days
                    last_date = product_data["date"].max()
                    future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
                    future_data = pd.DataFrame({
                        "date": future_dates,
                        "day": [d.day for d in future_dates],
                        "month": [d.month for d in future_dates],
                        "year": [d.year for d in future_dates]
                    })
                    future_data["predicted_quantity"] = model_quantity.predict(future_data[["day", "month", "year"]])

                    # Add product name to predictions
                    future_data["product name"] = product
                    predictions.append(future_data[["date", "product name", "predicted_quantity"]])

                # Combine all predictions into one DataFrame
                predictions_df = pd.concat(predictions, ignore_index=True)

                # Aggregate predicted quantities by product
                product_predictions = predictions_df.groupby("product name")["predicted_quantity"].sum().reset_index()

                # Display predictions as a bar chart
                self.plot_bar_chart(product_predictions, "product name", "predicted_quantity", "Predicted Sold Quantity for Next 7 Days")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to predict sales: {e}")
        else:
            messagebox.showwarning("No Data", "Please upload data first.")

    def plot_bar_chart(self, data, x_col, y_col, title):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=x_col, y=y_col, data=data, ax=ax, palette="viridis")
        ax.set_title(title, fontsize=14)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel("Predicted Sold Quantity", fontsize=12)

        # Format y-axis to display integers
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))

        plt.tight_layout()

        # Embed the chart in the Tkinter window
        chart_window = tk.Toplevel(self.root)
        chart_window.title(title)
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the application
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()