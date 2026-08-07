# n8n Docker Deployment & Workflow Architecture

## Overview & Image Naming

`n8n` is an open-source workflow automation tool. When running n8n via Docker,
it is critical to use the official repository image name.

* **Official Docker Hub Image**: `n8nio/n8n`
* **Common Error**: Running `docker run -d n8n` fails with:
  `Error response from daemon: pull access denied for n8n, repository does not exist or may require 'docker login'`

### Why `docker run -d n8n` Fails
Docker defaults to the root library namespace (`docker.io/library/n8n`) when
no organization prefix is supplied. Since n8n is published under the `n8nio`
organization, Docker cannot find `n8n:latest` under the default root namespace.

---

## Docker Fundamentals: Image vs Container

### Docker Image
A **Docker Image** is an immutable, read-only template that contains application code,
dependencies, runtime environment, libraries, and configuration layers required to run an application.
* **Analogy**: A class definition or a blueprint.
* **n8n Example**: `n8nio/n8n:latest` (or `n8nio/n8n:1.45.1`).

### Docker Container
A **Docker Container** is a runnable, isolated instance created from a Docker image.
It adds a thin read-write filesystem layer on top of the image and runs as an isolated OS process.
* **Analogy**: An instantiated object created from a class.
* **n8n Example**: The named container instance `n8n` (e.g., ID `c4f216311572`).

---

## Essential Docker Management Commands

### 1. Managing Container Lifecycle
* **List All Containers (Running & Exited)**:
  ```bash
  docker ps -a
  ```
* **Start an Existing Exited Container**:
  ```bash
  docker start n8n
  ```
* **Stop a Running Container**:
  ```bash
  docker stop n8n
  ```
* **Restart a Container**:
  ```bash
  docker restart n8n
  ```
* **Remove a Stopped Container**:
  ```bash
  docker rm n8n
  ```

### 2. Inspecting Images & Containers
* **List Local Docker Images**:
  ```bash
  docker images
  ```
* **View Container Logs**:
  ```bash
  docker logs -f n8n
  ```
* **Inspect Container Config & Volume Mounts**:
  ```bash
  docker inspect n8n
  ```


---

## Core Architecture & Deployment Modes

### 1. Single Container Mode (Development / Small Workloads)
In single container mode, n8n runs UI, execution engine, and SQLite database
within one container.

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_HOST="localhost" \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL="http" \
  --restart unless-stopped \
  n8nio/n8n
```

### 2. Distributed Queue Mode (Production Architecture)
For high-volume production, n8n separates responsibilities across multiple
containers using Redis as a message broker and PostgreSQL as the state store:

* **Main Instance**: Serves the UI, manages webhooks, and dispatches jobs.
* **Worker Instances**: Execute workflow nodes asynchronously.
* **Redis**: Serves as the task queue broker.
* **PostgreSQL**: Stores workflow definitions, credentials, and execution history.

```
                  +-------------------+
                  |   Reverse Proxy   |
                  | (Nginx / Traefik) |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |  n8n Main (UI/WH) |
                  +----+---------+----+
                       |         |
         +-------------+         +-------------+
         v                                     v
+-----------------+                   +-----------------+
|   PostgreSQL    |                   |      Redis      |
| (Database Store)|                   |  (Task Broker)  |
+-----------------+                   +--------+--------+
                                               |
                                               v
                                      +-----------------+
                                      |   n8n Workers   |
                                      +-----------------+
```

---

## Production Docker Compose Configuration

Below is a production-ready `docker-compose.yml` implementing PostgreSQL and
isolated networks.

```yaml
version: '3.8'

networks:
  n8n-internal:
    driver: bridge

volumes:
  db_data:
  n8n_data:

services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - n8n-internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  n8n:
    image: n8nio/n8n:1.45.1
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - WEBHOOK_URL=https://${SUBDOMAIN}.${DOMAIN_NAME}/
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - n8n-internal
    depends_on:
      postgres:
        condition: service_healthy
```

---

## Key Best Practices & Pitfalls

1. **Pin Specific Image Tags**: Never use `n8nio/n8n:latest` in production.
   Pin to a explicit release (e.g., `n8nio/n8n:1.45.1`) to ensure predictable
   deployments.
2. **Back Up Encryption Key**: `N8N_ENCRYPTION_KEY` encrypts credentials stored
   in the database. Loss of this key permanently invalidates stored credentials.
3. **Database Selection**: Avoid SQLite in production; use PostgreSQL to ensure
   concurrency handling and point-in-time recovery.
4. **Volume Mounting**: Persist `/home/node/.n8n` to preserve encryption keys
   and local execution data.

---

## References

* [Official n8n Docker Documentation](https://docs.n8n.io/hosting/installation/docker/)
* [n8n Environment Variables Reference](https://docs.n8n.io/hosting/environment-variables/)
* [n8n Scaling & Queue Mode](https://docs.n8n.io/hosting/scaling/queue-mode/)

---

## Interview Questions & Answers (5 YOE Level)

### Question 1: Conceptual
**Q**: Why does `docker run -d n8n` fail with `pull access denied for n8n, repository does not exist`, and how does Docker handle default image resolution?

**A**: Docker resolves image names using the pattern `[registry_host/][vendor_namespace/]repository[:tag]`.
When only `n8n` is requested, Docker assumes `docker.io/library/n8n:latest`.
The Docker Hub official image library (`library/`) is restricted to curated, top-level official images (like `python`, `nginx`, `postgres`). Third-party open-source vendors host images under their organization namespace. n8n is published under `n8nio/n8n`.
Because `library/n8n` does not exist, Docker Hub returns an authentication/not-found error (`pull access denied or repository does not exist`). The fix is to specify the fully qualified repository path: `n8nio/n8n`.

**Follow-up Question**: How would you configure a private container registry (e.g., AWS ECR or Harbor) to proxy or pull images from Docker Hub securely in an enterprise environment?

---

### Question 2: Practical / Scenario-Based
**Q**: An n8n deployment in a Docker container restarted, and all saved credentials became invalid, throwing decryption errors. What root cause produced this issue, and how do you remediate it?

**A**: The root cause is an missing or auto-generated `N8N_ENCRYPTION_KEY` combined with a non-persistent `/home/node/.n8n` volume.
When n8n starts without an explicit `N8N_ENCRYPTION_KEY` environment variable, it generates a random encryption key on first run and saves it to config files inside `/home/node/.n8n`. If the container restarts without volume persistence (or if the container is recreated), a new random key is generated. The new key cannot decrypt credentials encrypted by the previous key.

**Remediation**:
1. Explicitly set a static `N8N_ENCRYPTION_KEY` in environment variables or container configuration (e.g., Docker secrets or `.env` file).
2. Ensure `/home/node/.n8n` is mapped to a persistent named Docker volume or bind mount.
3. Securely back up `N8N_ENCRYPTION_KEY` in a vault (HashiCorp Vault, AWS Secrets Manager).

**Follow-up Question**: How can you rotate the n8n encryption key in production without losing credential data?

---

### Question 3: System Design / Architecture
**Q**: How would you design a high-throughput, fault-tolerant self-hosted n8n environment capable of processing tens of thousands of webhooks per minute?

**A**: To scale n8n for high throughput:
1. **Architecture Mode**: Deploy n8n in **Queue Mode**.
2. **Main Instance**: Deploy a main n8n instance dedicated exclusively to handling webhooks, API requests, and rendering the UI (`EXECUTIONS_PROCESS=main`). Disable direct workflow execution on the main node.
3. **Task Queue**: Deploy a high-availability **Redis** cluster to queue workflow execution jobs payload.
4. **Worker Pool**: Deploy autoscaling worker containers (`n8nio/n8n worker`) connected to the Redis queue. Scale worker replicas horizontally based on Redis queue depth and CPU utilization metrics.
5. **Database**: Use a managed **PostgreSQL** instance with connection pooling (e.g., PgBouncer) and primary/replica replication.
6. **Reverse Proxy & Load Balancer**: Place an ALB or Traefik in front of main n8n instances with SSL termination and DDoS protection.
7. **Pruning & Data Lifecycle**: Enable execution data pruning (`EXECUTIONS_DATA_PRUNE=true`, `EXECUTIONS_DATA_MAX_AGE=168`) to prevent execution history tables from bloating database disk usage.

**Follow-up Question**: How do you handle webhook backpressure when worker node consumption falls behind incoming request rates?

---

### Question 4: Disaster Recovery & Security
**Q**: What security and backup strategy should be enforced for self-hosted containerized automation platforms like n8n?

**A**:
1. **Security Control**:
   * **Network Segregation**: Place database and Redis containers on an internal Docker bridge network without mapped host ports.
   * **Non-Root User**: Run the container under a non-root UID (n8n container runs as `node` user by default).
   * **Reverse Proxy**: Enforce TLS 1.3 via Nginx/Traefik and set security headers (`HSTS`, `CSP`).
   * **Environment Variables**: Store sensitive values in secret vaults or encrypted files, avoiding inline docker-compose secrets.
2. **Backup Strategy**:
   * **Database Snapshots**: Daily automated PostgreSQL logical dumps (`pg_dump`) with point-in-time recovery (PITR) WAL archiving.
   * **Volume Backup**: Nightly backup of `/home/node/.n8n` containing custom nodes and file storage.
   * **Git-Based Workflow Backups**: Export workflows as JSON automatically via n8n CLI/API into a Git repository for infrastructure-as-code version control.

**Follow-up Question**: What container security scanning tools would you integrate into a CI/CD pipeline before deploying updated n8n images?
