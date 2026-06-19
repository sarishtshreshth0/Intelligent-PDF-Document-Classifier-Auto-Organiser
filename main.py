import os
import time
import shutil
import pickle
import pdfplumber

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ===========================
# Load Model and Vectorizer
# ===========================

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


# ===========================
# Classification Function
# ===========================

def classification(path):

    try:

        text = ""

        with pdfplumber.open(path) as pdf:

            # First 15 pages enough
            for page in pdf.pages[:15]:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + " "

        if len(text.strip()) == 0:
            return "other"

        vector = vectorizer.transform([text])

        prediction = model.predict(vector)[0]

        print(f"Predicted Category: {prediction}")

        return prediction

    except Exception as e:

        print("Classification Error:", e)

        return "other"


# ===========================
# Watchdog Handler
# ===========================

class MyHandler(FileSystemEventHandler):

    def on_moved(self, event):

        if event.is_directory:
            return

        print("\nFROM :", event.src_path)
        print("TO   :", event.dest_path)

        # Process only PDFs
        if not event.dest_path.lower().endswith(".pdf"):
            return

        # Wait until browser finishes download
        time.sleep(2)

        if not os.path.exists(event.dest_path):
            print("File does not exist")
            return

        try:

            category = classification(event.dest_path)

            destination_folder = os.path.join(
                r"C:\Users\JIT DAS\Downloads",
                category
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            destination_file = os.path.join(
                destination_folder,
                os.path.basename(event.dest_path)
            )

            shutil.move(
                event.dest_path,
                destination_file
            )

            print(
                f"Moved Successfully -> {destination_file}"
            )

        except Exception as e:

            print("Move Error:", e)

    def on_deleted(self, event):

        if not event.is_directory:
            print("Deleted:", event.src_path)


# ===========================
# Start Observer
# ===========================

DOWNLOAD_PATH = r"C:\Users\JIT DAS\Downloads"

observer = Observer()

observer.schedule(
    MyHandler(),
    path=DOWNLOAD_PATH,
    recursive=False
)

observer.start()

print("Watching Downloads Folder...")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()
