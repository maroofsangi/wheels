import tkinter as tk
from tkinter import ttk, messagebox
import unittest
import re

# --- Data Model ---
class Vehicle:
    def __init__(self, model, year, price, battery, range_km, top_speed, condition):
        self.model = model
        self.year = year
        self.price = price
        self.battery = battery
        self.range_km = range_km
        self.top_speed = top_speed
        self.condition = condition
        

    def get_details(self):
        return (
            f"Model: {self.model}\n"
            f"Year: {self.year}\n"
            f"Price: ${self.price:,.2f}\n"
            f"Battery: {self.battery} kWh\n"
            f"Range: {self.range_km} km\n"
            f"Top Speed: {self.top_speed} km/h\n"
            f"Condition: {self.condition}\n"
        )

class Inventory:
    def __init__(self):
        self.vehicles = []
        self.load_vehicles()

    def load_vehicles(self):
        data = [
            ("Model S Plaid", 2024, 89990, 100, 637, 322, "New"),
            ("Model 3 Standard", 2023, 39990, 57, 438, 225, "New"),
            ("Model X Long", 2022, 79990, 100, 560, 250, "Used"),
            ("Model Y", 2023, 47490, 75, 533, 217, "New"),
            ("Model 3 Performance", 2021, 45000, 75, 499, 261, "Used"),
            ("Model S (Basic)", 2020, 59000, 75, 505, 250, "Used"),
            ("Roadster", 2025, 200000, 200, 1000, 400, "New"),
            ("Cybertruck RWD", 2024, 49890, 100, 547, 180, "New"),
            ("Cybertruck AWD", 2024, 69900, 123, 610, 210, "New"),
            ("Model X Plaid", 2023, 94990, 100, 536, 262, "New")
        ]
        for d in data:
            self.vehicles.append(Vehicle(*d))

    def get_all(self):
        return self.vehicles

    def search_by_model(self, keyword):
        """Secure search with input sanitization"""
        if not self.is_valid_search_input(keyword):
            return []
        keyword = keyword.lower()
        return [v for v in self.vehicles if keyword in v.model.lower()]

    @staticmethod
    def is_valid_search_input(input_str):
        """Validate search input to prevent injection attacks"""
        if len(input_str) > 100:
            return False
        return bool(re.match(r'^[a-zA-Z0-9\s\-_]*$', input_str))

# --- GUI App ---
class VoltWheelsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoltWheels Tesla Dealership")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0f1c2e")
        self.inventory = Inventory()
        self.current_vehicle = None
        self.selected_image = None
        
        # Set application icon
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configure styles
        self.configure_styles()
        self.create_widgets()
        self.display_all_vehicles()

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#0f1c2e"
        self.card_bg = "#1f3a5c"
        self.accent_color = "#4fc3f7"
        self.text_color = "#e6f7ff"
        self.button_color = "#0288d1"
        
        # Style configurations
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        self.style.configure("Title.TLabel", font=("Arial", 24, "bold"), foreground=self.accent_color)
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Detail.TLabel", font=("Arial", 10))
        
        self.style.configure("TButton", font=("Arial", 10, "bold"), 
                            background=self.button_color, foreground="white",
                            borderwidth=1, relief="raised", padding=6)
        self.style.map("TButton", 
                      background=[("active", "#039be5"), ("pressed", "#0277bd")],
                      foreground=[("active", "white")])
        
        self.style.configure("Treeview", background=self.card_bg, fieldbackground=self.card_bg, 
                            foreground=self.text_color, rowheight=25)
        self.style.configure("Treeview.Heading", background="#2e4a76", foreground="white", 
                            font=("Arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#3d5a80")])
        
        self.style.configure("TLabelframe", background=self.bg_color, foreground=self.accent_color)
        self.style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.accent_color)

    def create_widgets(self):
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header Frame
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="⚡ VOLTWHEELS TESLA DEALERSHIP", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Add slogan
        slogan_label = ttk.Label(header_frame, text="Premium Electric Vehicles", 
                                font=("Arial", 12, "italic"), foreground=self.accent_color)
        slogan_label.pack(side=tk.RIGHT, padx=10)
        
        # Search Frame
        search_frame = ttk.LabelFrame(main_container, text="Find Your Tesla")
        search_frame.pack(fill=tk.X, pady=10)
        
        search_container = ttk.Frame(search_frame)
        search_container.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_container, text="Search by Model:", style="Header.TLabel").grid(row=0, column=0, padx=5)
        
        self.search_entry = ttk.Entry(search_container, width=30, font=("Arial", 10))
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_vehicles())
        
        ttk.Button(search_container, text="Search", command=self.search_vehicles).grid(row=0, column=2, padx=5)
        ttk.Button(search_container, text="Clear", command=self.clear_search).grid(row=0, column=3, padx=5)
        ttk.Button(search_container, text="Show All", command=self.display_all_vehicles).grid(row=0, column=4, padx=5)
        
        # Main Content Frame
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Vehicle List Frame
        list_frame = ttk.LabelFrame(content_frame, text="Available Vehicles")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("model", "year", "price", "condition")
        self.vehicle_list = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                        selectmode="browse", yscrollcommand=tree_scroll.set,
                                        height=15)
        tree_scroll.config(command=self.vehicle_list.yview)
        
        # Configure columns
        self.vehicle_list.heading("model", text="Model", command=lambda: self.sort_column("model", False))
        self.vehicle_list.heading("year", text="Year", command=lambda: self.sort_column("year", False))
        self.vehicle_list.heading("price", text="Price", command=lambda: self.sort_column("price", False))
        self.vehicle_list.heading("condition", text="Condition", command=lambda: self.sort_column("condition", False))
        
        self.vehicle_list.column("model", width=200)
        self.vehicle_list.column("year", width=80, anchor=tk.CENTER)
        self.vehicle_list.column("price", width=120, anchor=tk.CENTER)
        self.vehicle_list.column("condition", width=100, anchor=tk.CENTER)
        
        self.vehicle_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.vehicle_list.bind("<<TreeviewSelect>>", self.on_vehicle_select)
        
        # Details Frame
        detail_frame = ttk.LabelFrame(content_frame, text="Vehicle Details")
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Image display
        self.image_container = ttk.Frame(detail_frame)
        self.image_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = ttk.Label(self.image_container, background="black")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Details text
        detail_container = ttk.Frame(detail_frame)
        detail_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.detail_text = tk.Text(detail_container, wrap=tk.WORD, height=8, width=40, 
                                 font=("Arial", 10), bg=self.card_bg, fg=self.text_color,
                                 bd=0, highlightthickness=0, padx=10, pady=10)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        self.detail_text.config(state=tk.DISABLED)
        
        # Buttons Frame
        button_frame = ttk.Frame(detail_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Schedule Test Drive", 
                  command=self.schedule_test_drive).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="Contact Sales", 
                  command=self.contact_sales).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Footer
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        footer_text = (
            "📍 123 Innovation Drive, Tech City | "
            "☎️ (555) 123-4567 | "
            "📧 info@voltwheels.com | "
            "🌐 www.voltwheels.com"
        )
        ttk.Label(footer_frame, text=footer_text, font=("Arial", 9), 
                 foreground=self.accent_color).pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W,
                                   background="#2e4a76", foreground="white")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready | Vehicles loaded: {}".format(len(self.inventory.get_all())))

    def display_all_vehicles(self):
        self.clear_list()
        vehicles = self.inventory.get_all()
        for v in vehicles:
            self.vehicle_list.insert("", tk.END, values=(
                v.model, v.year, f"${v.price:,.2f}", v.condition
            ))
        self.search_entry.delete(0, tk.END)
        self.status_var.set(f"Showing all vehicles: {len(vehicles)} available")

    def search_vehicles(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("Search", "Please enter a model name to search.")
            return
            
        if not self.inventory.is_valid_search_input(keyword):
            messagebox.showwarning("Invalid Input", 
                                  "Search input contains invalid characters or is too long.\n"
                                  "Please use only letters, numbers, spaces, hyphens, and underscores.")
            return

        results = self.inventory.search_by_model(keyword)
        self.clear_list()
        
        if results:
            for v in results:
                self.vehicle_list.insert("", tk.END, values=(
                    v.model, v.year, f"${v.price:,.2f}", v.condition
                ))
            self.status_var.set(f"Search results: {len(results)} vehicles found for '{keyword}'")
        else:
            self.status_var.set(f"No vehicles found for '{keyword}'")
            messagebox.showinfo("Search Results", "No vehicles matched your search.")

    def clear_list(self):
        for item in self.vehicle_list.get_children():
            self.vehicle_list.delete(item)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.display_all_vehicles()

    def sort_column(self, col, reverse):
        data = [(self.vehicle_list.set(item, col), item) for item in self.vehicle_list.get_children("")]
        
        # Convert to appropriate types for sorting
        if col == "year" or col == "price":
            # Extract numbers from strings
            data = [(float(val.replace('$', '').replace(',', '')) if col == "price" else int(val), item) 
                    for val, item in data]
        else:
            data = [(val.lower(), item) for val, item in data]
        
        data.sort(reverse=reverse)
        
        for index, (_, item) in enumerate(data):
            self.vehicle_list.move(item, "", index)
        
        self.vehicle_list.heading(col, command=lambda: self.sort_column(col, not reverse))

    def on_vehicle_select(self, event):
        selected_item = self.vehicle_list.focus()
        if not selected_item:
            return
            
        model = self.vehicle_list.item(selected_item)["values"][0]
        vehicle = next((v for v in self.inventory.get_all() if v.model == model), None)
        
        if vehicle:
            self.current_vehicle = vehicle
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, vehicle.get_details())
            self.detail_text.config(state=tk.DISABLED)
            

    def schedule_test_drive(self):
        if not self.current_vehicle:
            messagebox.showinfo("Test Drive", "Please select a vehicle first.")
            return
            
        messagebox.showinfo("Schedule Test Drive", 
                          f"Test drive scheduled for:\n\n{self.current_vehicle.model}\n\n"
                          "Our sales team will contact you shortly to confirm your appointment!")

    def contact_sales(self):
        messagebox.showinfo("Contact Sales", 
                          "Our sales team is ready to assist you!\n\n"
                          "☎️ Call: (555) 123-4567\n"
                          "📧 Email: sales@voltwheels.com\n"
                          "📍 Visit: 123 Innovation Drive, Tech City\n\n"
                          "Business Hours:\nMon-Fri: 9:00 AM - 6:00 PM\nSat: 10:00 AM - 4:00 PM")


# --- Unit Tests ---
class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
    
    def test_inventory_loading(self):
        """Test that inventory loads correct number of vehicles"""
        vehicles = self.inventory.get_all()
        self.assertEqual(len(vehicles), 10, "Should load 10 vehicles")
    
    def test_search_valid(self):
        """Test valid search returns correct results"""
        results = self.inventory.search_by_model("Model 3")
        self.assertEqual(len(results), 2, "Should find 2 Model 3 variants")
        
        results = self.inventory.search_by_model("cybertruck")
        self.assertEqual(len(results), 2, "Should find 2 Cybertruck variants")
    
    def test_search_invalid(self):
        """Test invalid search returns no results"""
        results = self.inventory.search_by_model("InvalidModel")
        self.assertEqual(len(results), 0, "Should return no results for invalid model")
    
    def test_search_case_insensitive(self):
        """Test search is case insensitive"""
        results_lower = self.inventory.search_by_model("model s")
        results_upper = self.inventory.search_by_model("MODEL S")
        self.assertEqual(len(results_lower), len(results_upper), 
                         "Case should not affect search results")
    
    def test_input_validation_valid(self):
        """Test valid input passes validation"""
        self.assertTrue(self.inventory.is_valid_search_input("Model 3"))
        self.assertTrue(self.inventory.is_valid_search_input("Cyber-truck"))
        self.assertTrue(self.inventory.is_valid_search_input("Model_X"))
    
    def test_input_validation_invalid(self):
        """Test invalid input fails validation"""
        self.assertFalse(self.inventory.is_valid_search_input("Model; DROP TABLE vehicles;"))
        self.assertFalse(self.inventory.is_valid_search_input("<script>alert('xss')</script>"))
        self.assertFalse(self.inventory.is_valid_search_input("A" * 101))
        self.assertFalse(self.inventory.is_valid_search_input("Model$3#"))


# --- Main ---
if __name__ == "__main__":
    # Run tests if requested
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("Running unit tests...")
        unittest.main(argv=sys.argv[:1])
    else:
        # Run the application
        root = tk.Tk()
        app = VoltWheelsApp(root)
        root.mainloop()