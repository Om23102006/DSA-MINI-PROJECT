🌟 IPO Subscription Simulator 🌟
Overview:
The IPO Subscription Simulator is a Python desktop application built using Tkinter. It simulates the process of applying for Initial Public Offerings (IPOs), automatically validating applications, and allotting or rejecting shares based on availability.
This project demonstrates the use of data structures like Queue, Stack, and Linked List to manage IPO applications, along with a clean and interactive GUI.

Features:
Apply for IPO with Investor ID, Name, IPO selection, and number of shares.
Automatic allotment or rejection based on share availability.
Duplicate investor ID validation.
Display pending queue, allottees, and rejected investors in separate tabs.
Export allotment and rejection data to CSV.
Reset all data for a fresh start.
IPO Info panel showing price, available shares, and status.

Technologies Used:
Python 3.x
Tkinter for GUI
CSV module for data export
OOP concepts and data structures (Queue, Stack, LinkedList)

Data Structures:
Queue: Holds pending IPO applications (for future extensions).
Stack: Stores rejected applications.
Linked List: Stores successfully allotted investors.

Usage:
Fill in Investor ID, Name, select IPO, and enter number of shares.
Click Apply for IPO to automatically process the application.
View results in the respective tabs:
Pending Queue (currently not used as auto-validation is applied)
Allottees (successfully allotted investors)
Rejected (applications exceeding available shares)
Export data to CSV using Export CSV button.
Reset all data using Reset All button.
