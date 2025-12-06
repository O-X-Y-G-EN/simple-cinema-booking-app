import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class CinemaBookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Cinema Booking")
        self.geometry("450x350")
        self.config(bg="#f0f0f0") # Light gray background for a clean look

        # --- Data Mock-up ---
        self.movies = {
            "Action Hero 3": {"seats": [f"A{i}" for i in range(1, 11)], "price": 12.00},
            "Comedy Central": {"seats": [f"B{i}" for i in range(1, 11)], "price": 10.50},
            "Sci-Fi Odyssey": {"seats": [f"C{i}" for i in range(1, 11)], "price": 14.00},
        }
        self.available_seats = {} # Tracks available seats per movie
        for movie, data in self.movies.items():
            self.available_seats[movie] = set(data["seats"])

        self.selected_movie = tk.StringVar(self)
        self.selected_seat = tk.StringVar(self)
        self.selected_movie.set(list(self.movies.keys())[0]) # Set default movie

        self.create_widgets()

    def create_widgets(self):
        # Header Label
        tk.Label(self, text="🍿 Cinema Ticket Reservation 🎫", font=("Helvetica", 16, "bold"), 
                 bg="#3b5998", fg="white", pady=10).pack(fill='x', pady=5)
        
        # --- Movie Selection Frame ---
        movie_frame = ttk.Frame(self, padding="10")
        movie_frame.pack(pady=10)
        
        ttk.Label(movie_frame, text="Select Movie:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        movie_options = list(self.movies.keys())
        movie_dropdown = ttk.OptionMenu(movie_frame, self.selected_movie, self.selected_movie.get(), *movie_options, command=self.update_seats)
        movie_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # --- Seat Selection Frame ---
        seat_frame = ttk.Frame(self, padding="10")
        seat_frame.pack(pady=10)
        
        ttk.Label(seat_frame, text="Select Seat:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Dropdown for seats (will be updated)
        self.seat_dropdown = ttk.OptionMenu(seat_frame, self.selected_seat, "Select...", *["Select..."])
        self.seat_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Initialize seat options based on the default movie
        self.update_seats(self.selected_movie.get())

        # --- Book Button ---
        ttk.Button(self, text="Book Ticket", command=self.book_ticket, style='Accent.TButton').pack(pady=20)
        
    def update_seats(self, movie_name):
        """Updates the seat dropdown based on the selected movie."""
        seats_list = sorted(list(self.available_seats[movie_name]))
        
        # Reset the seat dropdown options
        menu = self.seat_dropdown["menu"]
        menu.delete(0, "end")
        
        if seats_list:
            self.selected_seat.set(seats_list[0]) # Set the first seat as default
            for seat in seats_list:
                menu.add_command(label=seat, command=tk._setit(self.selected_seat, seat))
        else:
            self.selected_seat.set("No Seats")
            messagebox.showinfo("Fully Booked", f"Sorry, '{movie_name}' is currently fully booked!")
            
    def book_ticket(self):
        """Handles the ticket booking logic."""
        movie = self.selected_movie.get()
        seat = self.selected_seat.get()

        if seat == "Select..." or seat == "No Seats":
            messagebox.showerror("Error", "Please select a valid seat.")
            return

        price = self.movies[movie]["price"]
        
        # Confirmation Dialog
        confirm = messagebox.askyesno(
            "Confirm Booking",
            f"Confirm booking for:\n\nMovie: {movie}\nSeat: {seat}\nPrice: ${price:.2f}"
        )

        if confirm:
            # Update the mock database
            self.available_seats[movie].remove(seat)
            
            # Show success message
            messagebox.showinfo(
                "Booking Successful! ✅",
                f"Your ticket for {movie} at seat {seat} has been booked.\nTotal Paid: ${price:.2f}"
            )
            
            # Update the seat dropdown for the remaining available seats
            self.update_seats(movie)
            
if __name__ == "__main__":
    app = CinemaBookingApp()
    app.mainloop()