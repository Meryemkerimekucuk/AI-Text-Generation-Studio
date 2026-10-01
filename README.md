# 🤖 AI Text Generation Studio

> **Gemini destekli, yapay zekâ tabanlı metin üretme ve metin işleme uygulaması.**

AI Text Generation Studio, kullanıcıların Google Gemini API aracılığıyla farklı türlerde metinler üretmesini, mevcut metinleri dönüştürmesini ve içerik fikirleri oluşturmasını sağlayan yapay zekâ destekli bir web uygulamasıdır.

Uygulama **Python** ve **Streamlit** kullanılarak geliştirilmiştir. Projede kullanıcı sohbetlerinin kalıcı olarak saklanması için **SQLite**, API anahtarının güvenli şekilde yönetilmesi için **`.env`**, farklı AI görevleri için ise ayrı bir **prompt katmanı** kullanılmıştır.

Projenin temel amacı yalnızca bir LLM API'sine istek göndermek değil; **kullanılabilir, modüler ve geliştirilebilir bir AI uygulaması** geliştirmektir.

---

## ✨ Özellikler

### 📝 1. Yeni Metin Oluşturma

Kullanıcı belirlediği konu hakkında sıfırdan yeni bir metin oluşturabilir.

**Metin Türü:**

- Genel Metin
- LinkedIn Gönderisi
- Blog Yazısı
- E-posta
- Sosyal Medya Gönderisi

**Ton:**

- Profesyonel
- Samimi
- Akademik
- Eğlenceli

**Uzunluk:**

- Kısa
- Orta
- Uzun

Girilen parametreler doğrultusunda Gemini API'ye özel bir prompt gönderilir ve oluşturulan metin kullanıcıya gösterilir.

---

### ✏️ 2. Mevcut Metni İyileştirme

Kullanıcı mevcut bir metni uygulamaya girerek yapay zekâdan metni geliştirmesini isteyebilir.

Bu özellik;

- Yazım ve anlatımın geliştirilmesi
- Metnin daha akıcı hale getirilmesi
- Anlatımın iyileştirilmesi
- Daha profesyonel bir ifade oluşturulması

gibi kullanım senaryoları için tasarlanmıştır.

---

### 📌 3. Metin Özetleme

Uzun bir metin Gemini kullanılarak özetlenebilir.

Kullanıcı özet uzunluğunu seçebilir:

- Çok Kısa
- Kısa
- Detaylı

Bu sayede aynı metin için farklı seviyelerde özet oluşturulabilir.

---

### 🌍 4. Metin Çevirme

Uygulama farklı dillere metin çevirisi yapabilir.

Desteklenen hedef diller:

- 🇹🇷 Türkçe
- 🇬🇧 İngilizce
- 🇩🇪 Almanca
- 🇫🇷 Fransızca
- 🇪🇸 İspanyolca

Kullanıcı çevirmek istediği metni girer ve hedef dili seçerek AI destekli çeviri oluşturabilir.

---

### 🔄 5. Metni Yeniden Yazma

Mevcut bir metin farklı bir anlatım biçimine dönüştürülebilir.

Kullanıcı aşağıdaki stillerden birini seçebilir:

- Daha Resmi
- Daha Samimi
- Daha Akademik
- Daha Etkileyici
- Daha Sade

Bu özellik aynı içeriğin farklı hedef kitlelere veya farklı iletişim amaçlarına uyarlanmasını sağlar.

---

### 💡 6. İçerik Fikri Üretme

Kullanıcı belirli bir konu için yapay zekâdan içerik fikirleri oluşturmasını isteyebilir.

Örneğin:

- Sosyal medya içerik fikirleri
- LinkedIn içerik fikirleri
- Blog fikirleri
- Dijital içerik fikirleri

gibi farklı kullanım alanlarında fikir üretilebilir.

---

## 💬 Chat History

Projenin önemli özelliklerinden biri **sohbet geçmişinin yönetilmesidir.**

Kullanıcı:

- ➕ Yeni sohbet oluşturabilir.
- 💬 Önceki sohbetlerini sidebar üzerinden görüntüleyebilir.
- 🔄 Daha önce oluşturulmuş sohbetlere tekrar geçebilir.
- 🗑️ Sohbetleri silebilir.
- 🏷️ Sohbetler otomatik olarak ilk kullanıcı mesajından isimlendirilebilir.
- 🔢 Aynı isimde sohbetler oluşturulduğunda otomatik olarak numaralandırılabilir.

Örneğin:

```text
Python öğrenmek istiyorum
Python öğrenmek istiyorum (2)
Python öğrenmek istiyorum (3)
```

şeklinde isimlendirme yapılabilir.

---

## 🗄️ SQLite ile Kalıcı Sohbet Saklama

Projenin ilk aşamalarında sohbetler yalnızca Streamlit session state içerisinde tutulurken, daha sonra **SQLite veritabanı entegrasyonu** eklenmiştir.

Bu sayede uygulama kapatılıp yeniden açıldığında sohbet geçmişi kaybolmaz.

Veritabanında iki temel tablo bulunmaktadır.

### `chats`

Sohbet bilgilerini saklar.

| Alan | Açıklama |
|---|---|
| `id` | Sohbet kimliği |
| `name` | Sohbet adı |
| `created_at` | Oluşturulma zamanı |

### `messages`

Sohbet içerisindeki kullanıcı ve AI mesajlarını saklar.

| Alan | Açıklama |
|---|---|
| `id` | Mesaj kimliği |
| `chat_id` | Bağlı olduğu sohbet |
| `role` | Mesajın kullanıcı veya AI tarafından gönderildiği |
| `content` | Mesaj içeriği |
| `created_at` | Oluşturulma zamanı |

Temel ilişki:

```text
Chats
  │
  └── Messages
        ├── user
        ├── assistant
        ├── user
        └── assistant
```

Bu yapı sayesinde her mesaj belirli bir sohbet ile ilişkilendirilir.

---

## 🧠 Google Gemini API

Uygulamanın AI katmanında **Google Gemini API** kullanılmaktadır.

API bağlantısı `services/gemini_service.py` içerisinde ayrı bir servis katmanında tutulmuştur.

Temel çalışma akışı:

```text
User Input
    ↓
Prompt oluşturma
    ↓
Gemini Service
    ↓
Google Gemini API
    ↓
AI Response
    ↓
Streamlit UI
```

Gemini API'ye yapılan isteklerde model davranışını kontrol etmek için iki önemli parametre kullanılmaktadır.

### Temperature

Modelin cevap üretimindeki yaratıcılık ve değişkenlik seviyesini kontrol eder.

Uygulamada:

```text
0.0 → 1.0
```

arasında ayarlanabilir.

Varsayılan değer:

```text
0.7
```

### Max Output Tokens

Model tarafından üretilebilecek maksimum çıktı uzunluğunu kontrol eder.

Uygulamada:

```text
200 → 2000
```

arasında ayarlanabilir.

Varsayılan değer:

```text
1000
```

---

## 🧩 Prompt Engineering

Projede promptlar doğrudan `app.py` içerisine yazılmak yerine ayrı bir dosyada tutulmuştur.

```text
services/
├── gemini_service.py
└── prompts.py
```

`prompts.py` içerisinde farklı AI görevleri için ayrı prompt fonksiyonları bulunmaktadır:

```python
create_generation_prompt()
create_improvement_prompt()
create_summary_prompt()
create_translation_prompt()
create_rewrite_prompt()
create_idea_prompt()
```

Bu yaklaşım sayesinde:

- Kod tekrarının azaltılması
- Promptların merkezi olarak yönetilmesi
- `app.py` dosyasının daha düzenli olması
- Yeni AI özelliklerinin daha kolay eklenebilmesi

amaçlanmıştır.

---

## 🏗️ Proje Mimarisi

Proje basit fakat modüler bir yapıda tasarlanmıştır.

```text
AI-Text-Generation-Studio/
│
├── app.py
│
├── database.py
│
├── services/
│   ├── gemini_service.py
│   └── prompts.py
│
├── .env.example
├── .gitignore
├── requirements.txt
│
└── chats.db
```

### `app.py`

Uygulamanın ana Streamlit dosyasıdır.

Şunları yönetir:

- Kullanıcı arayüzü
- AI özelliklerinin seçimi
- Kullanıcı girdileri
- Model ayarları
- Sohbet yönetimi
- Gemini servisinin çağrılması
- AI çıktılarının gösterilmesi

### `database.py`

SQLite veritabanı işlemlerinden sorumludur.

Temel işlemler:

```python
init_database()
create_chat()
get_all_chats()
get_messages()
add_message()
rename_chat()
delete_chat()
```

Bu yapı sayesinde veritabanı işlemleri ana uygulama kodundan ayrılmıştır.

### `services/gemini_service.py`

Gemini API ile iletişim sağlayan servis katmanıdır.

Bu dosyada:

- API key yükleme
- Gemini client oluşturma
- Metin üretme
- Hata yakalama

işlemleri gerçekleştirilir.

Ayrıca API hatalarının uygulamayı doğrudan durdurmasını önlemek amacıyla güvenli bir wrapper kullanılmaktadır:

```python
safe_generate_text()
```

### `services/prompts.py`

AI görevleri için kullanılan promptların bulunduğu katmandır.

Her AI özelliği için farklı bir prompt şablonu oluşturulmuştur.

Bu sayede uygulamanın **prompt engineering** kısmı UI kodundan ayrılmıştır.

---

## 🔐 API Key Güvenliği

Google Gemini API anahtarı doğrudan Python kodunun içerisine yazılmamıştır.

Bunun yerine `.env` dosyası kullanılmaktadır.

Örnek:

```env
google_apikey=YOUR_GOOGLE_GEMINI_API_KEY
```

Python tarafında `python-dotenv` kullanılarak bu değer yüklenmektedir:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("google_apikey")
```

Gerçek `.env` dosyası `.gitignore` içerisine eklenmiştir:

```gitignore
.env
.venv/
__pycache__/
chats.db
```

Bu nedenle API anahtarı GitHub repository'sine gönderilmez.

Ayrıca projede kullanıcıların kendi API anahtarlarını ekleyebilmesi için `.env.example` dosyası bulunmaktadır.

> ⚠️ Gerçek API anahtarınızı GitHub'a yüklemeyin.

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım Alanı |
|---|---|
| 🐍 Python | Ana programlama dili |
| 🎈 Streamlit | Web arayüzü |
| 🤖 Google Gemini API | LLM / AI işlemleri |
| 🗄️ SQLite | Sohbet verilerinin saklanması |
| 🔐 python-dotenv | Environment variable yönetimi |
| 📦 google-genai | Gemini API entegrasyonu |
| 🌱 Git | Versiyon kontrolü |
| 🐙 GitHub | Kod ve proje yönetimi |

---

## 📦 Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için öncelikle repository'yi klonlayın:

```bash
git clone https://github.com/Meryemkerimekucuk/AI-Text-Generation-Studio.git
```

Proje klasörüne geçin:

```bash
cd AI-Text-Generation-Studio
```

### 1. Virtual Environment Oluşturma

Python virtual environment oluşturabilirsiniz:

```bash
python -m venv .venv
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 2. Gerekli Paketleri Kurma

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

Daha sonra `.env` dosyasındaki:

```env
google_apikey=YOUR_GOOGLE_GEMINI_API_KEY
```

alanına kendi Gemini API anahtarınızı ekleyin.

> ⚠️ `.env` dosyanızı GitHub'a yüklemeyin.

### 4. Uygulamayı Çalıştırma

Streamlit uygulamasını başlatmak için:

```bash
streamlit run app.py
```

Uygulama tarayıcıda açılacaktır.

---

## 🖥️ Kullanım

Uygulama açıldığında kullanıcı ana ekrandan yapmak istediği işlemi seçebilir.

```text
Ne yapmak istiyorsunuz?

[ Yeni Metin Oluştur ]
[ Mevcut Metni İyileştir ]
[ Metni Özetle ]
[ Metni Çevir ]
[ Metni Yeniden Yaz ]
[ İçerik Fikri Üret ]
```

AI özelliklerinden biri seçildikten sonra kullanıcı gerekli bilgileri girer.

Model ayarlarından:

- Temperature
- Max Output Tokens

değerleri değiştirilebilir.

Ardından uygulama Gemini API'ye istek gönderir ve AI tarafından oluşturulan sonucu kullanıcıya gösterir.

---

## 🔄 Uygulamanın Çalışma Akışı

Genel sistem akışı:

```text
                    USER
                      │
                      ▼
             Streamlit Interface
                      │
                      ▼
              Feature Selection
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
     User Input             Model Settings
          │                       │
          └───────────┬───────────┘
                      ▼
                Prompt Layer
                 prompts.py
                      │
                      ▼
              Gemini Service
             gemini_service.py
                      │
                      ▼
             Google Gemini API
                      │
                      ▼
                AI Response
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
        Streamlit UI       SQLite DB
                            chats.db
```

Bu mimari sayesinde kullanıcı arayüzü, prompt yönetimi, AI servisi ve veritabanı işlemleri birbirinden ayrılmıştır.

---

## 🧪 Hata Yönetimi

Gemini API çağrılarında oluşabilecek hataların uygulamayı doğrudan sonlandırmaması için güvenli bir API çağrı fonksiyonu kullanılmaktadır.

```python
safe_generate_text()
```

API çağrısı sırasında bir hata meydana geldiğinde hata yakalanır ve kullanıcıya uygun bir hata mesajı gösterilir.

Örneğin:

```text
❌ Metin oluşturulurken bir hata oluştu.
Lütfen tekrar deneyin.
```

Bu yaklaşım kullanıcı deneyimini iyileştirmeyi ve API kaynaklı hataların kontrollü şekilde yönetilmesini amaçlamaktadır.

---

## 📁 GitHub'da Neden Bazı Dosyalar Yok?

Projede bazı dosyalar özellikle repository'ye dahil edilmemiştir.

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
chats.db
```

### `.env`

API anahtarını içerdiği için GitHub'a gönderilmez.

### `.venv`

Python virtual environment dosyaları projeye dahil edilmez.

### `__pycache__`

Python tarafından oluşturulan geçici dosyalardır.

### `chats.db`

Kullanıcıya ait lokal sohbet geçmişini içerdiği için repository'ye dahil edilmez.

Bu dosya uygulama çalıştırıldığında lokal olarak oluşturulur.

---

## 🚀 Gelecek Geliştirmeler

Projenin mevcut versiyonu temel olarak **text generation ve text processing** üzerine kurulmuştur.

Gelecek versiyonlarda aşağıdaki özelliklerin eklenmesi planlanmaktadır.

### 🎙️ Audio Generation

AI destekli:

- Metinden sese dönüştürme
- Sesli içerik oluşturma
- AI voice özellikleri

eklenebilir.

### 🖼️ Image Generation

Metin promptlarından görsel üretme özelliği eklenebilir.

### 🤖 Multimodal AI

Metin dışında:

- Görsel
- Ses
- Doküman

gibi farklı veri türleriyle çalışabilen multimodal AI özellikleri geliştirilebilir.

### 💾 Gelişmiş Chat Management

İlerleyen versiyonlarda:

- Sohbet arama
- Sohbet filtreleme
- Sohbet dışa aktarma
- Sohbet yeniden adlandırma
- Favori sohbetler

gibi özellikler eklenebilir.

### 🌐 Deployment

Uygulama ilerleyen aşamalarda cloud ortamına deploy edilerek herkesin erişebileceği bir web uygulamasına dönüştürülebilir.

---

## 🎯 Projenin Öğrenme Amaçları

Bu proje geliştirilirken yalnızca bir AI API'sinin kullanılması değil, aynı zamanda gerçek bir uygulamanın temel bileşenlerinin bir araya getirilmesi hedeflenmiştir.

Proje kapsamında:

- Python ile uygulama geliştirme
- Streamlit ile web arayüzü oluşturma
- LLM API entegrasyonu
- Prompt engineering
- Session state yönetimi
- SQLite veritabanı kullanımı
- CRUD işlemleri
- Environment variable yönetimi
- API hata yönetimi
- Modüler Python yapısı
- Git & GitHub kullanımı

üzerinde çalışılmıştır.

---

## 📌 Project Status

**Current Version:** `v1.0`

The current version focuses on AI-powered text generation and text processing.

More multimodal AI capabilities are planned for future versions.

---

## 👩‍💻 Developer

**Meryem Kerime Küçük**

Management Information Systems Graduate

### Interests

- Data Science
- Artificial Intelligence
- Big Data
- Data Analytics
- Python
- Generative AI

---

## ⭐ Future Development

This project will continue to evolve with new AI capabilities, multimodal features and improved user experience.

---

⭐ **If you find this project useful, feel free to explore the repository and follow the project for future updates.**
