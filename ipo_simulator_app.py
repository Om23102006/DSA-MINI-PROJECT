import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# -------------------- Data Structures --------------------
class Investor:
    def __init__(self, inv_id, name, ipo, shares):
        self.id = inv_id
        self.name = name
        self.ipo = ipo
        self.shares = shares
        self.next = None

class Queue:
    def __init__(self): self.items = []
    def enqueue(self, x): self.items.append(x)
    def dequeue(self): return self.items.pop(0) if not self.is_empty() else None
    def is_empty(self): return len(self.items) == 0
    def get_all(self): return self.items

class Stack:
    def __init__(self): self.items = []
    def push(self, x): self.items.append(x)
    def pop(self): return self.items.pop() if not self.is_empty() else None
    def is_empty(self): return len(self.items) == 0
    def get_all(self): return self.items[::-1]

class LinkedList:
    def __init__(self): self.head = None
    def add(self, inv):
        if not self.head: self.head = inv
        else:
            temp = self.head
            while temp.next: temp = temp.next
            temp.next = inv
    def get_all(self):
        res = []
        temp = self.head
        while temp:
            res.append(temp)
            temp = temp.next
        return res

# -------------------- Main App --------------------
class IPOAppAutoValidation:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 IPO Simulator (Auto Validation) 🌟")
        self.root.geometry("950x600")
        self.root.configure(bg="#1f2937")

        # Data structures
        self.queue = Queue()
        self.rejected = Stack()
        self.allottees = LinkedList()

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="IPO Subscription Simulator", font=("Helvetica", 20, "bold"), bg="#1f2937", fg="#facc15")
        title.pack(pady=15)

        # Form Frame
        form_frame = tk.Frame(self.root, bg="#1f2937")
        form_frame.pack(pady=10)

        labels = ["Investor ID:", "Name:", "Select IPO:", "Shares:"]
        self.entries = []

        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg="#1f2937", fg="#fef3c7", font=("Arial", 12)).grid(row=i, column=0, sticky="w", padx=5, pady=3)

        self.entry_id = tk.Entry(form_frame)
        self.entry_name = tk.Entry(form_frame)
        self.ipo_choice = ttk.Combobox(form_frame, values=["TechNova Ltd", "GreenEnergy Co", "FoodiesHub", "MediCore Pharma"], state="readonly")
        self.ipo_choice.current(0)
        self.entry_shares = tk.Entry(form_frame)

        self.entries = [self.entry_id, self.entry_name, self.ipo_choice, self.entry_shares]

        for i, e in enumerate(self.entries):
            e.grid(row=i, column=1, padx=5, pady=3)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1f2937")
        btn_frame.pack(pady=10)

        btn_config = {"bg": "#f59e0b", "fg": "#1f2937", "font": ("Arial", 11, "bold"), "width": 20, "bd": 0, "activebackground": "#fbbf24"}

        tk.Button(btn_frame, text="Apply for IPO", command=self.apply_ipo, **btn_config).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Process All", command=self.process_all, **btn_config).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset All", command=self.reset_all, **btn_config).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Export CSV", command=self.export_csv, **btn_config).grid(row=0, column=3, padx=5)

        # Notebook
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_queue = ttk.Frame(self.tabs)
        self.tab_allot = ttk.Frame(self.tabs)
        self.tab_reject = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_queue, text="Pending Queue")
        self.tabs.add(self.tab_allot, text="Allottees")
        self.tabs.add(self.tab_reject, text="Rejected")

        self.table_queue = self.create_table(self.tab_queue, ["ID", "Name", "IPO", "Shares"], "#fef3c7")
        self.table_allot = self.create_table(self.tab_allot, ["ID", "Name", "IPO", "Shares"], "#bbf7d0")
        self.table_reject = self.create_table(self.tab_reject, ["ID", "Name", "IPO", "Shares"], "#fecaca")

        # IPO Info Panel
        info_frame = tk.Frame(self.root, bg="#1f2937")
        info_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(info_frame, text="IPO Info Panel", font=("Arial", 12, "bold"), bg="#1f2937", fg="#fef3c7").pack(anchor="w")
        self.ipo_info = tk.Label(info_frame, text="Select an IPO to see details...", bg="#1f2937", fg="#fef3c7", font=("Arial", 11))
        self.ipo_info.pack(anchor="w")
        self.ipo_choice.bind("<<ComboboxSelected>>", self.update_ipo_info)

    def create_table(self, parent, columns, color):
        table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for c in columns:
            table.heading(c, text=c)
            table.column(c, width=140)
        table.pack(expand=True, fill="both", padx=5, pady=5)
        table.tag_configure("row_color", background=color)
        return table

    # -------------------- IPO Info --------------------
    def update_ipo_info(self, event=None):
        ipo_name = self.ipo_choice.get()
        data = {"price": 100, "available_shares": 5000, "status": "Open"}
        self.ipo_info.config(text=f"IPO: {ipo_name} | Price: ₹{data['price']} | Available Shares: {data['available_shares']} | Status: {data['status']}")

    # -------------------- Functionalities --------------------
    def apply_ipo(self):
        try:
            inv_id = int(self.entry_id.get())
            name = self.entry_name.get().strip()
            ipo = self.ipo_choice.get()
            shares = int(self.entry_shares.get())

            if shares <= 0:
                messagebox.showerror("Error", "Shares must be >0")
                return

            # Duplicate check
            existing_ids = [inv.id for inv in self.queue.get_all()] + \
                           [a.id for a in self.allottees.get_all()] + \
                           [r.id for r in self.rejected.get_all()]
            if inv_id in existing_ids:
                messagebox.showerror("Error", f"Investor ID {inv_id} already exists.")
                return

            # Auto-validation based on dummy available shares
            available_shares = 5000
            if shares <= available_shares:
                investor = Investor(inv_id, name, ipo, shares)
                self.allottees.add(investor)
            else:
                investor = Investor(inv_id, name, ipo, shares)
                self.rejected.push(investor)

            self.refresh_tables()
            messagebox.showinfo("Success", f"Application processed for {name} ({ipo})")

        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input")

    def process_all(self):
        messagebox.showinfo("Info", "Applications are automatically processed upon submission.")

    def refresh_tables(self):
        for tbl in [self.table_queue, self.table_allot, self.table_reject]:
            for r in tbl.get_children(): tbl.delete(r)
        for a in self.allottees.get_all():
            self.table_allot.insert("", "end", values=(a.id, a.name, a.ipo, a.shares), tags=("row_color",))
        for r in self.rejected.get_all():
            self.table_reject.insert("", "end", values=(r.id, r.name, r.ipo, r.shares), tags=("row_color",))

    def reset_all(self):
        self.queue = Queue()
        self.rejected = Stack()
        self.allottees = LinkedList()
        self.refresh_tables()
        messagebox.showinfo("Reset", "All data cleared!")

    def export_csv(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
            if not filename: return
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID","Name","IPO","Shares","Status"])
                for a in self.allottees.get_all():
                    writer.writerow([a.id, a.name, a.ipo, a.shares, "Allotted"])
                for r in self.rejected.get_all():
                    writer.writerow([r.id, r.name, r.ipo, r.shares, "Rejected"])
            messagebox.showinfo("Export", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")

# -------------------- Run App --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = IPOAppAutoValidation(root)
    root.mainloop()
    