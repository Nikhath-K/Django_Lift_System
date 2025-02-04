"# Django Lift System" 

# 🚀 Django Lift System - Real-Time Lift Monitoring

A real-time **lift monitoring system** using **Django, WebSockets, Modbus RTU, and RSS News Feeds**.

## 🎯 Features:
✅ **Live Lift Data Updates** (No delays)  
✅ **Real-Time WebSockets for Parallel Processing**  
✅ **Dynamic Floor Image Changes**  
✅ **Smooth Scrolling RSS News Bar**  
✅ **Multiprocessing for Faster Modbus & RSS Data**  
✅ **Compatible with Ubuntu, Windows, macOS**

---

## 🔧 Installation Guide

1️⃣ Clone the Repository
```bash
git clone https://github.com/Nikhath-K/Django_Lift_System.git

cd Django_Lift_System

2️⃣ Create a Virtual Environment
python3 -m venv myenv
source myenv/bin/activate  # Linux/macOS
myenv\Scripts\activate  # Windows


3️⃣ Install Dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt


4️⃣ Run Migrations
python manage.py migrate


5️⃣ Start the Server
python manage.py runserver
🔹 Visit: http://127.0.0.1:8000/


📜 requirements.txt (Dependencies)
Django==4.2.18
channels==4.0.0
daphne==4.0.0
autobahn==23.6.2
asgiref==3.7.2
channels-redis==4.1.0
pymodbus==2.5.0
pyserial==3.5
feedparser==6.0.10
cryptography==42.0.2
setuptools==69.0.3
wheel==0.42.0

🛠️ Troubleshooting for Ubuntu Users
If you encounter issues with cryptography or pymodbus, install system dependencies:

sudo apt update && sudo apt install -y \
    python3-dev python3-pip python3-venv \
    libssl-dev libffi-dev build-essential \
    libjpeg-dev zlib1g-dev


🎯 Project Structure

Django_Lift_System/
│── test_project/
│   ├── test_app/
│   │   ├── static
│   │   │   ├──Stock Images/  # Lift images
│   │   │   ├──up_arrow.gif
│   │   │   ├──down_arrow.gif
│   │   ├── templates/test_app/home.html
│   │   ├── views.py
│   │   ├── consumers.py  # WebSockets handling
│   │   ├── modbus_client.py  # Modbus RTU Communication
│   ├── settings.py
│   ├── urls.py
│── README.md  # Project documentation
│── requirements.txt  # Dependencies
│── manage.py


📡 WebSocket Endpoint
The system uses WebSockets for real-time updates.

ws://127.0.0.1:8000/ws/lift-data/
🔹 This ensures parallel updates for Lift Data, Floor Images, and News Feeds.


🎉 Contribute
Want to improve this project? Feel free to fork and submit a pull request.
We welcome contributions! 🚀