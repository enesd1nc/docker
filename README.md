# ☁️ CloudNotes - Bulut Tabanlı Not Defteri

Bu proje, modern bulut bilişim teknolojileri ve sanallaştırma prensipleri kullanılarak geliştirilmiş, web tabanlı bir not alma uygulamasıdır. Uygulama, geliştirme ortamında **Docker** ile konteynerize edilmiş ve prodüksiyon ortamı için **Render** bulut platformunda yayınlanmıştır.

## 🚀 Proje Hakkında

CloudNotes, kullanıcıların tarayıcı üzerinden hızlıca not ekleyip silebileceği, sade arayüze sahip bir web uygulamasıdır. Projenin temel amacı, bir web uygulamasının geliştirilmesinden ziyade, bu uygulamanın **Docker** ile sanallaştırılması ve bir **PaaS (Platform as a Service)** sağlayıcısı olan Render üzerinde canlıya alınması süreçlerini göstermektir.

### Öne Çıkan Özellikler
* 📝 Not ekleme, görüntüleme ve silme.
* 🐳 **Docker & Docker Compose** ile tam izole çalışma ortamı.
* ☁️ **Render** üzerinden kesintisiz (CI/CD) dağıtım.
* 📱 Mobil uyumlu (Responsive) tasarım.

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3 (Custom CSS)
* **Sanallaştırma:** Docker, Dockerfile
* **Orkestrasyon:** Docker Compose
* **Cloud Provider:** Render

## ⚙️ Kurulum ve Çalıştırma (Yerel Ortam)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### Gereksinimler
* Docker Desktop
* Git

### Adım 1: Projeyi Klonlayın
```bash
git clone [https://github.com/KULLANICI_ADIN/REPO_ISMI.git](https://github.com/KULLANICI_ADIN/REPO_ISMI.git)
cd REPO_ISMI
