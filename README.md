# AI Security Fundamentals Lab

Python ile embedding, cosine similarity, semantic search ve RAG context hazırlama temellerini öğrenmek için küçük bir laboratuvar. Açıklamalar Türkçe, model ve örnek sorgular İngilizce. API anahtarı veya ücretli servis gerekmez.

## Akış

```text
Metin → tokenizer/model → embedding vektörü
Soru + belge vektörleri → cosine similarity → en yakın paragraflar
Paragraflar + soru → RAG prompt önizlemesi → [gelecek adım: LLM cevabı]
```

Bu sürüm gerçek embedding ve retrieval çalıştırır. `--rag` kaynaklı bir prompt hazırlar; LLM cevabı üretmez. Böylece retrieval ve generation ayrımını görebilirsin.

## 1. VS Code ve proje klasörü

Windows PowerShell terminalinde:

```powershell
cd "$HOME\ai-security-fundamentals-lab"
code .
```

VS Code'da **Terminal → New Terminal** aç. `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv\Scripts\python.exe` seç (Python eklentisi kuruluysa). Dosyaları soldaki Explorer'da açabilirsin.

## 2. Virtual environment ve requirements

Yeni klon için Python 3.12 kullan:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

`.venv` paketleri bu projeye ayırır. `requirements.txt` doğrudan bağımlılığı, `requirements-lock.txt` doğrulanan ortamın tüm paket sürümlerini kaydeder. Linux/macOS için interpreter yolu `.venv/bin/python` olur. Aktivasyon zorunlu değildir; yukarıdaki yol doğru Python'u açıkça seçer.

## 3. Embedding benzerliği

Önce tahmin et: firewall cümlesi hangi cümleye daha yakın olacak?

```powershell
.\.venv\Scripts\python.exe -m lab.embedding_similarity
```

Model `sentence-transformers/all-MiniLM-L6-v2`, üç metni 384 boyutlu vektörlere çevirir. Normalize edilmiş vektörlerin dot product'ı cosine similarity verir. Sonuç bir olasılık değildir; `0.8`, yüzde 80 doğruluk demek değildir.

İlk çalıştırma internetten model indirir; sonraki çalıştırmalar önbelleği kullanır. Paketler ve model birkaç yüz MB disk alanı kullanabilir. Model yüklenirken indirme mesajları normaldir.

Doğrulanan örnek çıktı (ortama/model sürümüne göre küçük farklar olabilir):

```text
Embedding shape: (3, 384)
1 vs 2: cosine=0.6039
1 vs 3: cosine=0.0393
2 vs 3: cosine=0.0336
```

## 4. Küçük semantic search

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "How can I prevent account takeover?"
```

Belgeler boş satırlardan paragraflara bölünür (chunking). Soru ve paragraflar aynı modelle kodlanır; en yakın iki paragraf skor ve kaynak kimliğiyle gösterilir. Küçük corpus bellekte tutulur; vector database gerekmez.

## 5. RAG context ve güven sınırı

```powershell
.\.venv\Scripts\python.exe -m lab.semantic_search "What is prompt injection?" --rag
.\.venv\Scripts\python.exe -m lab.semantic_search "How does a firewall filter traffic?" --top-k 3 --rag --include-attack
```

İkinci komut kasıtlı zararlı bir örnek belge ekler. Skoru yüksek bir belgenin güvenilir olmasının gerekmediğini incele. Önizleme tek metindir; gerçek LLM entegrasyonunda system/user rolleri ayrı mesajlarla gönderilmeli ve yetkiler uygulama tarafından sınırlandırılmalı. Ayrıntılar: [security-notes.md](security-notes.md).

## Yapı

```text
lab/                       # ortak yardımcılar ve iki çalıştırılabilir örnek
data/knowledge/            # herkese açık, sentetik bilgi paragrafları
data/attack/               # yalnızca opt-in injection örneği
.vscode/settings.json     # proje interpreter tercihi
requirements*.txt         # bağımlılıklar
security-notes.md          # riskler ve güven sınırları
```

## 6. Git ve GitHub

İlk oluşturma akışı:

```powershell
git init -b main
git add .
git commit -m "Add AI security fundamentals learning lab"
gh repo create ai-security-fundamentals-lab --public --source . --remote origin --push
```

Repo zaten kurulmuşsa bunları tekrar çalıştırma. Kendi sonraki değişikliklerin için:

```powershell
git status
git diff
git add lab/embedding_similarity.py
git commit -m "Explore additional sentence similarities"
git push
```

Commit yerel bir kayıttır; push commit'leri GitHub'a gönderir. `.venv`, cache ve `.env` repoya girmez. Dosya eklemeden önce diff'i oku.

## Öğrenme alıştırmaları

Doğrulama: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
Gerçek modelle boyut/benzerlik, ilgili kaynağın bulunması ve prompt kaynak etiketleri kontrol edilir. Bu kontroller injection dayanıklılığı kanıtı değildir.

1. Banana cümlesini başka bir network cümlesiyle değiştir; çalıştırmadan skoru tahmin et.
2. `data/knowledge/` içine yeni bir Markdown belgesi ekle; farklı kelimelerle ilgili bir soru sor.
3. Corpus dışı bir yemek tarifi sor; en yakın sonucun yine döndüğünü gözlemle.
4. `--top-k 1` ve `--top-k 3` ile context miktarını karşılaştır.
5. Injection örneğini incele: bir belge hangi noktada talimat gibi davranmaya çalışıyor?

Kaynak: [Sentence Transformers resmi quickstart](https://www.sbert.net/docs/quickstart.html).
