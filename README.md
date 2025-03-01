# MobiSpace - Mobile Environmental Sensing Platform

A distributed system for collecting, processing, and visualizing mobile environmental sensor data in real-time and batch modes.

## 📌 Overview

MobiSpace enables crowd-sourced environmental monitoring by collecting sensor data from mobile devices. The system processes:
- Real-time GPS location data
- Environmental metrics (PM2.5, PM10, Temperature, Humidity, etc.)
 
## ✨ Key Features

- **Real-time Data Streaming**: Kafka-based data ingestion
- **Interactive Visualization**: Grafana dashboards with live maps and metrics
- **Batch Processing**: Airflow-powered data pipelines
- **Scalable Architecture**: Dockerized microservices
- **Smart Analytics**: Stop detection and activity classification (upcoming)

## 🧩 System Components

### Data Pipeline
```plaintext
CSV Simulators → Kafka → PostgreSQL → Grafana (Real-time)
                             ↓
                          Airflow (Batch Processing)
```

### Tech Stack
- **Stream Processing**: Apache Kafka
- **Database**: PostgreSQL
- **Visualization**: Grafana
- **Orchestration**: Apache Airflow
- **Infrastructure**: Docker

## 📂 Project Structure

```
mobispace/
├── app/
│   ├── producer/           # Kafka producer (data simulation)
│   ├── consumer/           # Kafka consumer (DB writer)
│   ├── initdb/             # Database initialization scripts
│   ├── grafana-data/       # Grafana volume
│   └── docker-compose.yaml # Main service orchestration
│
└── airflow/
    ├── dags/               # Data processing workflows
    ├── plugins/            # Custom Airflow plugins
    └── docker-compose.yaml # Airflow orchestration
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.8+

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/mobispace.git
cd mobispace
```

2. **Create Docker Network**
```bash
docker network create mobispace
```

3. **Start Core Services**
```bash
cd app
docker-compose up -d
```

4. **Start Airflow**
```bash
cd ../airflow
docker-compose up -d
```

Services will be available at:
- Grafana: `http://localhost:3000`
- Airflow: `http://localhost:8080`

### Data Simulation
Edit CSV files in `/app/data` to modify simulated sensor input:
- `gps.csv`: Virtual participant locations
- `measures.csv`: Environmental metrics

## 📊 Using the System

### Real-time Monitoring
1. Access Grafana at `http://localhost:3000`
2. Default credentials: admin/admin
3. Explore dashboards:
   - **Live Movement Map**: Participant GPS tracking
   - **Environmental Metrics**: Real-time pollution data

### Batch Processing
1. Access Airflow at `http://localhost:8080`
2. Default credentials: airflow/airflow
3. Trigger `main_workflow` DAG to:
   - Preprocess raw data
   - Generate analytical datasets
   - (Upcoming) Perform activity classification

## 🛠 Development

### Modifying Pipelines
1. Edit DAGs in `/airflow/dags`
2. Update processing logic in `/tasks`
3. Redeploy Airflow:
```bash
cd airflow
docker-compose up --build -d
```

## 📸 Screenshots

**Live Movement Tracking**  
![GPS Map](https://via.placeholder.com/600x300.png?text=Live+Participant+Movement+Map)  
*Real-time GPS data visualization with heatmap overlay*

### Data Pipeline
**Airflow DAG Overview**  
![Airflow DAG](https://via.placeholder.com/600x300.png?text=Airflow+DAG+Execution)  
*Data processing workflow with task dependencies*

## 🎥 Demo Video
- [Demo 01](https://drive.google.com/file/d/1tBk5DeFUIoAhQ8M8h2qHO8CRhBsAZ6F-/view?usp=sharing)  
- [Demo 02](https://drive.google.com/file/d/1DJImzbaB9cyATAahJH8Tg6Sbpl221GnR/view?usp=sharing)



## 📜 License
Apache 2.0 License

## 🤝 Contributing
Feel free to fork and add features!