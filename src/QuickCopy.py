# Required libraries
import pandas as pd          # For Excel file processing
import shutil               # For file copy functions
import os                   # For filesystem operations
from pathlib import Path    # For modern path handling
import sys                  # For system information
import tkinter as tk        # For GUI
from tkinter import filedialog, messagebox, ttk  # Additional GUI components
from tkinter import font

class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Transfer Tool")
        
        # Initialize path variables
        self.excel_path = tk.StringVar()
        self.target_directory = tk.StringVar()
        self.source_directory = tk.StringVar()
        
        # Set default paths
        if sys.platform == "darwin":
            self.source_directory.set(os.path.expanduser("~/Documents"))
        if sys.platform == "win32":
            self.source_directory.set(os.path.expanduser("~/Documents"))
        
        self.create_widgets()
        self.center_window()

    def show_about(self):
        messagebox.showinfo("About", "File Transfer Tool\nVersion 1.0\nOpen Source")
    
    # Placeholder for settings
    def show_preferences(self):
        pass
    
    # Quit the application
    def quit_app(self):
        self.root.quit()

    # Center the window on the screen
    def center_window(self):
        self.root.update_idletasks()
        width = 800  
        height = 600 
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Main frame for all input elements
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Source folder selection
        ttk.Label(input_frame, text="Source Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.source_directory, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.choose_source_folder).grid(row=0, column=2)
        
        # Excel file selection
        ttk.Label(input_frame, text="Excel File:").grid(row=1, column=0, sticky=tk.W, pady=10)
        ttk.Entry(input_frame, textvariable=self.excel_path, width=50).grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(input_frame, text="Browse", command=self.choose_excel).grid(row=1, column=2, pady=10)
        
        # Target folder selection
        ttk.Label(input_frame, text="Target Folder:").grid(row=2, column=0, sticky=tk.W, pady=10)
        ttk.Entry(input_frame, textvariable=self.target_directory, width=50).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(input_frame, text="Browse", command=self.choose_target_folder).grid(row=2, column=2, pady=10)
        
        # Start button
        ttk.Button(input_frame, text="Start", command=self.start_processing).grid(row=3, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(input_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status display
        self.status_label = ttk.Label(input_frame, text="Ready")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Detail view with scrollbar
        self.detail_text = tk.Text(input_frame, height=10, width=50)
        self.detail_text.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.detail_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S))
        self.detail_text.configure(yscrollcommand=scrollbar.set)
        
        # Tutorial button
        self.tutorial_button = ttk.Button(
            input_frame, 
            text="Tutorial", 
            command=self.show_tutorial,
            style='Tutorial.TButton'
        )
        self.tutorial_button.grid(row=7, column=0, sticky=tk.W, pady=10)
        
        # Optional: Custom style for the tutorial button
        style = ttk.Style()
        style.configure('Tutorial.TButton', font=('Helvetica', 8))

    # Dialog to select the Excel file
    def choose_excel(self):
        file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file:
            self.excel_path.set(file)

    # Dialog to select the target folder
    def choose_target_folder(self):
        folder = filedialog.askdirectory(title="Select Target Folder")
        if folder:
            self.target_directory.set(folder)

    # Dialog to select the source folder
    def choose_source_folder(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_directory.set(folder)

    # Start the processing
    def start_processing(self):
        # Check if all required paths are selected
        if not all([self.excel_path.get(), self.target_directory.get(), self.source_directory.get()]):
            messagebox.showerror("Error", "Please select all required folders and the Excel file.")
            return
        
        # Check if the source folder exists
        if not os.path.exists(self.source_directory.get()):
            messagebox.showerror("Error", "Source folder not found.")
            return
        
        self.copy_files()

    # Main function to copy the files
    def copy_files(self):
        try:
            # Read the Excel file and extract catalog numbers
            df = pd.read_excel(self.excel_path.get())
            catalog_numbers = df.iloc[:, 1].astype(str).tolist()  # Column B
            
            # Create target directory if it doesn't exist
            os.makedirs(self.target_directory.get(), exist_ok=True)
            
            found = []
            not_found = []
            total_files = 0
            
            # Count all files to be copied first
            for catalog_number in catalog_numbers:
                files = find_files_recursively(self.source_directory.get(), str(catalog_number))
                total_files += len(files)
            
            self.progress["maximum"] = total_files
            current_progress = 0
            
            # Copy the files and update the progress
            for catalog_number in catalog_numbers:
                found_files = find_files_recursively(self.source_directory.get(), str(catalog_number))
                
                if found_files:
                    for file in found_files:
                        self.status_label["text"] = f"Copying: {file.name}"
                        target_path = Path(self.target_directory.get()) / file.name
                        shutil.copy2(file, target_path)
                        current_progress += 1
                        self.progress["value"] = current_progress
                        self.root.update()
                    found.append(f"{catalog_number} ({len(found_files)} files)")
                else:
                    not_found.append(catalog_number)

            # Create a summary
            short_summary = f"""
Processing completed!

Found catalog numbers: {len(found)}
Total files copied: {total_files}
Not found catalog numbers: {len(not_found)}
"""
            # Show details in the text field
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, "Details of found files:\n")
            for x in found:
                self.detail_text.insert(tk.END, f"- {x}\n")
            
            if not_found:
                self.detail_text.insert(tk.END, "\nNot found catalog numbers:\n")
                for x in not_found:
                    self.detail_text.insert(tk.END, f"- {x}\n")
            
            self.status_label["text"] = "Done!"
            messagebox.showinfo("Summary", short_summary)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_tutorial(self):
        TutorialWindow(self.root)

# Helper function to recursively search directories
def find_files_recursively(base_path, catalog_number):
    """Finds all files that start with the catalog number"""
    found_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.startswith(str(catalog_number)):
                found_files.append(Path(root) / file)
    return found_files

class TutorialWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Welcome to File Transfer Tool")
        self.window.geometry("800x800")
        
        title_font = font.Font(size=12, weight="bold")
        
        # Tutorial steps
        self.steps = [
            {
                "title": "Welcome to File Transfer Tool!",
                "text": "This program helps you automatically find and copy files "
                       "based on catalog numbers from an Excel list."
            },
            {
                "title": "Step 1: Excel File",
                "text": "Select an Excel file that contains the catalog numbers "
                       "in column B that you want to search for."
            },
            {
                "title": "Step 2: Source Folder",
                "text": "Select the folder where the files should be searched. "
                       "The program will automatically search all subfolders."
            },
            {
                "title": "Step 3: Target Folder",
                "text": "Select the folder where the found files should be copied to."
            }
        ]
        
        self.current_step = 0
        
        # GUI elements
        self.frame = ttk.Frame(self.window, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.title_label = ttk.Label(self.frame, font=title_font)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)
        
        self.text_label = ttk.Label(self.frame, wraplength=500, justify=tk.LEFT)
        self.text_label.grid(row=1, column=0, columnspan=3, pady=(0, 40), sticky=tk.W)
        
        # Navigation buttons
        ttk.Button(self.frame, text="Previous", command=self.previous_step).grid(row=2, column=0, padx=5)
        ttk.Button(self.frame, text="Next", command=self.next_step).grid(row=2, column=1, padx=5)
        
        self.show_current_step()
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'+{x}+{y}')
    
    def show_current_step(self):
        step = self.steps[self.current_step]
        self.title_label["text"] = step["title"]
        self.text_label["text"] = step["text"]
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            self.window.destroy()

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()