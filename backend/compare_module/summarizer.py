from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")
    def summarize(self, text):
        # Summarize in chunks if text is too long
        if len(text) > 1024:
            text = text[:1024]
        summary = self.summarizer(text, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']
