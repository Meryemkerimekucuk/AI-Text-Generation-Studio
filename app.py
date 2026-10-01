import streamlit as st

from services.gemini_service import safe_generate_text

from services.prompts import (
    create_generation_prompt,
    create_improvement_prompt,
    create_summary_prompt,
    create_translation_prompt,
    create_rewrite_prompt,
    create_idea_prompt,
)


from database import (
    init_database,
    create_chat,
    get_all_chats,
    get_messages,
    add_message,
    rename_chat,
    delete_chat
)


# DATABASE
init_database()


# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_ids" not in st.session_state:
    st.session_state.chat_ids = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


# DATABASE'DEN SOHBETLERİ YÜKLE

if not st.session_state.chats:

    database_chats = get_all_chats()

    for chat in database_chats:

        chat_name = chat["name"]
        chat_id = chat["id"]

        st.session_state.chats[chat_name] = []
        st.session_state.chat_ids[chat_name] = chat_id


# HİÇ SOHBET YOKSA İLK SOHBETİ OLUŞTUR


if not st.session_state.chats:

    chat_id = create_chat("Yeni Sohbet")

    st.session_state.chats["Yeni Sohbet"] = []

    st.session_state.chat_ids["Yeni Sohbet"] = chat_id

    st.session_state.current_chat = "Yeni Sohbet"

    st.session_state.messages = []


# AKTİF SOHBETİ YÜKLE

if st.session_state.current_chat is None:

    first_chat = next(iter(st.session_state.chats))

    st.session_state.current_chat = first_chat


chat_id = st.session_state.chat_ids[st.session_state.current_chat]

database_messages = get_messages(chat_id)

st.session_state.messages = [
    {
        "role": message["role"],
        "content": message["content"]
    }
    for message in database_messages
]

# CHAT KAYDETME FONKSİYONU

# CHAT KAYDETME

def save_to_chat(role, content):

    current_chat = st.session_state.current_chat

    chat_id = st.session_state.chat_ids[current_chat]

    # Session state'e ekle
    st.session_state.messages.append(
        {"role": role,"content": content})

    # Database'e ekle
    add_message(chat_id,role,content)

    # İlk kullanıcı mesajı sohbet adı olsun
    if role == "user":

        user_messages = [
            message["content"]
            for message in st.session_state.messages
            if message["role"] == "user"
        ]

        if len(user_messages) == 1:

            old_chat_name = current_chat

            new_chat_name = user_messages[0][:40]

            base_name = new_chat_name
            counter = 2

            while (
                new_chat_name in st.session_state.chats
                and new_chat_name != old_chat_name
            ):

                new_chat_name = (f"{base_name} ({counter})")

                counter += 1

            # Database'de ismi değiştir
            rename_chat(chat_id,new_chat_name)

            # Session state'i güncelle
            st.session_state.chats[new_chat_name] = st.session_state.chats.pop(old_chat_name)

            st.session_state.chat_ids[new_chat_name] = st.session_state.chat_ids.pop(old_chat_name)

            st.session_state.current_chat = (new_chat_name)


# SIDEBAR

with st.sidebar:

    st.title("✨ AI Text Assistant")

    st.write("LLM destekli metin işleme ve üretim uygulaması.")

    st.divider()


    
    # YENİ SOHBET
  

    if st.button("➕ Yeni Sohbet",use_container_width=True):

        chat_number = (len(st.session_state.chats) + 1)

        chat_name = (f"Yeni Sohbet {chat_number}")

        chat_id = create_chat(chat_name)

        st.session_state.chats[chat_name] = []

        st.session_state.chat_ids[chat_name] = chat_id

        st.session_state.current_chat = (chat_name)

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # ÖZELLİKLER

    st.subheader("🚀 Özellikler")

    st.write("📝 Metin oluşturma")
    st.write("✏️ Metin iyileştirme")
    st.write("📌 Metin özetleme")
    st.write("🌍 Metin çevirme")
    st.write("🔄 Metin yeniden yazma")
    st.write("💡 İçerik fikri üretme")


    st.divider()


    # CHAT HISTORY

    st.subheader("💬 Chat History")

    st.divider()

    st.subheader("🗂️ Sohbetler")


    # SADECE BİR TANE SOHBET DÖNGÜSÜ VAR
    for chat_name in list(st.session_state.chats.keys()):

        chat_id = st.session_state.chat_ids[chat_name]

        col1, col2 = st.columns([6, 1],vertical_alignment="center")


        # SOHBETE GİT

        with col1:

            if st.button(
                f"💬 {chat_name}",
                key=f"open_chat_{chat_id}",
                use_container_width=True
            ):

                st.session_state.current_chat = (chat_name)

                database_messages = get_messages(chat_id)

                st.session_state.messages = [
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                    for message in database_messages
                ]

                st.rerun()


        # SOHBETİ SİL
        

        with col2:

            if st.button("🗑️",key=f"delete_chat_{chat_id}"):

                delete_chat(chat_id)

                del st.session_state.chats[chat_name]

                del st.session_state.chat_ids[chat_name]


                # Silinen sohbet aktif sohbetse
                if (st.session_state.current_chat == chat_name):

                    if st.session_state.chats:

                        new_chat_name = next(iter(st.session_state.chats))

                        st.session_state.current_chat = (new_chat_name)

                        new_chat_id = (st.session_state.chat_ids[new_chat_name])

                        database_messages = (get_messages(new_chat_id))

                        st.session_state.messages = [
                            {
                                "role": message["role"],
                                "content": message["content"]
                            }
                            for message in database_messages
                        ]

                    else:

                        new_chat_id = create_chat("Yeni Sohbet")

                        st.session_state.chats["Yeni Sohbet"] = []

                        st.session_state.chat_ids["Yeni Sohbet"] = new_chat_id

                        st.session_state.current_chat = ("Yeni Sohbet")

                        st.session_state.messages = []


                st.rerun()


    st.divider()

    st.caption(
        "Powered by Google Gemini"
    )

# ANA SAYFA

st.title("✨ AI Text Assistant")

st.markdown("### Yapay zekâ ile metin üretin ve dönüştürün.")

st.caption("Gemini destekli yapay zekâ metin asistanı")


st.divider()


# MODEL AYARLARI

st.subheader("⚙️ Model Ayarları")


temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)


max_output_tokens = st.slider(
    "Max Output Tokens",
    min_value=200,
    max_value=2000,
    value=1000,
    step=100
)


# MOD SEÇİMİ


mode = st.radio(
    "Ne yapmak istiyorsunuz?",
    [
        "Yeni Metin Oluştur",
        "Mevcut Metni İyileştir",
        "Metni Özetle",
        "Metni Çevir",
        "Metni Yeniden Yaz",
        "İçerik Fikri Üret"
    ],
    horizontal=True
)


# 1. YENİ METİN OLUŞTUR

if mode == "Yeni Metin Oluştur":

    topic = st.text_area("Ne hakkında bir metin oluşturmak istiyorsunuz?")


    text_type = st.selectbox(
        "Metin türünü seçin:",
        [
            "Genel Metin",
            "LinkedIn Gönderisi",
            "Blog Yazısı",
            "E-posta",
            "Sosyal Medya Gönderisi"
        ]
    )


    tone = st.selectbox(
        "Metnin tonunu seçin:",
        [
            "Profesyonel",
            "Samimi",
            "Akademik",
            "Eğlenceli"
        ]
    )


    length = st.selectbox(
        "Metin uzunluğunu seçin:",
        [
            "Kısa",
            "Orta",
            "Uzun"
        ]
    )


    generate_button = st.button("✨ Metin Oluştur")


    if generate_button:

        if not topic.strip():

            st.warning("Lütfen bir konu girin.")

        else:

            # Kullanıcı mesajını kaydet
            save_to_chat("user",topic)


            # Konuşma geçmişini oluştur
            conversation_history = ""


            for message in st.session_state.messages:

                conversation_history += (
                    f"{message['role']}: "
                    f"{message['content']}\n"
                )


            # Prompt oluştur
            prompt = create_generation_prompt(
                topic=topic,
                text_type=text_type,
                tone=tone,
                length=length,
                conversation_history=conversation_history
            )


            # Gemini
            with st.spinner("✨ Gemini yanıt oluşturuyor..."):

                    response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("assistant",response)


                st.subheader("✨ Oluşturulan Metin")

                st.write(response)


            else:

                st.error(
                    "❌ Metin oluşturulurken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )


# 2. METNİ İYİLEŞTİR

elif mode == "Mevcut Metni İyileştir":

    topic = st.text_area("İyileştirmek istediğiniz metni girin:")


    improve_button = st.button("✨ Metni İyileştir")


    if improve_button:

        if not topic.strip():

            st.warning("Lütfen bir metin girin.")

        else:

            prompt = create_improvement_prompt(topic)


            with st.spinner("✨ Gemini metni iyileştiriyor..."):

                response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("user",topic)

                save_to_chat("assistant",response)


                st.subheader("✨ İyileştirilmiş Metin")

                st.write(response)


            else:

                st.error(
                    "❌ Metin iyileştirilirken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )


# 3. METNİ ÖZETLE

elif mode == "Metni Özetle":

    topic = st.text_area("Özetlemek istediğiniz metni girin:")


    summary_length = st.selectbox(
        "Özet uzunluğunu seçin:",
        [
            "Çok Kısa",
            "Kısa",
            "Detaylı"
        ]
    )


    summarize_button = st.button("✨ Metni Özetle")


    if summarize_button:

        if not topic.strip():

            st.warning("Lütfen özetlemek istediğiniz metni girin.")

        else:

            prompt = create_summary_prompt(
                topic=topic,
                summary_length=summary_length
            )


            with st.spinner("✨ Gemini metni özetliyor..."):

                response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("user",topic)

                save_to_chat("assistant",response)


                st.subheader("✨ Özet")

                st.write(response)


            else:

                st.error(
                    "❌ Metin özetlenirken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )


# 4. METNİ ÇEVİR

elif mode == "Metni Çevir":

    topic = st.text_area("Çevirmek istediğiniz metni girin:")


    target_language = st.selectbox(
        "Hedef dili seçin:",
        [
            "İngilizce",
            "Türkçe",
            "Almanca",
            "Fransızca",
            "İspanyolca"
        ]
    )


    translate_button = st.button("🌍 Metni Çevir")


    if translate_button:

        if not topic.strip():

            st.warning("Lütfen çevirmek istediğiniz metni girin.")

        else:

            prompt = create_translation_prompt(
                topic=topic,
                target_language=target_language
            )


            with st.spinner("🌍 Gemini metni çeviriyor..."):

                response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("user",topic)

                save_to_chat("assistant",response)


                st.subheader("✨ Çeviri")

                st.write(response)


            else:

                st.error(
                    "❌ Metin çevrilirken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )


# 5. METNİ YENİDEN YAZ

elif mode == "Metni Yeniden Yaz":

    topic = st.text_area("Yeniden yazmak istediğiniz metni girin:")


    rewrite_style = st.selectbox(
        "Metnin nasıl yeniden yazılmasını istiyorsunuz?",
        [
            "Daha Resmi",
            "Daha Samimi",
            "Daha Akademik",
            "Daha Etkileyici",
            "Daha Sade"
        ]
    )


    rewrite_button = st.button("✨ Metni Yeniden Yaz")


    if rewrite_button:

        if not topic.strip():

            st.warning("Lütfen yeniden yazmak istediğiniz metni girin.")

        else:

            prompt = create_rewrite_prompt(topic=topic,rewrite_style=rewrite_style)


            with st.spinner("✨ Gemini metni yeniden yazıyor..."):

                response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("user",topic)

                save_to_chat("assistant",response)


                st.subheader("✨ Yeniden Yazılmış Metin")

                st.write(response)


            else:

                st.error(
                    "❌ Metin yeniden yazılırken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )


# 6. İÇERİK FİKRİ ÜRET

elif mode == "İçerik Fikri Üret":

    topic = st.text_input("Hangi konuda içerik fikri istiyorsunuz?")


    platform = st.selectbox(
        "İçeriğin yayınlanacağı platform:",
        [
            "LinkedIn",
            "Instagram",
            "Blog",
            "X"
        ]
    )


    idea_count = st.selectbox(
        "Kaç fikir üretilecek?",
        [
            5,
            10,
            15
        ]
    )


    idea_button = st.button("💡 Fikir Üret")


    if idea_button:

        if not topic.strip():

            st.warning("Lütfen bir konu girin.")

        else:

            prompt = create_idea_prompt(
                topic=topic,
                platform=platform,
                idea_count=idea_count
            )


            with st.spinner("💡 İçerik fikirleri oluşturuluyor..."):

                response = safe_generate_text(
                    prompt,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )


            if response:

                save_to_chat("user",topic)

                save_to_chat("assistant",response)


                st.subheader("💡 İçerik Fikirleri")

                st.write(response)


            else:

                st.error(
                    "❌ İçerik fikirleri oluşturulurken bir hata oluştu. "
                    "Lütfen tekrar deneyin."
                )