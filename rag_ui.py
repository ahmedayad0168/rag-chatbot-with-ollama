import tkinter as tk
from tkinter import scrolledtext
import threading
from query_data import query_rag

chat_history = []

def ask_question():
    user_input = question_entry.get("1.0", "end-1c").strip()
    if not user_input:
        return

    update_chat_log("You", user_input, "blue_text")
    question_entry.delete("1.0", "end")
    
    update_chat_log("Assistant", "Thinking...", "gray_text", tag= "status")
    
    threading.Thread(target= process_rag, args= (user_input,), daemon= True).start()

def process_rag(user_input):
    try:
        answer, sources_list = query_rag(user_input, chat_history)
        
        if sources_list:
            source_display = "\n\nSources:\n" + "\n".join([f"- {s}" for s in sources_list])
        else:
            source_display = ""
            
        full_message = f"{answer}{source_display}"
        root.after(0, finalize_response, answer, full_message)
    except Exception as e:
        root.after(0, finalize_response, "Error", f"Failed to get response: {str(e)}")

def finalize_response(raw_answer, full_display):
    chat_log.config(state= "normal")
    chat_log.delete("status.first", "status.last")
    chat_log.config(state= "disabled")
    
    update_chat_log("Assistant", full_display, "black_text")
    
    chat_history.append({"role": "user", "content": raw_answer})
    if len(chat_history) > 10:
        chat_history.pop(0)

def update_chat_log(sender, message, color_tag, tag=None):
    chat_log.config(state="normal")
    idx = "end"
    chat_log.insert(idx, f"\n {sender}: \n", ("bold", color_tag))
    
    if tag:
        chat_log.insert("end", f" {message} \n", (tag,))
    else:
        chat_log.insert("end", f" {message} \n")
        
    chat_log.insert("end", "-" * 60 + "\n")
    chat_log.config(state="disabled")
    chat_log.yview("end")

root = tk.Tk()
root.title("RAG & SQL Agent")
root.geometry("800x600")

chat_log = scrolledtext.ScrolledText(root, wrap= "word", state= "disabled", font= ("Segoe UI", 11))
chat_log.tag_configure("bold", font= ("Segoe UI", 11, "bold"))
chat_log.tag_configure("blue_text", foreground= "#0078d4")
chat_log.tag_configure("gray_text", foreground= "gray")
chat_log.tag_configure("status")
chat_log.pack(padx= 20, pady= 20, fill= "both", expand= True)

input_frame = tk.Frame(root)
input_frame.pack(fill= "x", side= "bottom", padx= 20, pady= 10)

question_entry = tk.Text(input_frame, height= 3, font= ("Segoe UI", 11))
question_entry.pack(side= "left", fill= "x", expand= True, padx= (0, 10))
question_entry.bind("<Return>", lambda e: ask_question() or "break") 

btn = tk.Button(input_frame, text= "Send", command= ask_question, bg= "#0078d4", fg= "white", width= 10)
btn.pack(side= "right", fill= "y")

root.mainloop()