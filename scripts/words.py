# Время каждого слова в фразах диктора: python words.py ph/*.wav  -> words.json
import sys, json, glob
from faster_whisper import WhisperModel
files = [f for a in sys.argv[1:] for f in glob.glob(a)]
m = WhisperModel('small', device='cpu', compute_type='int8')
out = {}
for f in files:
    segs, _ = m.transcribe(f, language='ru', word_timestamps=True)
    out[f] = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
    print(f, ' '.join(w[0] for w in out[f]))
json.dump(out, open('words.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
