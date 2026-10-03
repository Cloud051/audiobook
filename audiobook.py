import re
import keyboard
import pyttsx3
from PyPDF2 import PdfReader

is_stopped = False

def stop_audio():
    global is_stopped
    is_stopped = True
    print("\n[Stopping playback...]")

def get_sentences_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    all_sentences = []
    for page_num, page in enumerate(reader.pages):
        raw = page.extract_text()
        if not raw or not raw.strip():
            continue
        # clean lines and split into sentences
        clean = " ".join(raw.split())
        sentences = [
            s.strip() for s in re.split(r"(?<=[.!?])\s+", clean) if s.strip()
        ]
        for s in sentences:
            all_sentences.append((page_num + 1, s))
    return all_sentences

def main():
    global is_stopped

    file_path = input("Enter path to PDF: ").strip().strip('"')

    try:
        sentences = get_sentences_from_pdf(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    if not sentences:
        print("No readable text found.")
        return

    print(f"\nLoaded {len(sentences)} sentences.")
    print("Controls:\n  Press [q] to stop.\n")

    keyboard.add_hotkey("q", stop_audio)

    current_page = None

    for page_num, sentence in sentences:
        if is_stopped:
            break

        if page_num != current_page:
            current_page = page_num
            print(f"\n--- Page {page_num} ---")

        print(f"> {sentence}")

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(sentence)
        engine.runAndWait()
        engine.stop()
        del engine

    keyboard.unhook_all()
    print("\nDone.")

if __name__ == "__main__":
    main()