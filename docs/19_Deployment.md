# Deployment Guide

> Comprehensive guide for deploying Scilab Studio across desktop, web, and cloud environments.

---

## Deployment Options

| Option | Target Audience | Complexity | Scalability |
|--------|----------------|------------|-------------|
| Desktop | Individual engineers, students | Low | Single user |
| Web (self-hosted) | Labs, teams | Medium | 10–50 users |
| Cloud (managed) | Organizations, SaaS | High | 50–10,000+ users |
| Hybrid | Enterprise | High | Custom |

---

## Desktop Installation

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Windows 10, macOS 12, Ubuntu 20.04 | Latest stable versions |
| RAM | 4 GB | 8 GB |
| Disk | 1 GB free | 5 GB free |
| Display | 1280×720 | 1920×1080 |
| Scilab | 2024.0+ | Latest stable |

### Windows

1. Download `Scilab-Studio-Setup-x.x.x.exe` from the releases page.
2. Run the installer.
3. Follow the installation wizard:
   - Choose installation directory (default: `C:\Program Files\Scilab Studio`).
   - Select components to install.
   - Choose Start Menu folder.
4. Launch Scilab Studio from the Start Menu or desktop shortcut.
5. On first launch, the Setup Wizard will help configure Scilab engine path.

### macOS

1. Download `Scilab-Studio-x.x.x.dmg` from the releases page.
2. Open the DMG file.
3. Drag `Scilab Studio.app` to the Applications folder.
4. Launch from Applications or Spotlight.
5. On first launch, grant necessary permissions when prompted.
6. The Setup Wizard will help locate the Scilab engine.

**Note:** macOS may require allowing the app in System Preferences > Security & Privacy for unsigned builds.

### Linux

**Debian/Ubuntu:**
```bash
sudo dpkg -i scilab-studio_x.x.x_amd64.deb
```

**Fedora/RHEL:**
```bash
sudo rpm -i scilab-studio-x.x.x-1.x86_64.rpm
```

**Arch Linux (AUR):**
```bash
yay -S scilab-studio
```

**AppImage (any distro):**
```bash
chmod +x Scilab-Studio-x.x.x.AppImage
./Scilab-Studio-x.x.x.AppImage
```

### Verifying Installation

```bash
# Check Scilab Studio version
scilab-studio --version

# Check Scilab engine connectivity
scilab-studio --check-engine
```

---

## Web Deployment

### Docker Deployment (Recommended)

**Quick Start:**
```bash
# Pull the image
docker pull scilab-studio/server:latest

# Run the container
docker run -d \
  --name scilab-studio \
  -p 3000:3000 \
  -p 8080:8080 \
  -v scilab-data:/app/data \
  -e SCILAB_PATH=/usr/local/bin/scilab \
  scilab-studio/server:latest
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  scilab-studio:
    image: scilab-studio/server:latest
    ports:
      - "3000:3000"   # Application
      - "8080:8080"   # API
    volumes:
      - scilab-data:/app/data
      - ./projects:/app/projects
    environment:
      - SCILAB_PATH=/usr/local/bin/scilab
      - NODE_ENV=production
      - DATABASE_URL=postgresql://db:5432/scilab_studio
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=scilab_studio
      - POSTGRES_USER=scilab
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - scilab-studio
    restart: unless-stopped

volumes:
  scilab-data:
  pgdata:
```

### Nginx Configuration

```nginx
upstream scilab_studio {
    server scilab-studio:3000;
}

server {
    listen 443 ssl http2;
    server_name scilab.example.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    location / {
        proxy_pass http://scilab_studio;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static assets
    location /assets/ {
        proxy_pass http://scilab_studio;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Cloud Deployment

### AWS

**Recommended Services:**
- **Compute:** ECS Fargate or EC2 (for Scilab engine with native dependencies)
- **Database:** RDS PostgreSQL
- **Cache:** ElastiCache Redis
- **Storage:** S3 for packages and user uploads
- **CDN:** CloudFront for static assets
- **Load Balancer:** ALB

**Key Considerations:**
- Fargate may not support Scilab's native dependencies. Use EC2 with a custom AMI or ECS with EC2 launch type.
- Use S3 for marketplace package storage.
- Enable CloudWatch for monitoring and alerting.

### Google Cloud Platform

**Recommended Services:**
- **Compute:** Cloud Run (containerized) or GKE
- **Database:** Cloud SQL (PostgreSQL)
- **Cache:** Memorystore (Redis)
- **Storage:** Cloud Storage
- **CDN:** Cloud CDN

### Azure

**Recommended Services:**
- **Compute:** Azure Container Instances or AKS
- **Database:** Azure Database for PostgreSQL
- **Cache:** Azure Cache for Redis
- **Storage:** Azure Blob Storage
- **CDN:** Azure CDN

### General Cloud Considerations

- Use managed PostgreSQL for marketplace and user data.
- Use managed Redis for session caching and real-time features.
- Deploy a reverse proxy (nginx) in front of the application.
- Use TLS certificates from Let's Encrypt or your cloud provider's certificate manager.
- Enable auto-scaling for compute resources based on user load.
- Use environment variables for all configuration (never hardcode secrets).

---

## Configuration Management

### Configuration Hierarchy

Configuration is loaded in order of precedence (highest first):

1. **Environment variables** — Override all other sources.
2. **User config** (`~/.scilab-studio/config.json`) — Per-user settings.
3. **Project config** (`.scilab-studio/project.json`) — Per-project settings.
4. **Default config** (bundled with application) — Fallback defaults.

### Configuration File Locations

| Platform | Location |
|----------|----------|
| Linux | `~/.scilab-studio/config.json` |
| macOS | `~/Library/Application Support/Scilab Studio/config.json` |
| Windows | `%APPDATA%\Scilab Studio\config.json` |
| Server | `/app/config/config.json` (Docker) or `$SCILAB_STUDIO_CONFIG` |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCILAB_PATH` | Auto-detect | Path to Scilab binary |
| `SCILAB_VERSION` | Auto-detect | Required Scilab version |
| `NODE_ENV` | `development` | Environment mode |
| `PORT` | `3000` | Application port |
| `API_PORT` | `8080` | API port |
| `DATABASE_URL` | `sqlite://local.db` | Database connection string |
| `REDIS_URL` | — | Redis connection string |
| `LOG_LEVEL` | `info` | Logging level |
| `SESSION_SECRET` | — | Secret for session encryption |
| `JWT_SECRET` | — | Secret for JWT tokens |
| `SCILAB_STUDIO_CONFIG` | Platform default | Custom config path |
| `SCILAB_STUDIO_DATA` | Platform default | Custom data directory |
| `MAX_SESSIONS` | `4` | Max concurrent Scilab sessions |
| `SESSION_TIMEOUT` | `300000` | Session timeout (ms) |
| `MARKETPLACE_URL` | `https://marketplace.scilab-studio.org` | Marketplace endpoint |
| `TELEMETRY` | `false` | Enable anonymous telemetry |
| `HTTP_PROXY` | — | HTTP proxy server |
| `HTTPS_PROXY` | — | HTTPS proxy server |

---

## Database Setup

### PostgreSQL (for web/cloud deployments)

```sql
-- Create database and user
CREATE USER scilab WITH PASSWORD 'secure_password';
CREATE DATABASE scilab_studio OWNER scilab;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE scilab_studio TO scilab;

-- Connect and create tables
\c scilab_studio

-- The application runs migrations automatically on startup
```

### SQLite (for desktop)

No setup required. The database file is created automatically at:
- `~/.scilab-studio/scilab-studio.db` (Linux/macOS)
- `%APPDATA%\Scilab Studio\scilab-studio.db` (Windows)

---

## Scilab Engine Installation

### Desktop
The Setup Wizard will help locate or install Scilab. You can also set the path manually:

```
Settings > Engine > Scilab Path: /usr/local/bin/scilab
```

### Server/Cloud (Docker)

Scilab is included in the official Docker image. For custom builds:

```dockerfile
FROM ubuntu:22.04

# Install Scilab
RUN apt-get update && apt-get install -y \
    scilab \
    && rm -rf /var/lib/apt/lists/*

# Verify
RUN scilab -version
```

### Multiple Scilab Versions

For environments requiring multiple Scilab versions:

```bash
# Install multiple versions
/usr/local/scilab-2024.0/bin/scilab
/usr/local/scilab-2023.1/bin/scilab

# Configure per-project
# In project.json:
{
  "settings": {
    "scilabVersion": "2024.0"
  }
}
```

---

## Plugin Installation

### Desktop
1. Open Settings > Plugins.
2. Browse the Marketplace or select "Install from File."
3. Click Install.

### Server
```bash
# Via CLI
scilab-studio plugin install plugin-thermal-analysis@2.0.0

# Via API
curl -X POST http://localhost:8080/v1/plugins \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"source": "marketplace", "packageId": "plugin-thermal-analysis", "version": "2.0.0"}'
```

### Docker
Add plugins to a `plugins/` volume or install at build time:

```dockerfile
RUN scilab-studio plugin install plugin-thermal-analysis@2.0.0
```

---

## Update Mechanism

### Desktop
- **Auto-update:** Enabled by default. Checks for updates on launch.
- **Manual update:** Help > Check for Updates.
- **Disable auto-update:** Settings > General > Auto Update: Off.

### Server
```bash
# Pull latest image
docker pull scilab-studio/server:latest

# Restart with new image
docker-compose up -d
```

### Database Migrations
Migrations run automatically on application startup. Backup your database before major version upgrades.

---

## Backup and Recovery

### Desktop
```bash
# Backup configuration and data
tar -czf scilab-studio-backup-$(date +%Y%m%d).tar.gz \
  ~/.scilab-studio/

# Restore
tar -xzf scilab-studio-backup-YYYYMMDD.tar.gz -C ~/
```

### Server
```bash
# Database backup
pg_dump -U scilab scilab_studio > backup_$(date +%Y%m%d).sql

# Full backup (database + files)
docker exec scilab-studio pg_dump -U scilab scilab_studio > db_backup.sql
tar -czf files_backup.tar.gz /app/data /app/projects

# Restore database
psql -U scilab scilab_studio < backup_YYYYMMDD.sql
```

### Automated Backups
```bash
# Cron job for daily backups (add to crontab)
0 2 * * * pg_dump -U scilab scilab_studio | gzip > /backups/scilab_$(date +\%Y\%m\%d).sql.gz
```

---

## Monitoring

### Health Check Endpoints

```
GET /health          # Basic health check
GET /health/ready    # Readiness check (all services connected)
GET /health/live     # Liveness check (process is running)
```

### Metrics

Exposed via Prometheus format at `/metrics`:

| Metric | Description |
|--------|-------------|
| `scilab_studio_requests_total` | Total HTTP requests |
| `scilab_studio_request_duration` | Request latency histogram |
| `scilab_studio_active_sessions` | Active Scilab sessions |
| `scilab_studio_engine_executions` | Total code executions |
| `scilab_studio_memory_usage` | Memory consumption |
| `scilab_studio_cpu_usage` | CPU consumption |

### Logging

Logs are structured JSON by default:

```json
{
  "level": "info",
  "message": "Project opened",
  "timestamp": "2026-01-15T10:30:00Z",
  "projectId": "proj_abc123",
  "userId": "user_xyz",
  "duration": 0.23
}
```

### Alerting

Recommended alerts:
- Application down (health check fails for > 1 minute)
- High memory usage (> 80% for > 5 minutes)
- Error rate spike (> 5% of requests returning 5xx)
- Scilab engine unresponsive
- Disk usage > 85%

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Application won't start | Check logs in `~/.scilab-studio/logs/`. Verify Scilab engine path. |
| Scilab engine not found | Set `SCILAB_PATH` environment variable or configure in Settings. |
| Port already in use | Change the port via `PORT` environment variable or config file. |
| Database connection failed | Check `DATABASE_URL`. Ensure PostgreSQL is running. |
| Plugin won't load | Check plugin manifest syntax. Review plugin logs. Verify dependencies. |
| Slow performance | Check Scilab engine version. Reduce dataset size. Check system resources. |
| WebSocket connection issues | Verify nginx proxy_pass includes WebSocket headers. |
| Permission denied (Linux) | Check file permissions on `~/.scilab-studio/`. Run `chmod -R 755 ~/.scilab-studio/`. |
| Docker container exits | Check container logs: `docker logs scilab-studio`. Verify environment variables. |
| Auto-update fails | Check network connectivity. Verify write permissions on install directory. |
