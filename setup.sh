#!/bin/bash

# Warna
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}Mulai proses setup ModCore Bot...${NC}"

# Update & Upgrade sistem
echo -e "${CYAN}Update & Upgrade package...${NC}"
# Menggunakan && untuk memastikan perintah sebelumnya berhasil sebelum melanjutkan
# Perintah ini mungkin memerlukan sudo di beberapa sistem
apt update && apt upgrade -y || sudo apt update && sudo apt upgrade -y

# Install Python & Pip
echo -e "${CYAN}Pastikan Python & Pip terinstall...${NC}"
apt install python3 python3-pip -y || sudo apt install python3 python3-pip -y

# Install dependency Python
echo -e "${CYYAN}Install dependency Python...${NC}"
pip install -r requirements.txt

# Setup konfigurasi .env
echo -e "${CYAN}Setup konfigurasi .env...${NC}"
if [ ! -f ".env" ]; then
    echo "API_ID=" > .env
    echo "API_HASH=" >> .env
    echo "BOT_TOKEN=" >> .env
    echo "USERNAME=" >> .env

    # Pilihan AI
    echo -e "${CYAN}Mau aktifkan AI? (y/n)${NC}"
    read ai_option

    if [ "$ai_option" == "y" ] || [ "$ai_option" == "Y" ]; then
        echo "USE_AI=True" >> .env
        echo -e "${CYAN}Pilih Provider AI: (openrouter / ollama)${NC}"
        read ai_provider
        ai_provider=$(echo "$ai_provider" | tr '[:upper:]' '[:lower:]') # Convert to lowercase
        echo "AI_PROVIDER=$ai_provider" >> .env

        if [ "$ai_provider" == "openrouter" ]; then
            echo "Masukkan API Key OpenRouter:"
            read openrouter_key
            echo "OPENROUTER_API_KEY=$openrouter_key" >> .env
            echo "OLLAMA_MODEL=" >> .env # Pastikan ini kosong jika OpenRouter
        elif [ "$ai_provider" == "ollama" ]; then
            echo "Masukkan nama model Ollama yang akan digunakan (contoh: llama2):"
            read ollama_model_name
            echo "OLLAMA_MODEL=$ollama_model_name" >> .env
            echo "OPENROUTER_API_KEY=" >> .env # Pastikan ini kosong jika Ollama
        else
            echo "AI_PROVIDER tidak valid. AI mungkin tidak berfungsi."
            echo "USE_AI=False" >> .env
            echo "OPENROUTER_API_KEY=" >> .env
            echo "OLLAMA_MODEL=" >> .env
        fi
    else
        echo "USE_AI=False" >> .env
        echo "AI_PROVIDER=" >> .env
        echo "OPENROUTER_API_KEY=" >> .env
        echo "OLLAMA_MODEL=" >> .env
    fi

    # Hugging Face API Token untuk Image Generation
    echo -e "${CYAN}Masukkan Hugging Face API Token untuk Image Generation (opsional, kosongkan jika tidak ingin):${NC}"
    read hf_api_token
    echo "HF_API_TOKEN=$hf_api_token" >> .env

    # Link Donasi Saweria
    echo -e "${CYAN}Masukkan link Saweria kamu (contoh: https://saweria.co/username):${NC}"
    read saweria_link
    echo "LINK_DONASI_SAWERIA=$saweria_link" >> .env

    # Token ShrinkMe
    echo -e "${CYAN}Masukkan API Token ShrinkMe.io kamu (opsional, kosongkan jika tidak ingin):${NC}"
    read shrinkme_token
    echo "SHRINKME_API_TOKEN=$shrinkme_token" >> .env


    echo -e "${GREEN}File .env sudah dibuat. Harap periksa dan isi API_ID, API_HASH, BOT_TOKEN, dan USERNAME secara manual jika belum terisi.${NC}"
else
    echo -e "${GREEN}.env sudah ada, lewati pembuatan. Harap pastikan semua variabel sudah terisi.${NC}"
fi

echo -e "${GREEN}Setup selesai! Jalankan bot dengan: python3 main.py${NC}"