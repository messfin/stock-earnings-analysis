from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys

# Import your existing analysis code
from az import analyze_earnings_impact

class ZMTechApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZMTech Finance - Stock Analysis")
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Configure main window
        window_width = 1000
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create frames
        self.create_input_frame()
        self.create_output_frame()
        
    def create_input_frame(self):
        """Create input section"""
        input_frame = ttk.LabelFrame(self.main_container, text="Analysis Input", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Title
        title_label = ttk.Label(input_frame, text="Stock Analysis", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Stock inputs
        ttk.Label(input_frame, text="Ticker 1:").grid(row=1, column=0, padx=5, pady=5)
        self.ticker1 = ttk.Entry(input_frame, width=15)
        self.ticker1.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Ticker 2:").grid(row=1, column=2, padx=5, pady=5)
        self.ticker2 = ttk.Entry(input_frame, width=15)
        self.ticker2.grid(row=1, column=3, padx=5, pady=5)
        
        # Analysis period
        period_frame = ttk.LabelFrame(input_frame, text="Analysis Period", padding="5")
        period_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)
        
        ttk.Label(period_frame, text="Days Before:").grid(row=0, column=0, padx=5)
        self.days_before = ttk.Entry(period_frame, width=10)
        self.days_before.insert(0, "10")
        self.days_before.grid(row=0, column=1, padx=5)
        
        ttk.Label(period_frame, text="Days After:").grid(row=0, column=2, padx=5)
        self.days_after = ttk.Entry(period_frame, width=10)
        self.days_after.insert(0, "10")
        self.days_after.grid(row=0, column=3, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Run Analysis", 
                  command=self.run_analysis).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_output).grid(row=0, column=1, padx=5)
        
    def create_output_frame(self):
        """Create output section"""
        output_frame = ttk.LabelFrame(self.main_container, text="Analysis Output", padding="10")
        output_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(output_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Output text
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=20)
        self.output_text.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", 
                                command=self.output_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure output frame grid
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        
    def run_analysis(self):
        """Run the stock analysis"""
        try:
            self.status_var.set("Running analysis...")
            self.root.update()
            
            # Get input values
            ticker1 = self.ticker1.get().upper()
            ticker2 = self.ticker2.get().upper()
            days_before = int(self.days_before.get())
            days_after = int(self.days_after.get())
            
            if not ticker1 or not ticker2:
                raise ValueError("Please enter both stock tickers")
            
            # Run analysis using your existing function
            results = analyze_earnings_impact(
                ticker1, 
                ticker2,
                days_before=days_before,
                days_after=days_after
            )
            
            # Display results
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Analysis completed for {ticker1} and {ticker2}\n\n")
            self.output_text.insert(tk.END, "Analysis Results:\n")
            self.output_text.insert(tk.END, str(results))
            
            self.status_var.set("Analysis complete")
            
        except ValueError as ve:
            self.status_var.set("Input error")
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            self.status_var.set("Error in analysis")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def clear_output(self):
        """Clear the output text"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Ready")
            
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    app = ZMTechApp()
    app.run()

if __name__ == "__main__":
    main()