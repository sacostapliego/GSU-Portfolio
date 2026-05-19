# Smart Parking Finder for Atlanta

A cloud-powered web application that displays real-time (simulated) parking availability, pricing, and location data for both large commercial garages and small local lots across Atlanta. Built as a Cloud Computing course project demonstrating serverless functions, managed databases, and distributed architecture.

- **Frontend** — React with Leaflet interactive map, filters, and admin panel
- **Backend** — FastAPI REST API serving parking data with filtering and CRUD
- **Database** — PostgreSQL storing parking lot data (locations, pricing, availability)
- **Lambda** — Simulates IoT occupancy updates every 5 minutes via CloudWatch

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | React, Leaflet, React Router, Axios |
| Backend    | FastAPI, SQLAlchemy, Pydantic     |
| Database   | PostgreSQL (AWS RDS)              |
| Automation | AWS Lambda + CloudWatch Events    |
| Hosting    | AWS S3 + CloudFront, EC2/Elastic Beanstalk |

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+ (or Docker)

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
docker compose up --build
```

This starts PostgreSQL, the backend (port 8000), and the frontend (port 3000).

Then seed the database:
```bash
docker compose exec backend python -m app.seed
```

### Option 2: Manual Setup

**Database:**
```bash
# Start PostgreSQL and create the database
createdb smart_parking
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m app.seed          # Seed with Atlanta parking data
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

The app will be available at `http://localhost:3000`.

## API Endpoints

| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| GET    | `/parking`                        | List all parking lots    |
| GET    | `/parking/cheapest`               | Lots sorted by price     |
| GET    | `/parking/small`                  | Small lots only          |
| GET    | `/parking/nearby?lat=&lng=&radius=` | Lots within radius (mi)  |
| GET    | `/parking/{id}`                   | Single lot details       |
| POST   | `/admin/parking`                  | Create a lot             |
| PUT    | `/admin/parking/{id}`             | Update a lot             |
| DELETE | `/admin/parking/{id}`             | Delete a lot             |

API docs available at `http://localhost:8000/docs` (Swagger UI).

## Lambda Simulation

The `lambda/simulate_occupancy.py` function simulates IoT sensor updates:
- Adjusts `occupied_count` randomly for each lot (-3 to +5 cars)
- Clamps values within valid bounds (0 to slot_count)
- Updates `last_updated` timestamp
- Designed to run on AWS Lambda with CloudWatch Events every 5 minutes

Run locally for testing:
```bash
python lambda/simulate_occupancy.py
```

## Project Structure

```
Smart-Parking-Finder/
├── backend/
│   ├── app/
│   │   ├── main.py          
│   │   ├── config.py        
│   │   ├── database.py     
│   │   ├── models.py        
│   │   ├── schemas.py       
│   │   ├── seed.py         
│   │   └── routers/
│   │       ├── parking.py 
│   │       └── admin.py     
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js           
│   │   ├── api.js         
│   │   └── components/
│   │       ├── Navbar.js
│   │       ├── ParkingMap.js
│   │       ├── ParkingList.js
│   │       ├── ParkingDetail.js
│   │       ├── Filters.js
│   │       ├── AdminPanel.js
│   │       └── AdminLotForm.js
│   ├── package.json
│   └── Dockerfile
├── lambda/
│   ├── simulate_occupancy.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Cloud Deployment (AWS)

| Component  | AWS Service                    |
|------------|--------------------------------|
| Frontend   | S3 + CloudFront (CDN)          |
| Backend    | EC2 or Elastic Beanstalk       |
| Database   | RDS (PostgreSQL)               |
| Simulation | Lambda + CloudWatch Events     |
| Security   | IAM roles, HTTPS via ACM       |

