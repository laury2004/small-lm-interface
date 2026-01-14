import random
import re
from datasets import load_dataset

class LyricModel:
    def __init__(self):
        self.artists_data = {} 
        self.available_artists = []

    def download_and_train(self):
        try:
            ds = load_dataset("m-p-m/italian-lyrics", split="train", streaming=True)
            iterator = iter(ds)
            for _ in range(300):
                row = next(iterator)
                artist = row.get('artist', 'Artista Ignoto').strip()
                lyrics = row.get('lyrics', '').lower()
                if len(lyrics) > 50:
                    if artist not in self.artists_data:
                        self.artists_data[artist] = {"unigrams": {}, "bigrams": {}, "vocab": set()}
                    self._process_text(lyrics, self.artists_data[artist])
            self.available_artists = sorted(list(self.artists_data.keys()))
            if not self.available_artists: self._load_fallback()
        except:
            self._load_fallback()

    def _load_fallback(self):
        fallback_data = {
            "Pop Moderno": "il sole splende alto nel cielo amore mio rimani qui con me stasera non andare via",
            "Rap/Trap": "nella strada non si dorme mai fra la gang corre forte non ci fermi siamo i primi",
            "Cantautore": "camminando lungo il fiume cerco ancora le parole che non ti ho detto mai nel silenzio"
        }
        for artist, text in fallback_data.items():
            self.artists_data[artist] = {"unigrams": {}, "bigrams": {}, "vocab": set()}
            self._process_text(text * 15, self.artists_data[artist])
        self.available_artists = sorted(list(self.artists_data.keys()))

    def _process_text(self, text, model_dict):
        tokens = re.findall(r'\b\w+\b', text)
        model_dict["vocab"].update(tokens)
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i+1]
            model_dict["unigrams"][w1] = model_dict["unigrams"].get(w1, 0) + 1
            model_dict["bigrams"][(w1, w2)] = model_dict["bigrams"].get((w1, w2), 0) + 1

    def generate(self, artist, prompt, length=40, creativity=0.5):
        if artist not in self.artists_data: return "Seleziona un artista."
        model = self.artists_data[artist]
        tokens = re.findall(r'\b\w+\b', prompt.lower())
        
        result = tokens if tokens else [random.choice(list(model["vocab"]))]
        current_word = result[-1]
        vocab_size = len(model["vocab"])

        for i in range(length):
            candidates = list(model["vocab"])
            # La creatività riduce il numero di candidati (più bassa = più coerente, più alta = più pazza)
            sample_size = int(20 + (creativity * 100))
            random_candidates = random.sample(candidates, min(sample_size, vocab_size))
            
            best_word = random.choice(random_candidates)
            max_prob = -1
            
            for next_word in random_candidates:
                c_bigram = model["bigrams"].get((current_word, next_word), 0)
                c_unigram = model["unigrams"].get(current_word, 0)
                prob = (c_bigram + 1) / (c_unigram + vocab_size)
                
                if prob > max_prob:
                    max_prob = prob
                    best_word = next_word
            
            # Aggiungiamo punteggiatura casuale "musicale"
            if i > 0 and i % 6 == 0:
                punct = random.choice([",", "...", " "])
                result[-1] = result[-1] + punct

            result.append(best_word)
            current_word = best_word

        # Formattazione finale: Maiuscola solo all'inizio assoluto
        text = " ".join(result)
        return text.strip().capitalize() + "."

lyric_model = LyricModel()