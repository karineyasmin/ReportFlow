# ReportFlow 📈

**ReportFlow** is a production-ready, asynchronous report generation and data export system built with **FastAPI**, **Celery**, and **Keycloak**. 

The project demonstrates how to offload heavy computational or I/O-bound tasks (such as synthesizing large datasets and generating CSV/Excel files) to background workers while keeping the HTTP API responsive, secure, and fully auditable.

---

## 🚀 Key Features

* **Asynchronous Task Processing:** Heavy data extraction and report rendering are offloaded to background workers using **Celery** and **Redis**.
* **Identity & Access Management (IAM):** Secure authentication and fine-grained Role-Based Access Control (RBAC) managed externally via **Keycloak** OAuth2/OIDC.
* **Non-blocking Polling Architecture:** Clients request resources using a standard `202 Accepted` pattern, tracking status updates asynchronously via task IDs.
* **Structured & Colored Logging:** Custom internal logging system powered by `colorama` for clean, production-grade console monitoring.
* **Containerized Ecosystem:** Fully dockerized multi-container stack for seamless local development, testing, and deployment.

---

## 🛠️ Tech Stack

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
* **Task Queue & Automation:** [Celery](https://docs.celeryq.dev/)
* **Message Broker & Result Backend:** [Redis](https://redis.io/)
* **Authentication Server:** [Keycloak](https://www.keycloak.org/) (Quarkus 24.0)
* **Database:** [PostgreSQL 15](https://www.postgresql.org/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/) & [OpenPyXL](https://openpyxl.readthedocs.io/)

---

## ⚙️ Environment Variables (.env)

Create a `.env` file in the root directory using the sample below:

```dotenv
PROJECT_NAME="ReportFlow"
API_V1_STR="/api/v1"

# KEYCLOAK CONFIGURATION
KEYCLOAK_SERVER_URL="http://localhost:8080"
KEYCLOAK_REALM="ReportFlowRealm"
KEYCLOAK_CLIENT_ID="reportflow-backend"
KEYCLOAK_CLIENT_SECRET="pUdcBwnrCLISzWGw6SkDE703IBHT8J0J"
KEYCLOAK_CERTS_URL="http://keycloak:8080/realms/ReportFlowRealm/protocol/openid-connect/certs"

# CELERY & REDIS
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

> **Note:** Inside Docker Compose services, replace `localhost` with the respective service names (`redis`, `keycloak`) when communicating over the internal network.

---

## 🚦 Quick Start

### 1. Start the Environment

Clone the repository and spin up the Docker Compose stack:

```bash
docker compose up -d
```

Check that all containers are running and healthy (`postgres`, `keycloak`, `redis`, `api`, `worker`):

```bash
docker compose ps
```

---

## 🔐 Authentication & Keycloak Setup

The API secures report generation endpoints with Role-Based Access Control (**RBAC**), requiring the `report_admin` realm role.

### Initial Keycloak Setup:
1. Open the Keycloak Admin Console at [http://localhost:8080](http://localhost:8080) (Default admin: `admin` / `admin`).
2. Select or import the **`ReportFlowRealm`**.
3. Under **Realm roles**, ensure the **`report_admin`** role exists.
4. Under **Clients** -> **`reportflow-backend`** -> **Settings**:
   * Set **Valid redirect URIs** to `http://localhost:8000/*`
   * Set **Web origins** to `http://localhost:8000` (or `*`) to permit Swagger UI CORS requests.
5. Under **Users**, create a development user (e.g., `devuser`):
   * Set **Email**, **First Name**, and **Last Name** to satisfy user profile requirements.
   * In the **Credentials** tab, set a permanent password (toggle **Temporary** to **OFF**).
   * In the **Role mapping** tab, assign the **`report_admin`** role.
   * Ensure no pending actions remain under **Required user actions**.

---

## 📖 Interactive API Docs (Swagger UI)

1. Navigate to the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
2. Click the green **Authorize** button at the top right.
3. Fill in the authentication modal:

| Field | Value |
| :--- | :--- |
| **username** | `devuser` |
| **password** | `admin123` (or your configured password) |
| **client_id** | `reportflow-backend` |
| **client_secret** | `pUdcBwnrCLISzWGw6SkDE703IBHT8J0J` |

4. Click **Authorize** and then close the dialog.

---

## 🔄 Report Generation Workflow

| Step | HTTP Method & Path | Status Code | Description |
| :--- | :--- | :--- | :--- |
| **1. Trigger** | `POST /api/v1/reports` | `202 Accepted` | Enqueues background task. Returns `task_id`. |
| **2. Poll** | `GET /api/v1/reports/{task_id}` | `200 OK` | Polls Celery execution state (`PENDING`, `SUCCESS`, etc.). |
| **3. Download** | `GET /api/v1/reports/{task_id}/download` | `200 OK` | Downloads the compiled CSV/Excel export file once ready. |

---

## 🪵 Real-time Monitoring

To inspect asynchronous job execution directly inside the Celery worker:

```bash
docker compose logs -f worker
```