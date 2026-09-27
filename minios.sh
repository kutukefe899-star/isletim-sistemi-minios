#!/bin/bash

# Renk tanımları
green='\033[0;32m'
cyan='\033[0;36m'
clear_color='\033[0m'

while true; do
    clear
    # ASCII Sanat Karşılama Ekranı
    echo -e "${cyan}"
    echo "  ______ F_K ______   ___  ____  "
    echo " |  ____|  ___|   \ / _ \/ ___| "
    echo " | |__  | |_  | |_) | | | \___ \ "
    echo " |  __| |  _| |  _ <| |_| |___) |"
    echo " |_|    |_|   |__| \_\\___/|____/ "
    echo -e "${clear_color}"
    echo " [ Pardus XFCE Destekli Özel Mini OS ]"
    echo "----------------------------------------"

    # Whiptail ile şık grafiksel menü
    SECIM=$(whiptail --title "EFE OS - Ana Kontrol Merkezi" --menu "Bir işlem seçin:" 18 65 7 \
    "1" "Sistem Çekirdeği ve Donanım Bilgisi" \
    "2" "XFCE Masaüstü / Pencere Durumu" \
    "3" "Hızlı Terminal Komut Aracı" \
    "4" "Not Defteri (Nano)" \
    "5" "Sistemi Temizle / Optimize Et" \
    "6" "Python toolbox" \
    "7" "python hafif oyunlar" \
    "8" "Mini OS'ten Çık" 3>&1 1>&2 2>&3)

    exitstatus=$?
    if [ $exitstatus = 0 ]; then
        case $SECIM in
            1)
                KERNEL=$(uname -r)
                UPTIME=$(uptime -p)
                CPU=$(lscpu | grep "Model adı" | sed 's/Model adı:\s*//')
                INFO="Çekirdek Sürümü: $KERNEL\nÇalışma Süresi: $UPTIME\nİşlemci: $CPU"
                whiptail --title "Çekirdek & Donanım" --msgbox "$INFO" 12 60
                ;;
            2)
                XFCE_INFO="Bu Mini OS, altta Pardus XFCE ve Linux çekirdeğini kullanır.\nXFWM4 pencere yöneticisi aktif."
                whiptail --title "XFCE Entegrasyonu" --msgbox "$XFCE_INFO" 10 55
                ;;
            3)
                clear
                echo "=== Terminal Komut Ekranı ==="
                read -p "Çalıştırmak istediğin Linux komutunu gir: " komut
                eval $komut
                read -p "İşlem bitti. Devam etmek için Enter'a basın..."
                ;;
            4)
                nano minios_notlar.txt
                ;;
            5)
                clear
                echo "Sistem önbelleği temizleniyor..."
                sudo apt clean
                echo "İşlem tamamlandı!"
                read -p "Ana menüye dönmek için Enter'a basın..."
                ;;
            6)
                clear
                if [ -f "arac.py" ]; then
                    python3 arac.py
                else
                    echo "Hata: arac.py dosyası bulunamadı!"
                    read -p "Devam etmek için Enter'a basın..."
                fi
                ;;
            7)
                clear
                if [ -f "oyunlar.py" ]; then
                    python3 oyunlar.py
                else
                    echo "SİSTEMDE BİR HATA OLUŞTU VE OYUNLAR BULUNAMADI"
                    read -p "DEVAM ETMEK İÇİN HERHANGİ Bİ TUŞA BASIN"
                fi
                ;; 
            8)
                if (whiptail --title "Çıkış" --yesno "Mini OS sonlandırılsın mı?" 7 35); then
                    clear
                    echo "Mini OS kapatıldı. Normal terminale döndün."
                    exit 0
                fi
                ;;
        esac
    else
        clear
        echo "Mini OS'ten çıkıldı."
        exit 0
    fi
done
