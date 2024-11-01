import tkinter as tk
from tkinter import simpledialog, Label, Button, messagebox

class DeadlockSolver:
    def __init__(self):
        self.num_processes = 0
        self.resources = 0
        self.allocated = []
        self.max_resources = []
        self.available = []
        self.need = []
        self.safe_sequence = []

    def get_num_processes(self):
        self.num_processes = simpledialog.askinteger("Input", "Enter the number of processes:", minvalue=1)

    def get_resources(self):
        self.resources = simpledialog.askinteger("Input", "Enter the number of resource types:", minvalue=1)

    def get_allocated_resources(self):
        for i in range(1, self.num_processes + 1):
            allocation = simpledialog.askstring("Input", f"Enter allocated resources for process {i} (space-separated values):")
            allocation = list(map(int, allocation.split()))
            self.allocated.append(allocation)

    def get_max_resources(self):
        for i in range(1, self.num_processes + 1):
            max_resource = simpledialog.askstring("Input", f"Enter maximum resource requirements for process {i} (space-separated values):")
            max_resource = list(map(int, max_resource.split()))
            self.max_resources.append(max_resource)

    def get_available_resources(self):
        available = simpledialog.askstring("Input", "Enter available resources (space-separated values):")
        self.available = list(map(int, available.split()))

    def calculate_need_matrix(self):
        for i in range(self.num_processes):
            need_row = [self.max_resources[i][j] - self.allocated[i][j] for j in range(self.resources)]
            self.need.append(need_row)

    def is_less_than_or_equal(self, a, b):
        return all(a[i] <= b[i] for i in range(len(a)))

    def find_safe_sequence(self):
        work = self.available[:]
        finish = [False] * self.num_processes

        while True:
            found = False
            for i in range(1, self.num_processes + 1):
                index = i - 1  # Adjust index to start from 0
                if not finish[index] and self.is_less_than_or_equal(self.need[index], work):
                    work = [work[j] + self.allocated[index][j] for j in range(self.resources)]
                    finish[index] = True
                    self.safe_sequence.append(index + 1)  # Corrected indexing
                    found = True
                    
            if not found:
                break

        return all(finish)


    def display_allocation_max_need(self):
        result = "Allocation Matrix:\n"
        for i in range(self.num_processes):
            result += str(self.allocated[i]) + "\n"

        result += "\nMax Resource Matrix:\n"
        for i in range(self.num_processes):
            result += str(self.max_resources[i]) + "\n"

        result += "\nNeed Matrix:\n"
        for i in range(self.num_processes):
            result += str(self.need[i]) + "\n"

        return result

    def display_result(self):
        result = self.display_allocation_max_need()

        if self.find_safe_sequence():
            result += "\nSafe sequence: " + str(self.safe_sequence)
        else:
            result += "\nNo safe sequence found. Deadlock detected."

        return result

def run_solver():
    solver = DeadlockSolver()
    solver.get_num_processes()
    solver.get_resources()
    solver.get_allocated_resources()
    solver.get_max_resources()
    solver.get_available_resources()
    solver.calculate_need_matrix()
    result = solver.display_result()
    
    # Create a new window to display the result
    result_window = tk.Toplevel(root)
    result_window.title("Deadlock Solver Result")
    result_window.geometry("600x500")  # Set window size
    result_window.configure(bg="lightblue")  # Set background color

    result_label = Label(result_window, text=result, font=("Helvetica", 12), bg="lightblue")
    result_label.pack(pady=10)

    # Ask if the user wants to solve another deadlock
    solve_another = messagebox.askyesno("Solve Another Deadlock", "Do you want to solve another deadlock?")
    
    if solve_another:
        # Destroy the result window and reset the solver attributes for the new deadlock
        result_window.destroy()
        solver.allocated = []
        solver.max_resources = []
        solver.available = []
        solver.need = []
        solver.safe_sequence = []
        run_solver()
    else:
        messagebox.showinfo("Thank You", "Thank you for using the Deadlock Solver!")

# GUI setup
root = tk.Tk()
root.title("Deadlock Solver")
root.geometry("500x400")  # Set window size
root.configure(bg="lightblue")  # Set background color

Label(root, text="Welcome to Deadlock Solver", font=("Helvetica", 16), bg="lightblue").pack(pady=20)

Button(root, text="Run Solver", command=run_solver, bg="light pink").pack()

root.mainloop()
