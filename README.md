# ReportFlow 📈

**ReportFlow** is a production-ready, asynchronous report generation and data export system built with **FastAPI**, **Celery**, and **Keycloak**. 

The project demonstrates how to offload heavy computational or I/O-bound tasks (such as processing large datasets and generating Excel/PDF files) to background workers while keeping the HTTP API responsive, secure, and fully auditable.

---

## 🚀 Key Features

* **Asynchronous Task Processing:** Heavy data extraction and report rendering are offloaded to background workers using **Celery** and **Redis**.
* **Identity & Access Management (IAM):** Secure authentication and fine-grained Role-Based Access Control (RBAC) managed externally via **Keycloak** OAuth2/OIDC.
* **Non-blocking Polling Architecture:** Clients request resources using a standard `202 Accepted` pattern, tracking status updates asynchronously.
* **Structured & Colored Logging:** Custom internal logging system powered by `colorama` for beautiful, production-grade console monitoring.
* **Containerized Ecosystem:** Fully dockerized stack for seamless local development, testing, and deployment.

---

## 🛠️ Tech Stack

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
* **Task Queue & Automation:** [Celery](https://docs.celeryq.dev/)
* **Message Broker & Result Backend:** [Redis](https://redis.io/)
* **Authentication Server:** [Keycloak](https://www.keycloak.org/)
* **Database:** [PostgreSQL](https://www.postgresql.org/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/) & [OpenPyXL](https://openpyxl.readthedocs.io/)

## 🔐 Authentication with Swagger

The development environment imports [ReportFlowRealm-realm.json](keycloak/ReportFlowRealm-realm.json)
into Keycloak. The `reportflow-backend` client is public, enables the password flow,
and allows requests from `http://localhost:8000`, so Swagger can authenticate
without a client secret.

Start the stack:

```bash
docker compose up -d
```

If Keycloak was already initialized with an older configuration, recreate the
development volumes to apply the realm import:

```bash
docker compose down -v
docker compose up -d
```

Open the Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs),
click **Authorize**, and use:

| Field | Value |
| --- | --- |
| Username | A user created in the `ReportFlowRealm` realm |
| Password | The user's Keycloak password |
| Client ID | `reportflow-backend` |
| Client secret | Leave empty |
| Scopes | Leave empty |

The token endpoint is
`http://localhost:8080/realms/ReportFlowRealm/protocol/openid-connect/token`.

Create the user in the Keycloak administration console at
[http://localhost:8080](http://localhost:8080), using the `admin` development
credentials, and assign the `report_admin` realm role. This role is required by
`POST /api/v1/reports`.