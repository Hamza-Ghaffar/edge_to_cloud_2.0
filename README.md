# Edge-to-Cloud 2.0: AI-Powered Detection System

![sequence_dia](https://github.com/user-attachments/assets/3d5dfc24-bd27-4450-b5cb-4af83623adf4)


A three-layer architecture system to detect, process, store, and visualize real-time detection data from cameras using AI models, edge computing, and cloud technologies.


## 🚀 **Project Overview**
![image](https://github.com/user-attachments/assets/b94fb498-d1e0-43d9-b29d-8a64b10d3ca4)
![image](https://github.com/user-attachments/assets/26497cd6-9c33-46a6-8ddc-054bdedb145d)



The **Edge-to-Cloud 2.0** project demonstrates an AI-powered, three-layer architecture system:

1. **AI/ML Layer**:
   - Detects people in a room via cameras using AI models.
   - Sends detection data (CameraId, DetectionTime, Detections) to the Edge layer.

2. **Edge Layer**:
   - Acts as an intermediate gateway to forward detection data to the cloud.
   - Does not store data.

3. **Cloud Layer**:
   - Processes and stores detection data in a MariaDB database.
   - Serves the data to a front-end dashboard for visualization.

---


## 📂 **Project Structure**

```plaintext
├── static/                # Frontend files (HTML, CSS, JS)
│   ├── index.html         # Frontend dashboard
│   ├── style.css          # Styling for the dashboard
│   ├── googlefonts.css    # Custom fonts
│   ├── chart.js           # Line graph visualization
│   └── jquery-3.6.0.min.js # AJAX for backend communication
├── db_init/               # Database initialization scripts
│   └── init.sql           # Creates database and tables
├── main.py                # FastAPI backend
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration for FastAPI
├── docker-compose.yml     # Docker Compose configuration
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
└── README.md              # Project documentation

Column	Type	Description
Id	INT (PK)	Primary key (auto-increment).
CameraId	VARCHAR(50)	Unique ID of the camera.
DetectionTime	DATETIME	Timestamp of the detection.
Detections	INT	Count of detections.


👥 Contributors
Hamza Ghaffar - GitHub
Ruth Dunthuluri

Special thanks to the Cloud Team, ML Team, and all contributors who helped build this project.

This project is licensed under the FH Kaernten. (Public)
