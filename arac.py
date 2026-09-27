#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil
import urllib.request
import json
import time

def ekran_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def baslik_yaz(baslik):
    print("=" * 60)
    print(f"       PARDUS 25 XFCE PYTHON 3.1 TOOLBOX")
    print(f"       {baslik}")
    print("=" * 60)

def sistem_bilgisi():
    ekran_temizle()
    baslik_yaz("1. SİSTEM BİLGİLERİ")
    os.system('uname -a')
    print("\n--- Dağıtım Bilgisi ---")
    os.system('cat /etc/os-release')
    print("\n--- Disk Kullanımı ---")
    os.system('df -h /')
    input("\nAna menüye dönmek için ENTER tuşuna basın...")

def paket_guncelle():
    ekran_temizle()
    baslik_yaz("2. PAKETLERİ GÜNCELLE")
    print("Sistem güncelleniyor (apt update & upgrade)...")
    os.system('sudo apt update && sudo apt upgrade -y')
    input("\nİşlem tamamlandı. Devam etmek için ENTER tuşuna basın...")

def hizli_temizlik():
    ekran_temizle()
    baslik_yaz("3. HIZLI SİSTEM TEMİZLİĞİ")
    print("Gereksiz paketler ve önbellek temizleniyor...")
    os.system('sudo apt autoremove -y && sudo apt clean')
    input("\nTemizlik tamamlandı. Devam etmek için ENTER tuşuna basın...")

def hiz_testi():
    ekran_temizle()
    baslik_yaz("4. İNTERNET HIZ TESTİ")
    print("speedtest-cli kontrol ediliyor...")
    if shutil.which('speedtest-cli') is None:
        print("speedtest-cli bulunamadı, kuruluyor...")
        os.system('sudo apt install speedtest-cli -y')
    os.system('speedtest-cli')
    input("\nTest tamamlandı. Devam etmek için ENTER tuşuna basın...")

def yerel_ip_ogren():
    ekran_temizle()
    baslik_yaz("5. YEREL IP ADRESİ")
    os.system('hostname -I')
    input("\nDevam etmek için ENTER tuşuna basın...")

def dis_ip_ogren():
    ekran_temizle()
    baslik_yaz("6. DIŞ (WAN) IP ADRESİ")
    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json') as response:
            data = json.loads(response.read().decode())
            print(f"Dış IP Adresiniz: {data.get('ip')}")
    except Exception as e:
        print(f"IP adresi alınamadı: {e}")
    input("\nDevam etmek için ENTER tuşuna basın...")

def port_taramasi():
    ekran_temizle()
    baslik_yaz("7. YEREL PORT TARAMASI (NETSTAT)")
    os.system('ss -tuln')
    input("\nDevam etmek için ENTER tuşuna basın...")

def ram_kullanimi():
    ekran_temizle()
    baslik_yaz("8. RAM KULLANIMI")
    os.system('free -h')
    input("\nDevam etmek için ENTER tuşuna basın...")

def cpu_bilgisi():
    ekran_temizle()
    baslik_yaz("9. CPU / İŞLEMCİ BİLGİSİ")
    os.system('lscpu')
    input("\nDevam etmek için ENTER tuşuna basın...")

def aktif_sure():
    ekran_temizle()
    baslik_yaz("10. SİSTEM ÇALIŞMA SÜRESİ")
    os.system('uptime')
    input("\nDevam etmek için ENTER tuşuna basın...")

def dosya_bulucu():
    ekran_temizle()
    baslik_yaz("11. DOSYA ARAMA")
    aranan = input("Aranacak dosya adı: ")
    dizin = input("Hangi dizinde aransın (varsayılan /home): ")
    if not dizin:
        dizin = "/home"
    os.system(f"find {dizin} -name '*{aranan}* 2>/dev/null'")
    input("\nArama tamamlandı. Devam etmek için ENTER tuşuna basın...")

def servis_durumlari():
    ekran_temizle()
    baslik_yaz("12. ÇALIŞAN SERVİSLER")
    os.system('systemctl list-units --type=service --state=running')
    input("\nDevam etmek için ENTER tuşuna basın...")

def usb_aygitlar():
    ekran_temizle()
    baslik_yaz("13. USB CİHAZLARI LİSTELE")
    os.system('lsusb')
    input("\nDevam etmek için ENTER tuşuna basın...")

def pci_aygitlar():
    ekran_temizle()
    baslik_yaz("14. PCI / DONANIM LİSTESİ")
    os.system('lspci')
    input("\nDevam etmek için ENTER tuşuna basın...")

def aktif_kullanicilar():
    ekran_temizle()
    baslik_yaz("15. AKTİF KULLANICILAR")
    os.system('who')
    input("\nDevam etmek için ENTER tuşuna basın...")

def komut_gecmisi():
    ekran_temizle()
    baslik_yaz("16. SON KOMUT GEÇMİŞİ")
    os.system('history | tail -n 20')
    input("\nDevam etmek için ENTER tuşuna basın...")

def xfce_ayarlar_yedek():
    ekran_temizle()
    baslik_yaz("17. XFCE PANEL AYARLARINI YEDEKLE")
    hedef = os.path.expanduser("~/xfce4_panel_yedek.tar.gz")
    kaynak = os.path.expanduser("~/.config/xfce4/panel")
    if os.path.exists(kaynak):
        os.system(f"tar -czf {hedef} -C ~/.config/xfce4 panel")
        print(f"Yedek başarıyla oluşturuldu: {hedef}")
    else:
        print("XFCE panel yapılandırma klasörü bulunamadı.")
    input("\nDevam etmek için ENTER tuşuna basın...")

def sistem_saat_senkron():
    ekran_temizle()
    baslik_yaz("18. SAATİ SENKRONİZE ET")
    os.system('sudo timedatectl set-ntp true')
    print("NTP zaman senkronizasyonu aktif edildi.")
    os.system('timedatectl status')
    input("\nDevam etmek için ENTER tuşuna basın...")

def ping_testi():
    ekran_temizle()
    baslik_yaz("19. PING TESTİ (Google DNS)")
    print("Google DNS (8.8.8.8) adresine ping atılıyor (Durdurmak için Ctrl+C)...")
    os.system('ping -c 4 8.8.8.8')
    input("\nDevam etmek için ENTER tuşuna basın...")

def ortam_degiskenleri():
    ekran_temizle()
    baslik_yaz("20. ORTAM DEĞİŞKENLERİ (ENV)")
    os.system('printenv')
    input("\nDevam etmek için ENTER tuşuna basın...")

def sistem_yeniden_baslat():
    ekran_temizle()
    baslik_yaz("21. SİSTEMİ YENİDEN BAŞLAT")
    onay = input("Sistemi şimdi yeniden başlatmak istiyor musunuz? (e/h): ")
    if onay.lower() == 'e':
        os.system('sudo reboot')

def ana_menu():
    while True:
        ekran_temizle()
        baslik_yaz("ANA MENÜ")
        print(" 1. Sistem Bilgileri")
        print(" 2. Paketleri Güncelle (Apt)")
        print(" 3. Hızlı Sistem Temizliği")
        print(" 4. İnternet Hız Testi (Speedtest)")
        print(" 5. Yerel IP Adresi")
        print(" 6. Dış (WAN) IP Adresi")
        print(" 7. Yerel Port Taraması")
        print(" 8. RAM Kullanımı")
        print(" 9. CPU / İşlemci Bilgisi")
        print("10. Sistem Çalışma Süresi")
        print("11. Dosya Arama")
        print("12. Çalışan Servisler")
        print("13. USB Cihazları Listele")
        print("14. PCI Donanım Listesi")
        print("15. Aktif Kullanıcılar")
        print("16. Son Komut Geçmişi")
        print("17. XFCE Panel Ayarlarını Yedekle")
        print("18. Saati Senkronize Et (NTP)")
        print("19. Ping Testi (8.8.8.8)")
        print("20. Ortam Değişkenleri (Env)")
        print("21. Sistemi Yeniden Başlat")
        print(" 0. Çıkış")
        print("=" * 60)
        
        secim = input("Lütfen bir seçenek girin (0-21): ").strip()
        
        if secim == '1':
            sistem_bilgisi()
        elif secim == '2':
            paket_guncelle()
        elif secim == '3':
            hizli_temizlik()
        elif secim == '4':
            hiz_testi()
        elif secim == '5':
            yerel_ip_ogren()
        elif secim == '6':
            dis_ip_ogren()
        elif secim == '7':
            port_taramasi()
        elif secim == '8':
            ram_kullanimi()
        elif secim == '9':
            cpu_bilgisi()
        elif secim == '10':
            aktif_sure()
        elif secim == '11':
            dosya_bulucu()
        elif secim == '12':
            servis_durumlari()
        elif secim == '13':
            usb_aygitlar()
        elif secim == '14':
            pci_aygitlar()
        elif secim == '15':
            aktif_kullanicilar()
        elif secim == '16':
            komut_gecmisi()
        elif secim == '17':
            xfce_ayarlar_yedek()
        elif secim == '18':
            sistem_saat_senkron()
        elif secim == '19':
            ping_testi()
        elif secim == '20':
            ortam_degiskenleri()
        elif secim == '21':
            sistem_yeniden_baslat()
        elif secim == '0':
            print("Toolbox kapatılıyor...")
            sys.exit(0)
        else:
            input("Geçersiz seçim! Tekrar denemek için ENTER tuşuna basın...")

if __name__ == '__main__':
    try:
        ana_menu()
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
        sys.exit(0)
