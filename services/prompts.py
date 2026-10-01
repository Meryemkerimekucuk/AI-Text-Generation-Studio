def create_generation_prompt(
    topic: str,
    text_type: str,
    tone: str,
    length: str,
    conversation_history: str = ""
) -> str:

    return f"""
Sen profesyonel bir içerik yazarı ve metin üretme asistanısın.

Önceki konuşma:
{conversation_history}

Kullanıcının yeni isteği:
{topic}

Metin türü:
{text_type}

Metnin tonu:
{tone}

Metnin uzunluğu:
{length}

Kurallar:
- Metin Türkçe olmalı.
- Metin, seçilen metin türüne uygun hazırlanmalı.
- Seçilen tona uygun bir dil kullanılmalı.
- Kısa seçildiyse yaklaşık 100-150 kelime yaz.
- Orta seçildiyse yaklaşık 250-350 kelime yaz.
- Uzun seçildiyse yaklaşık 500-700 kelime yaz.
- Anlaşılır ve akıcı bir dil kullanılmalı.
- Gereksiz tekrar yapılmamalı.
"""


def create_improvement_prompt(topic: str) -> str:

    return f"""
Sen profesyonel bir metin editörüsün.

Aşağıdaki metni daha anlaşılır, akıcı ve profesyonel
hale getir.

Mevcut metin:
{topic}

Kurallar:
- Metnin ana fikrini koru.
- Gereksiz tekrarları kaldır.
- Yazım ve dil bilgisi hatalarını düzelt.
- Cümleleri daha doğal hale getir.
- Metne gereksiz bilgi ekleme.
- Türkçe yaz.
"""


def create_summary_prompt(
    topic: str,
    summary_length: str
) -> str:

    return f"""
Sen profesyonel bir metin özetleme asistanısın.

Aşağıdaki metni özetle.

Metin:
{topic}

Özet uzunluğu:
{summary_length}

Kurallar:
- Metnin ana fikrini koru.
- Önemli bilgileri kaybetme.
- Gereksiz ayrıntıları çıkar.
- Yeni bilgi ekleme.
- Türkçe yaz.
"""


def create_translation_prompt(
    topic: str,
    target_language: str
) -> str:

    return f"""
Sen profesyonel bir çeviri asistanısın.

Aşağıdaki metni {target_language} diline çevir.

Metin:
{topic}

Kurallar:
- Metnin anlamını koru.
- Doğal ve akıcı bir dil kullan.
- Kelime kelime mekanik çeviri yapma.
- Özel isimleri ve teknik terimleri doğru şekilde koru.
- Sadece çeviriyi ver.
"""


def create_rewrite_prompt(
    topic: str,
    rewrite_style: str
) -> str:

    return f"""
Sen profesyonel bir metin düzenleme asistanısın.

Aşağıdaki metni yeniden yaz.

Mevcut metin:
{topic}

İstenen yazım tarzı:
{rewrite_style}

Kurallar:
- Metnin ana fikrini ve temel bilgilerini koru.
- Metni seçilen yazım tarzına uygun hale getir.
- Gereksiz bilgi ekleme.
- Anlamı değiştirme.
- Türkçe yaz.
- Doğal ve akıcı bir dil kullan.
"""


def create_idea_prompt(
    topic: str,
    platform: str,
    idea_count: int
) -> str:

    return f"""
Sen yaratıcı bir içerik stratejistisin.

Aşağıdaki konu hakkında içerik fikirleri üret.

Konu:
{topic}

Platform:
{platform}

İstenen fikir sayısı:
{idea_count}

Kurallar:
- Her fikir birbirinden farklı olmalı.
- Fikirler yaratıcı ve uygulanabilir olmalı.
- Platformun kullanıcı kitlesine uygun olmalı.
- Her fikri kısa ve anlaşılır şekilde yaz.
- Türkçe yaz.
- Her fikri numaralandır.
"""