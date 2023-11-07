import threading
import tkinter as tk
import traceback
from tkinter import simpledialog, messagebox, Text, END
import customtkinter
from threading import Thread
from PIL import Image, ImageTk
import requests, io
import logging
from api.openai_interface import GPTInterface
from database.db_manager import Database
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Configure logging for the application
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Initialize logging
        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            # configure window
            self.title("Synthetica")
            self.geometry(f"{1100}x{580}")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.db = Database("synt.db")
            api_token = self.db.get_api_token()
            org_id = self.db.get_api_org()
            self.gpt = GPTInterface(api_token, org_id)
            self.radio_var = tk.IntVar(value=0)
            self.init_ui()
        except Exception as e:
            self.logger.error(f"Failed to initialize the application: {e}")
            self.logger.debug(traceback.format_exc())

    def init_ui(self):
        try:
            # Configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)
            self.appearance_mode_optionemenu.set("Dark")
            logging.info("Grid layout configured successfully.")
        except Exception as e:
            logging.exception("Failed to configure grid layout.")

        try:
            # Create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            logging.info("Sidebar frame created successfully.")
        except Exception as e:
            logging.exception("Failed to create sidebar frame.")

        try:
            # Create tabview
            self.tabview = customtkinter.CTkTabview(self.sidebar_frame)
            self.tabview.grid(row=0, column=0, rowspan=5, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.tabview.add("OpenAI")
            self.tabview.tab("OpenAI").grid_columnconfigure(0, weight=1)
            self.tabview.tab("OpenAI").grid_rowconfigure(1, weight=1)
            self.tabview.add("Settings")
            self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)
            logging.info("Tabview created successfully.")
        except Exception as e:
            logging.exception("Failed to create tabview.")

        try:
            # Create buttons, labels, entries, and listboxes for the AI tab
            self.history_delete_btn = customtkinter.CTkButton(self.tabview.tab("OpenAI"), text="Delete Selected", command=self.delete_selected)
            self.history_delete_btn.grid(row=6, column=0, padx=20, pady=(10, 10))
            self.history_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="Prompt History:")
            self.history_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.history_listbox = tk.Listbox(self.tabview.tab("OpenAI"), exportselection=False, selectmode=tk.SINGLE, bd=0,
                                              activestyle="none", highlightthickness=0, bg="#2e2e2e", fg="white",
                                              selectbackground="#555555", selectforeground="white",
                                              font=("Helvetica", 14))
            self.history_listbox.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
            self.load_history()
            self.history_listbox.bind('<Double-Button-1>', self.on_history_select)
            logging.info("Widgets for AI tab created successfully.")
        except Exception as e:
            logging.exception("Failed to create widgets for AI tab.")

        try:
            # OpenAI Credentials in Settings tab
            self.oai_label = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="OpenAI Credentials:")
            self.oai_label.grid(row=0, column=0, padx=20, pady=0)
            self.oai_api_entry = customtkinter.CTkEntry(self.tabview.tab("Settings"), placeholder_text="API:")
            self.oai_api_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.oai_org_entry = customtkinter.CTkEntry(self.tabview.tab("Settings"), placeholder_text="Org:")
            self.oai_org_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            self.oai_save = customtkinter.CTkButton(self.tabview.tab("Settings"), fg_color="transparent",
                                                    border_width=1,
                                                    text="Save", text_color=("gray10", "#DCE4EE"),
                                                    command=self.save_credentials)
            self.oai_save.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

            self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="Appearance Mode:", anchor="w")
            self.appearance_mode_label.grid(row=4, column=0, padx=5, pady=(20, 0))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Settings"),
                                                                           values=["Dark","Light",  "System"],
                                                                           command=self.change_appearance_mode_event)
            self.appearance_mode_optionemenu.grid(row=5, column=0, padx=5, pady=5)
            logging.info("OpenAI credentials widgets created successfully.")
        except Exception as e:
            logging.exception("Failed to create OpenAI credentials widgets.")


        try:
            # Question Entry and Submit Button
            self.question_entry = customtkinter.CTkEntry(self, placeholder_text="Enter your question:")
            self.question_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
            self.question_entry.bind("<Return>", self.submit_question)
            self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                         text="Submit", text_color=("gray10", "#DCE4EE"),
                                                         command=self.submit_question)
            self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
            logging.info("Question entry and submit button created successfully.")
        except Exception as e:
            logging.exception("Failed to create question entry and submit button.")

        try:
            # Response Textbox
            self.response_text = customtkinter.CTkTextbox(self, width=250, wrap='word')
            self.response_text.grid(row=0, column=1, columnspan=3, rowspan=3, padx=(10, 10), pady=(10, 0),
                                    sticky="nsew")
            logging.info("Response textbox created successfully.")
        except Exception as e:
            logging.exception("Failed to create response textbox.")

        try:
            # Radio Buttons for ChatGPT and DALL-E
            self.radio_var = tk.IntVar(value=0)
            self.radio_button_chat = customtkinter.CTkRadioButton(self.sidebar_frame, text="ChatGPT",
                                                                  variable=self.radio_var, value=0,
                                                                  command=self.switch_response_widget)
            self.radio_button_chat.grid(row=6, column=0, padx=20, pady=(10, 10))
            self.radio_button_dalle = customtkinter.CTkRadioButton(self.sidebar_frame, text="DALL-E",
                                                                   variable=self.radio_var, value=1,
                                                                   command=self.switch_response_widget)
            self.radio_button_dalle.grid(row=7, column=0, padx=20, pady=(10, 10))
            logging.info("Radio buttons for ChatGPT and DALL-E created successfully.")
        except Exception as e:
            logging.exception("Failed to create radio buttons for ChatGPT and DALL-E.")

        try:
            # Response Canvas for DALL-E
            self.response_canvas = tk.Canvas(self, width=250, height=self.response_text.winfo_height(), bg='gray13', highlightthickness=0)
            # The canvas is not gridded yet because its display depends on the radio button selection
            logging.info("Response canvas for DALL-E created successfully.")
        except Exception as e:
            logging.exception("Failed to create response canvas for DALL-E.")

    def load_history(self):
        try:
            self.history_listbox.delete(0, END)
            questions = self.db.get_questions()
            for question in questions:
                self.history_listbox.insert(END, question + "\n")
        except Exception as e:
            logging.error(f"Error loading history: {e}")


    def credentials_are_set(self):
        api_token = self.db.get_api_token()
        org_id = self.db.get_api_org()
        return api_token is not None and api_token != "" and org_id is not None and org_id != ""

    def submit_question(self, event=None):
        try:
            if not self.credentials_are_set():
                messagebox.showinfo("Missing Credentials", "Please set you Token and Org in the Settings Tab")
                return

            question = self.question_entry.get()
            self.question_entry.delete(0, END)
            if question:
                if self.radio_var.get() == 0:
                    self.db.add_question(question)
                    self.load_history()
                    Thread(target=self.fetch_response, args=(question,)).start()
                else:
                    self.db.add_question(question)
                    self.load_history()
                    Thread(target=self.generate_and_display_dalle_image, args=(question,)).start()
        except Exception as e:
            logging.error(f"Error submitting question: {e}")

    # def fetch_response(self, question):
    #     try:
    #         response = self.gpt.get_response(question)
    #         self.response_text.delete("1.0", END)
    #         self.response_text.insert(END, response)
    #     except Exception as e:
    #         logging.error(f"Error fetching response: {e}")

    def update_status_message(self, message, count=0):
        if self.fetch_complete:  # Stop updating the message if fetch is complete
            return

        dots = "." * (count % 4)  # Change the number of dots every second
        final_message = message + dots
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, final_message)
        count += 1
        self.after(1000, self.update_status_message, message, count)

    def fetch_response(self, question):
        self.fetch_complete = False
        self.update_status_message("Fetching data")  # Start the 'Fetching data...' message with dots

        def after_fetch():
            try:
                response = self.gpt.get_response(question)
                self.response_text.delete("1.0", tk.END)
                self.response_text.insert(tk.END, response)
            except Exception as e:
                self.response_text.delete("1.0", tk.END)
                self.response_text.insert(tk.END, f"An error occurred: {e}")
            finally:
                self.fetch_complete = True  # Set this to True when fetch is complete or an exception occurs

        # Run the fetch operation in a separate thread if it's blocking
        threading.Thread(target=after_fetch).start()

    def on_closing(self):
        self.db.conn.close()
        self.destroy()

    def save_token(self):
        try:
            token = self.oai_api_entry.get()
            self.db.set_api_token(token)
            self.gpt.set_api_token(token)
            self.oai_save.configure(text="Saved!", text_color="green")
            self.oai_api_entry.delete(0, 'end')
            self.oai_api_entry.insert(0, '')
            self.after(2000, lambda: self.oai_save.configure(text="Save", text_color=("gray10", "#DCE4EE")))
        except Exception as e:
            logging.error(f"Error saving token: {e}")

    def save_org(self):
        try:
            org = self.oai_org_entry.get()
            self.db.set_api_org(org)
            self.gpt.set_api_org(org)
            self.oai_save.configure(text="Saved!", text_color="green")
            self.oai_org_entry.delete(0, 'end')
            self.oai_org_entry.insert(0, '')
            self.after(2000, lambda: self.oai_save.configure(text="Save", text_color=("gray10", "#DCE4EE")))
        except Exception as e:
            logging.error(f"Error saving org: {e}")

    def save_credentials(self):
        self.save_token()
        self.save_org()

    # Modify the delete_selected function
    def delete_selected(self):
        try:
            selected_indices = self.history_listbox.curselection()
            if selected_indices:
                selected_index = selected_indices[0]
                question = self.history_listbox.get(selected_index).strip()
                self.history_listbox.delete(selected_index)
                self.db.delete_question(question)
                self.load_history()
        except Exception as e:
            logging.error(f"Error deleting selected: {e}")

    # Update the on_history_select function to use question_entry instead of prompt_entry
    def on_history_select(self, event):
        try:
            selected_index = self.history_listbox.curselection()

            if selected_index:
                selected_question = self.history_listbox.get(selected_index)

                self.question_entry.delete(0, customtkinter.END)
                self.question_entry.insert(0, selected_question.strip())

                self.submit_question()
        except Exception as e:
            logging.error(f"Error selecting history: {e}")

    def load_dalle_image(self):
        try:
            # Load the image from the file
            image = Image.open("assets/Dalle.png")  # Corrected path

            # Get the canvas dimensions
            canvas_width = self.response_canvas.winfo_width()
            canvas_height = self.response_canvas.winfo_height()

            # Calculate the resize ratio to maintain aspect ratio
            img_width, img_height = image.size
            width_ratio = canvas_width / img_width
            height_ratio = canvas_height / img_height
            scale_ratio = max(width_ratio, height_ratio)  # Use max to fill the canvas

            # Compute the new size to fill the canvas
            new_width = int(img_width * scale_ratio)
            new_height = int(img_height * scale_ratio)

            # Resize the image with the computed size
            image = image.resize((new_width, new_height), Image.BILINEAR)

            # Create a PhotoImage object from the loaded image
            image = ImageTk.PhotoImage(image)

            # Center the image on the canvas
            x_position = (canvas_width - new_width) // 2
            y_position = (canvas_height - new_height) // 2

            # Display the image on the canvas, centered
            self.response_canvas.create_image(x_position, y_position, anchor=tk.NW, image=image)

            # Keep a reference to prevent image from being garbage collected
            self.response_canvas.image = image
        except Exception as e:
            print(f"Error loading image: {e}")

    def switch_response_widget(self):
        try:
            self.response_text.grid_remove()
            self.response_canvas.grid_remove()

            if self.radio_var.get() == 0:
                self.response_text.grid(row=0, column=1, columnspan=3, rowspan=3, padx=(10, 10), pady=(10, 0),
                                        sticky="nsew")
            else:
                self.after(100, self.load_dalle_image)
                self.response_canvas.grid(row=0, column=1, columnspan=3, rowspan=3, padx=(10, 10), pady=(10, 0),
                                          sticky="nsew")
        except Exception as e:
            logging.error(f"Error switching response widget: {e}")



    def generate_and_display_dalle_image(self, question):
        try:
            url = self.gpt.create_image_response(question)

            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))

            canvas_width = self.response_canvas.winfo_width()
            canvas_height = self.response_canvas.winfo_height()

            image = image.resize((canvas_width, canvas_height))
            photo_image = ImageTk.PhotoImage(image)

            self.response_canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
            self.response_canvas.photo_image = photo_image
        except Exception as e:
            logging.error(f"Error generating/displaying DALL-E image: {e}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        try:
            customtkinter.set_appearance_mode(new_appearance_mode)
        except Exception as e:
            logging.error(f"Error generating/displaying DALL-E image: {e}")

