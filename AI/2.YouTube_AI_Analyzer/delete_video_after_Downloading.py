import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from tkinter import ttk
import google.generativeai as genai
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress


# --- Google Gemini API Setup ---
model_names = [
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
]

api_key = "AIzaSyAMPldBGV9CeYfSV4MUps6cKtEULNQAydk"
genai.configure(api_key=api_key)

# --- Global Variables ---
chat_sessions = {} 
active_chat_id = None
chat_count = 1
downloading = False

# --- Functions ---
def create_new_chat_session(chat_id):
    """Creates a new chat session with Gemini."""
    global chat_sessions
    for model_name in model_names:
        try:
            chat_session = genai.GenerativeModel(model_name=model_name).start_chat()
            chat_sessions[chat_id] = {
                "session": chat_session,
                "history": [],
                "uploaded_files": [],
            }
            update_chat_history_list()
            display_chat(chat_id)
            return True
        except Exception as e:
            print(f"Error trying model '{model_name}': {e}")
    print("Error: Could not create a chat session with any available model.")
    return False

def send_message(event=None):
    """Sends the user's message and uploaded files to Gemini."""
    global active_chat_id, chat_sessions
    if active_chat_id is None:
        return

    user_input = input_field.get("1.0", tk.END).strip()
    input_field.delete("1.0", tk.END)

    if user_input:
        chat_data = chat_sessions.get(active_chat_id)
        if chat_data:
            try:
                chat_session = chat_data["session"]
                prompt_parts = [user_input] + chat_data["uploaded_files"]
                response = chat_session.send_message(prompt_parts)

                chat_data["history"].append(f"You: {user_input}")
                chat_data["history"].append(f"Gemini: {response.text}")
                chat_data["uploaded_files"] = []  # Clear uploaded files after sending
                update_chat_display(active_chat_id)
            except Exception as e:
                print(f"Error sending message: {e}")


def start_new_chat(chat_name=None):
    """Starts a new chat session, optionally with a specific name."""
    global chat_count, active_chat_id
    if chat_name is None:
        chat_name = f"Chat {chat_count}"
        chat_count += 1 
    else:
        # Ensure unique chat names, even with video titles 
        chat_name = find_unique_chat_name(chat_name)

    create_new_chat_session(chat_name)
    active_chat_id = chat_name  # Set the new chat as active

def find_unique_chat_name(base_name):
    """Appends numbers to base_name to make it unique in chat_sessions."""
    counter = 1
    new_name = base_name
    while new_name in chat_sessions:
        new_name = f"{base_name} ({counter})"
        counter += 1
    return new_name

def on_chat_selected(event):
    """Handles chat selection from the history list."""
    global active_chat_id
    selection = chat_history_list.curselection()
    if selection:
        index = selection[0]
        active_chat_id = chat_history_list.get(index)
        display_chat(active_chat_id)

def display_chat(chat_id):
    """Displays the chat history for the selected chat."""
    global chat_sessions
    chat_text.config(state="normal")
    chat_text.delete("1.0", tk.END)
    chat_data = chat_sessions.get(chat_id)
    if chat_data:
        for message in chat_data["history"]:
            chat_text.insert(tk.END, f"{message}\n")
    chat_text.config(state="disabled")

def update_chat_display(chat_id):
    """Updates the chat display after sending a message or file."""
    display_chat(chat_id)  


def update_chat_history_list():
    """Updates the chat history list and selects the active chat."""
    chat_history_list.delete(0, tk.END)
    for chat_id in chat_sessions:
        chat_history_list.insert(tk.END, chat_id)
    if active_chat_id:
        try:  
            index = chat_history_list.get(0, tk.END).index(active_chat_id)
            chat_history_list.selection_clear(0, tk.END)
            chat_history_list.selection_set(index)
        except ValueError: 
            pass

def download_youtube_video():
    """Downloads the video and renames the active chat if there is one."""
    global downloading, active_chat_id
    yt_url = youtube_entry.get()
    if not yt_url:
        messagebox.showwarning("Error", "Please enter a YouTube video URL.")
        return

    try:
        downloading = True
        download_button.config(state="disabled")
        yt = YouTube(yt_url, on_progress_callback=on_progress)
        video_title = yt.title
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(filename=f"{video_title}.mp4")
        messagebox.showinfo("Success", f"Processed '{video_title}' successfully!")
        upload_downloaded_video(f"{video_title}.mp4")

        # Rename the active chat if it exists
        if active_chat_id:
            rename_chat(active_chat_id, video_title) 
        else:
            start_new_chat(chat_name=video_title)

    except Exception as e:
        messagebox.showerror("Error", f"Could not download video: {e}")
    finally:
        downloading = False
        download_button.config(state="normal")


        

# def upload_downloaded_video(filename):
#     """Uploads the downloaded video to Gemini and adds it to the current chat session."""
#     global active_chat_id, chat_sessions
#     if active_chat_id is None:
#         return
#     chat_data = chat_sessions[active_chat_id]
#     try:
#         uploaded_file = genai.upload_file(filename)
#         processed_file = wait_for_file_processing(uploaded_file)
#         chat_data["uploaded_files"].append(processed_file)
#         chat_text.config(state="normal")
#         chat_text.insert(tk.END, f"Uploaded: {filename} (Ready!)\n")
#         chat_text.config(state="disabled")
#     except Exception as e:
#         chat_text.config(state="normal")
#         chat_text.insert(tk.END, f"Error uploading file {filename}: {e}\n")
#         chat_text.config(state="disabled")


def wait_for_file_processing(file):
    """Waits for a file to finish processing on Gemini's servers."""
    while file.state.name == "PROCESSING":
        time.sleep(2)
        file = genai.get_file(file.name)
    return file


def rename_chat(old_name, new_name):
    """Renames a chat session."""
    global chat_sessions, active_chat_id
    if old_name in chat_sessions:
        chat_sessions[new_name] = chat_sessions.pop(old_name)
        if active_chat_id == old_name:
            active_chat_id = new_name
        update_chat_history_list()



def download_youtube_video():
    """Downloads the video, renames the active chat, and handles progress."""
    global downloading, active_chat_id
    yt_url = youtube_entry.get()
    if not yt_url:
        messagebox.showwarning("Error", "Please enter a YouTube video URL.")
        return

    try:
        downloading = True
        download_button.config(state="disabled")
        progress_bar["value"] = 0  # Reset progress bar
        yt = YouTube(yt_url, on_progress_callback=on_download_progress)
        video_title = yt.title
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(filename=f"{video_title}.mp4")
        messagebox.showinfo("Success", f"Processed '{video_title}' successfully!")
        upload_downloaded_video(f"{video_title}.mp4")

        # Rename the active chat if it exists
        if active_chat_id:
            rename_chat(active_chat_id, video_title)
        else:
            start_new_chat(chat_name=video_title)

    except Exception as e:
        messagebox.showerror("Error", f"Could not download video: {e}")
    finally:
        downloading = False
        download_button.config(state="normal")
        progress_bar["value"] = 0  # Reset progress bar after download 



def upload_downloaded_video(filename):
    """Uploads the downloaded video, adds it to chat, and then deletes it."""
    global active_chat_id, chat_sessions
    if active_chat_id is None:
        return
    chat_data = chat_sessions[active_chat_id]
    try:
        uploaded_file = genai.upload_file(filename)
        processed_file = wait_for_file_processing(uploaded_file)
        chat_data["uploaded_files"].append(processed_file)
        chat_text.config(state="normal")
        chat_text.insert(tk.END, f"Uploaded: {filename} (Ready!)\n")
        chat_text.config(state="disabled")

        # Delete the file after successful upload
        try:
            os.remove(filename)
            print(f"Deleted: {filename}")
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

    except Exception as e:
        chat_text.config(state="normal")
        chat_text.insert(tk.END, f"Error uploading file {filename}: {e}\n")
        chat_text.config(state="disabled")




# --- GUI Setup ---
window = tk.Tk()
window.title("Gemini YouTube Assistant")



# --- Left Side: Chat History ---
history_frame = tk.Frame(window, width=200, borderwidth=1, relief="solid")
history_frame.pack(side="left", fill="y")

new_chat_button = tk.Button(history_frame, text="New Chat", command=start_new_chat)
new_chat_button.pack(pady=5)

chat_history_list = tk.Listbox(history_frame)
chat_history_list.pack(fill="both", expand=True)
chat_history_list.bind('<<ListboxSelect>>', on_chat_selected)

# --- Right Side: Chat Area and YouTube Download ---
right_frame = tk.Frame(window)
right_frame.pack(side="left", fill="both", expand=True)

# YouTube Download Section
youtube_frame = tk.Frame(right_frame)
youtube_frame.pack(side="top", fill="x")

youtube_label = tk.Label(youtube_frame, text="Enter YouTube Video URL:")
youtube_label.pack(side="left")

youtube_entry = tk.Entry(youtube_frame)
youtube_entry.pack(side="left", fill="x", expand=True)

# --- Input Field Handling ---
def clear_youtube_entry():
    """Clears the YouTube URL entry field."""
    youtube_entry.delete(0, tk.END)

def select_all_text(event):
    """Selects all text in the YouTube URL entry field."""
    youtube_entry.select_range(0, tk.END)
    youtube_entry.icursor(tk.END)  # Move cursor to the end

youtube_entry.bind("<FocusIn>", select_all_text) 

# download_button = tk.Button(youtube_frame, text="Process", command=lambda: [download_youtube_video(), clear_youtube_entry()])
# download_button.pack(side="left")


# --- Download Progress Bar ---
progress_bar = ttk.Progressbar(
    youtube_frame, orient="horizontal", mode="determinate", length=200
)
progress_bar.pack(side="left", padx=(5, 0)) 

def on_download_progress(stream, chunk, bytes_remaining):
    """Callback function for pytube's download progress."""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = (bytes_downloaded / total_size) * 100
    progress_bar["value"] = percentage_completed
    window.update_idletasks()  # Update the GUI 


download_button = tk.Button(
    youtube_frame,
    text="Process",
    command=lambda: [
        download_youtube_video(),
        clear_youtube_entry(),
    ],
)
download_button.pack(side="left")


# Chat Area 
chat_frame = tk.Frame(right_frame)
chat_frame.pack(side="top", fill="both", expand=True)

chat_text = Text(chat_frame, height=20, width=80)
chat_text.config(state="disabled")
chat_text.pack(fill="both", expand=True)

# User Input
input_field = Text(chat_frame, height=3, width=80)
input_field.pack(fill="x")
input_field.bind("<Return>", send_message) 

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack()



start_new_chat()  # Start the initial chat
window.mainloop()