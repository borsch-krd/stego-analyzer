#!/usr/bin/env python3
"""
Steganography Analyzer GUI
Tkinter-based GUI for the steganography analyzer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
import sys

# Fix import path for executable
if hasattr(sys, '_MEIPASS'):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from stego_analyzer import StegoAnalyzer
except ImportError:
    # Fallback for when running as standalone
    import importlib.util
    spec = importlib.util.spec_from_file_location("stego_analyzer", 
                                                 os.path.join(os.path.dirname(__file__), "stego_analyzer.py"))
    stego_analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stego_analyzer)
    StegoAnalyzer = stego_analyzer.StegoAnalyzer

class StegoGUI:
    """GUI interface for steganography analyzer"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Steganography Analyzer v1.0")
        self.root.geometry("800x600")
        self.analyzer = StegoAnalyzer()
        self.current_file = None
        self.results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="File to analyze:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state="readonly")
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=1)
        
        # Password field
        ttk.Label(main_frame, text="Password (optional):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Tool selection
        ttk.Label(main_frame, text="Tools:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=5)
        
        tools_frame = ttk.LabelFrame(main_frame, text="Available Tools", padding="5")
        tools_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.tool_vars = {}
        tools = ['zsteg', 'steghide', 'outguess', 'exiftool', 'binwalk', 'foremost', 'strings']
        
        for i, tool in enumerate(tools):
            var = tk.BooleanVar(value=True)
            self.tool_vars[tool] = var
            ttk.Checkbutton(tools_frame, text=tool, variable=var).grid(
                row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2
            )
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.analyze_btn = ttk.Button(button_frame, text="Analyze File", command=self.start_analysis)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Results", command=self.save_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Tools", command=self.check_tools).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="5")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=20)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
    def browse_file(self):
        """Open file dialog to select file for analysis"""
        filename = filedialog.askopenfilename(
            title="Select file to analyze",
            filetypes=[
                ("All files", "*.*"),
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("Audio files", "*.wav *.mp3 *.flac"),
                ("Archive files", "*.zip *.rar *.tar *.gz")
            ]
        )
        if filename:
            self.file_var.set(filename)
            self.current_file = filename
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
    
    def check_tools(self):
        """Check which tools are available"""
        self.status_var.set("Checking tool availability...")
        
        def check_thread():
            available_tools = self.analyzer.check_tool_availability()
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_tool_status(available_tools))
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def update_tool_status(self, available_tools):
        """Update tool status in the UI"""
        message = "Tool Availability Status:\n\n"
        for tool, available in available_tools.items():
            status = "✓ Available" if available else "✗ Not found"
            message += f"{tool}: {status}\n"
        
        messagebox.showinfo("Tool Status", message)
        self.status_var.set("Tool check complete")
    
    def start_analysis(self):
        """Start the analysis in a separate thread"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file to analyze")
            return
        
        if not os.path.exists(self.current_file):
            messagebox.showerror("Error", "Selected file does not exist")
            return
        
        # Disable analyze button and start progress
        self.analyze_btn.config(state="disabled")
        self.progress.start()
        self.status_var.set("Analyzing file...")
        
        # Start analysis in separate thread
        threading.Thread(target=self.run_analysis, daemon=True).start()
    
    def run_analysis(self):
        """Run the actual analysis"""
        try:
            password = self.password_var.get()
            results = self.analyzer.analyze_file(self.current_file, password)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.analysis_complete(results))
            
        except Exception as e:
            self.root.after(0, lambda: self.analysis_error(str(e)))
    
    def analysis_complete(self, results):
        """Handle analysis completion"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        self.results = results
        
        # Display results
        self.display_results(results)
        self.status_var.set("Analysis complete")
    
    def analysis_error(self, error_msg):
        """Handle analysis error"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        messagebox.showerror("Analysis Error", f"An error occurred during analysis:\n{error_msg}")
        self.status_var.set("Analysis failed")
    
    def display_results(self, results):
        """Display analysis results in the text area"""
        self.results_text.delete(1.0, tk.END)
        
        output = f"STEGANOGRAPHY ANALYSIS RESULTS\n"
        output += f"{'='*60}\n\n"
        output += f"File: {results['file_path']}\n"
        output += f"Size: {results['file_size']} bytes\n\n"
        
        for tool_name, tool_results in results["analysis_results"].items():
            output += f"[{tool_name.upper()}]\n"
            output += "-" * 40 + "\n"
            
            if "error" in tool_results:
                output += f"Error: {tool_results['error']}\n\n"
                continue
            
            if not tool_results.get("success", False):
                output += "No results found\n\n"
                continue
            
            # Display tool-specific results
            if tool_name == "zsteg" and tool_results.get("output"):
                output += tool_results["output"] + "\n"
            
            elif tool_name == "steghide":
                if tool_results.get("extracted_content"):
                    output += "Extracted content:\n"
                    content = tool_results["extracted_content"]
                    output += (content[:500] + "..." if len(content) > 500 else content) + "\n"
                else:
                    output += "No hidden content extracted\n"
            
            elif tool_name == "outguess":
                if tool_results.get("extracted_content"):
                    output += "Extracted content:\n"
                    content = tool_results["extracted_content"]
                    output += (content[:500] + "..." if len(content) > 500 else content) + "\n"
                else:
                    output += "No hidden content extracted\n"
            
            elif tool_name == "exiftool":
                metadata = tool_results.get("metadata", {})
                if metadata:
                    for key, value in metadata.items():
                        output += f"{key}: {value}\n"
                else:
                    output += "No metadata found\n"
            
            elif tool_name == "binwalk":
                if tool_results.get("signatures"):
                    output += tool_results["signatures"] + "\n"
                else:
                    output += "No signatures found\n"
            
            elif tool_name == "foremost":
                if tool_results.get("audit"):
                    output += tool_results["audit"] + "\n"
                else:
                    output += "No carved files found\n"
            
            elif tool_name == "strings":
                interesting = tool_results.get("interesting_strings", [])
                total = tool_results.get("total_strings", 0)
                if interesting:
                    output += f"Found {total} strings, showing first 10 interesting ones:\n"
                    for i, string in enumerate(interesting[:10]):
                        output += f"  {i+1}: {string}\n"
                else:
                    output += "No interesting strings found\n"
            
            output += "\n"
        
        self.results_text.insert(1.0, output)
    
    def clear_results(self):
        """Clear the results area"""
        self.results_text.delete(1.0, tk.END)
        self.results = None
        self.status_var.set("Results cleared")
    
    def save_results(self):
        """Save results to a file"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.results, f, indent=2, default=str)
                else:
                    # Save as text
                    content = self.results_text.get(1.0, tk.END)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                messagebox.showinfo("Success", f"Results saved to: {filename}")
                self.status_var.set(f"Results saved to {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results:\n{str(e)}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()
        # Cleanup when GUI closes
        self.analyzer.cleanup()

if __name__ == "__main__":
    app = StegoGUI()
    app.run()
