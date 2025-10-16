import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random, csv, os

# -------------------- Data Structures --------------------
class Investor:
    def __init__(self, inv_id, name, ipo, shares):
        self.id = inv_id
        self.name = name
        self.ipo = ipo
        self.shares = shares
        self.next = None  # For linked list

class Queue:
    def __init__(self): self.items = []
    def enqueue(self, x): self.items.append(x)
    def dequeue(self): return self.items.pop(0) if self.items else None
    def is_empty(self): return len(self.items) == 0
    def get_all(self): return self.items

class Stack:
    def __init__(self): self.items = []
    def push(self, x): self.items.append(x)
    def pop(self): return self.items.pop() if self.items else None
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

# -------------------- IPO App --------------------
class IPOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IPO Subscription Simulator")
        self.root.geometry("900x600")
        self.root.config(bg="#f0f4f8")

        self.api_key = "YOUR_API_KEY_HERE"

        # DSA Structures
        self.queue = Queue()
        self.rejected = Stack()
        self.allottees = LinkedList()

        self.ipo_list = ["TechNova Ltd", "GreenEnergy Co", "FoodiesHub", "MediCore Pharma", "AquaPure Ltd"]

        self.load_data()
        self.setup_ui()

    # -------------------- UI --------------------
    def setup_ui(self):
        tk.Label(self.root, text="IPO Subscription Simulator", font=("Helvetica", 20, "bold"), fg="#0f172a", bg="#f0f4f8").pack(pady=10)

        form = tk.Frame(self.root, bg="#f0f4f8")
        form.pack(pady=10)

        tk.Label(form, text="Investor ID:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        tk.Label(form, text="Name:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        tk.Label(form, text="Select IPO:").grid(row=2, column=0, padx=5, pady=2, sticky='w')
        tk.Label(form, text="Shares (Lot-wise, 50 per lot):").grid(row=3, column=0, padx=5, pady=2, sticky='w')

        self.entry_id = tk.Entry(form)
        self.entry_name = tk.Entry(form)
        self.ipo_choice = ttk.Combobox(form, values=self.ipo_list, state="readonly")
        self.ipo_choice.current(0)
        self.entry_shares = tk.Entry(form)

        self.entry_id.grid(row=0, column=1, padx=5, pady=2)
        self.entry_name.grid(row=1, column=1, padx=5, pady=2)
        self.ipo_choice.grid(row=2, column=1, padx=5, pady=2)
        self.entry_shares.grid(row=3, column=1, padx=5, pady=2)

        tk.Button(form, text="Apply for IPO", command=self.apply_ipo, bg="#2563eb", fg="white").grid(row=4, column=0, columnspan=2, pady=6)
        tk.Button(form, text="Process All Applications", command=self.process_all, bg="#22c55e", fg="white").grid(row=5, column=0, columnspan=2, pady=4)
        tk.Button(form, text="Reset", command=self.reset_all, bg="#ef4444", fg="white").grid(row=6, column=0, columnspan=2, pady=4)

        # AI Assistant
        ai_frame = tk.LabelFrame(self.root, text="AI Assistant", bg="#f0f4f8")
        ai_frame.pack(pady=10, fill='both', expand=True)
        self.ai_box = scrolledtext.ScrolledText(ai_frame, height=6)
        self.ai_box.pack(expand=True, fill='both', padx=5, pady=5)
        tk.Button(ai_frame, text="Ask AI", command=self.ai_response, bg="#f97316", fg="white").pack(pady=4)

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill='both')

        self.tab_queue = ttk.Frame(self.tabs)
        self.tab_allot = ttk.Frame(self.tabs)
        self.tab_reject = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_queue, text='Pending Queue')
        self.tabs.add(self.tab_allot, text='Allottees')
        self.tabs.add(self.tab_reject, text='Rejected')

        self.table_queue = self.create_table(self.tab_queue, ["ID", "Name", "IPO", "Shares"])
        self.table_allot = self.create_table(self.tab_allot, ["ID", "Name", "IPO", "Shares"])
        self.table_reject = self.create_table(self.tab_reject, ["ID", "Name", "IPO", "Shares"])

        self.refresh_tables()

    def create_table(self, parent, cols):
        table = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=150)
        table.pack(expand=True, fill='both', padx=10, pady=10)
        return table

    # -------------------- Functionalities --------------------
    def apply_ipo(self):
        try:
            inv_id = int(self.entry_id.get())
            name = self.entry_name.get()
            ipo = self.ipo_choice.get()
            shares = int(self.entry_shares.get()) * 50

            investor = Investor(inv_id, name, ipo, shares)
            self.queue.enqueue(investor)
            self.save_data()
            messagebox.showinfo("Success", f"Application for {ipo} submitted by {name}.")
            self.refresh_tables()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric inputs.")

    def process_all(self):
        if self.queue.is_empty():
            messagebox.showwarning("Empty", "No applications to process.")
            return
        while not self.queue.is_empty():
            inv = self.queue.dequeue()
            # 50% chance approve / reject
            if random.random() < 0.5:
                self.allottees.add(inv)
            else:
                self.rejected.push(inv)
        self.save_data()
        messagebox.showinfo("Done", "All applications processed!")
        self.refresh_tables()

    def refresh_tables(self):
        for tbl in [self.table_queue, self.table_allot, self.table_reject]:
            for r in tbl.get_children(): tbl.delete(r)
        for q in self.queue.get_all():
            self.table_queue.insert('', 'end', values=(q.id, q.name, q.ipo, q.shares))
        for a in self.allottees.get_all():
            self.table_allot.insert('', 'end', values=(a.id, a.name, a.ipo, a.shares))
        for r in self.rejected.get_all():
            self.table_reject.insert('', 'end', values=(r.id, r.name, r.ipo, r.shares))

    def reset_all(self):
        self.queue = Queue()
        self.rejected = Stack()
        self.allottees = LinkedList()
        self.save_data()
        self.refresh_tables()
        messagebox.showinfo("Reset", "All data cleared successfully!")

    # -------------------- AI Assistant --------------------
    def ai_response(self):
        user_input = self.ai_box.get('1.0', tk.END).strip()
        if not user_input: return
        response = f"AI Tip: Choose IPO wisely. Currently, {len(self.ipo_list)} IPOs are available."
        self.ai_box.insert(tk.END, f"\nUser: {user_input}\n{response}\n")
        self.ai_box.see(tk.END)

    # -------------------- Persistent Storage --------------------
    def save_data(self):
        self.save_list(self.queue.get_all(), 'queue.csv')
        self.save_list(self.allottees.get_all(), 'allottees.csv')
        self.save_list(self.rejected.get_all(), 'rejected.csv')

    def load_data(self):
        for inv in self.load_list('queue.csv'): self.queue.enqueue(inv)
        for inv in self.load_list('allottees.csv'): self.allottees.add(inv)
        for inv in self.load_list('rejected.csv'): self.rejected.push(inv)

    def save_list(self, lst, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for inv in lst:
                writer.writerow([inv.id, inv.name, inv.ipo, inv.shares])

    def load_list(self, filename):
        lst = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4:
                        lst.append(Investor(int(row[0]), row[1], row[2], int(row[3])))
        return lst

# -------------------- Run --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = IPOApp(root)
    root.mainloop()
