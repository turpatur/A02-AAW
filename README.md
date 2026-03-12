## Cara Menjalankan Project

Jalankan perintah berikut:

```bash
docker compose up --build -d
```

Aplikasi yang akan berjalan:

- **Frontend (FE)**: http://localhost:8080  
- **Backend (BE)**: http://localhost:5000  
- **RabbitMQ Dashboard**: http://localhost:15672  
  - Username: `guest`  
  - Password: `guest`

---

# Alur Event

Backend akan mem-publish event ke RabbitMQ menggunakan kode berikut:

```python
channel.basic_publish(
    exchange="post_events",
    routing_key="",
    body=json.dumps(event)
)

connection.close()
return {"status": "ok"}
```

Ketika `api.py` menerima request, program akan **langsung mem-publish pesan ke RabbitMQ** dan **langsung memberikan response ke client** tanpa menunggu respons dari consumer ataupun memeriksa kondisi consumer.

Setelah pesan masuk ke RabbitMQ, broker akan mendistribusikan pesan tersebut ke queue yang sudah di-bind pada exchange, yaitu:

- `logger_queue`
- `wordcount_queue`
- `archive_queue`

Ketiga queue ini akan **memproses pesan secara paralel** tanpa ketergantungan satu sama lain.

Output dari masing-masing consumer dapat dilihat pada **logs Docker** berikut:

<img width="519" height="82" alt="image" src="https://github.com/user-attachments/assets/27c36db7-4898-483a-b923-345dcb5c8ce2" />

---

# Simulasi Ketika Consumer Mati

Jika salah satu container dimatikan, misalnya:

```bash
docker compose stop logger_consumer
```

Maka pesan yang dikirim oleh producer **tidak akan hilang**, tetapi akan **tertahan di queue dengan status `Ready`** hingga consumer kembali aktif.

### Logs

<img width="1057" height="580" alt="image" src="https://github.com/user-attachments/assets/a169f57e-b617-442f-a13b-2c5de4e8a056" />

### RabbitMQ Dashboard

<img width="1745" height="504" alt="image" src="https://github.com/user-attachments/assets/605111de-ca14-406c-aff7-e692e03abbbb" />

---

# Consumer Dinyalakan Kembali

Ketika container consumer dijalankan kembali, pesan yang tertahan di queue akan langsung diproses oleh consumer.

### Logs

<img width="1059" height="678" alt="image" src="https://github.com/user-attachments/assets/67cd2547-fbd5-43c3-89ba-cfe3bdf48328" />

### RabbitMQ Dashboard

<img width="1790" height="609" alt="image" src="https://github.com/user-attachments/assets/2b4ddbdd-8601-41cf-9d6b-3cdf7cf8defb" />

---

# Perbandingan Sinkronus vs Asinkronus

### Sinkronus
Pada proses sinkronus, browser harus **menunggu seluruh proses selesai** sebelum menerima respons dari server. Jika salah satu proses gagal atau lambat, maka respons ke client juga akan tertunda.

### Asinkronus
Pada proses asinkronus, server dapat **langsung memberikan respons kepada client** tanpa menunggu seluruh proses selesai.

Setiap consumer dapat memproses pesan secara **independen** tanpa mempengaruhi consumer lainnya.

Selain itu, sistem asinkronus **tetap dapat berjalan meskipun salah satu consumer tidak tersedia**, karena pesan akan tetap disimpan di queue hingga consumer siap memprosesnya kembali.

---

# Pertanyaan Tutorial

Jawaban untuk pertanyaan tutorial dapat dilihat pada file berikut:

```
Tutorial_WorkloadDesign_2306206282_FathurrahmanKesumaRidwan.pdf
```

---

# AI Declaration

Saya menggunakan **Claude** untuk:

- Brainstorming ide
- Membantu implementasi integrasi dengan RabbitMQ
- Debugging
- Membantu merapikan format README
