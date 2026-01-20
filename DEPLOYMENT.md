# Deployment Guide - Unified E-Commerce System

## 🌐 Deployment Options

This guide covers multiple ways to deploy the Unified E-Commerce System.

---

## 1️⃣ Streamlit Cloud (Recommended - Easiest)

### Prerequisites
- GitHub account
- Streamlit account (free at share.streamlit.io)
- Code pushed to GitHub

### Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repository
   - Select branch: `main`
   - File path: `app.py`
   - Click "Deploy"

3. **Configure Environment Variables** (if needed)
   - Go to Advanced Settings
   - Add any required environment variables

### Advantages
- ✅ Free tier available
- ✅ Automatic deployment from GitHub
- ✅ Custom domain support
- ✅ Built-in HTTPS
- ✅ No server management

### Disadvantages
- Limited computational resources on free tier
- Slower cold starts
- Public repository required (unless paid plan)

---

## 2️⃣ Docker Deployment

### Prerequisites
- Docker installed
- Docker Hub account (optional, for public images)

### Local Docker

```bash
# Build image
docker build -t ecommerce-app:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  ecommerce-app:latest

# Or with Docker Compose
docker-compose up
```

### Docker Hub

```bash
# Build with tag
docker build -t yourusername/ecommerce-app:latest .

# Push to Docker Hub
docker push yourusername/ecommerce-app:latest

# Pull and run anywhere
docker pull yourusername/ecommerce-app:latest
docker run -p 8501:8501 yourusername/ecommerce-app:latest
```

### Advantages
- ✅ Consistent environments
- ✅ Easy deployment across platforms
- ✅ Version control
- ✅ Easy scaling

---

## 3️⃣ Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Code in Git repository

### Steps

1. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = \$PORT\n\
   enableCORS = false\n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **View logs**
   ```bash
   heroku logs --tail
   ```

### Advantages
- ✅ Simple Git-based deployment
- ✅ Free dyno option
- ✅ Automatic scaling
- ✅ Built-in PostgreSQL support

### Disadvantages
- ❌ Dynos go to sleep after 30 mins (free tier)
- ❌ Monthly dyno hours limit
- ❌ Performance limitations on free tier

---

## 4️⃣ AWS EC2 Deployment

### Prerequisites
- AWS account
- EC2 instance running Ubuntu
- SSH access to instance

### Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance type: t2.medium or larger
   - Storage: 20GB+ EBS
   - Security group: Allow ports 80, 443, 22, 8501

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-dev git
   pip3 install --upgrade pip
   ```

4. **Clone repository**
   ```bash
   git clone your-repo-url
   cd unified_ecommerce_app
   pip3 install -r requirements.txt
   ```

5. **Run with Gunicorn and Nginx** (for production)

   a. Install Gunicorn
   ```bash
   pip3 install gunicorn
   ```

   b. Create systemd service file
   ```bash
   sudo tee /etc/systemd/system/ecommerce.service > /dev/null <<EOF
   [Unit]
   Description=Unified E-Commerce System
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/unified_ecommerce_app
   ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

   c. Start service
   ```bash
   sudo systemctl start ecommerce
   sudo systemctl enable ecommerce
   ```

6. **Setup Nginx reverse proxy**
   ```bash
   sudo apt install -y nginx
   
   sudo tee /etc/nginx/sites-available/ecommerce > /dev/null <<EOF
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host \$host;
           proxy_set_header X-Real-IP \$remote_addr;
       }
   }
   EOF
   
   sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

### Advantages
- ✅ Full control
- ✅ Cost-effective
- ✅ Good performance
- ✅ Scalability options

---

## 5️⃣ Google Cloud Platform (GCP)

### Using App Engine

```bash
# Create app.yaml
cat > app.yaml <<EOF
runtime: python39
env: standard
handlers:
- url: /.*
  secure: always
  redirect_http_response_code: 301
  script: auto
EOF

# Deploy
gcloud app deploy
```

### Using Cloud Run (Recommended)

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ecommerce-app

# Deploy
gcloud run deploy ecommerce-app \
  --image gcr.io/PROJECT_ID/ecommerce-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Advantages
- ✅ Serverless (less management)
- ✅ Auto-scaling
- ✅ Pay per use
- ✅ Google ecosystem integration

---

## 6️⃣ Azure Deployment

### Using App Service

```bash
# Install Azure CLI
# Then login
az login

# Create resource group
az group create --name ecommerce-rg --location eastus

# Create app service plan
az appservice plan create --name ecommerce-plan \
  --resource-group ecommerce-rg --sku B1 --is-linux

# Deploy
az webapp create --resource-group ecommerce-rg \
  --plan ecommerce-plan --name ecommerce-app \
  --runtime "PYTHON|3.9"

# Push code
git remote add azure <git-clone-url>
git push azure main
```

### Advantages
- ✅ Tight integration with Microsoft stack
- ✅ Good for enterprise
- ✅ Free tier available

---

## 7️⃣ DigitalOcean Deployment

### Using App Platform

1. **Create app.yaml**
   ```yaml
   name: ecommerce-app
   services:
   - name: web
     github:
       repo: username/ecommerce-repo
       branch: main
     build_command: pip install -r requirements.txt
     run_command: streamlit run app.py --server.port 8080
     envs:
     - key: STREAMLIT_SERVER_PORT
       value: "8080"
   ```

2. **Deploy**
   - Go to DigitalOcean Dashboard
   - Create new App
   - Connect GitHub repository
   - Deploy

### Using Droplet

```bash
# Create droplet and SSH in
ssh root@your-droplet-ip

# Install Python and dependencies
apt update && apt install -y python3-pip git

# Clone and setup
git clone your-repo
cd unified_ecommerce_app
pip3 install -r requirements.txt

# Run with systemd
# (Similar to AWS EC2 steps above)
```

### Advantages
- ✅ Affordable
- ✅ Straightforward
- ✅ 24/7 support
- ✅ Good documentation

---

## ⚙️ Production Best Practices

### Environment Variables
```bash
# Create .env file
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
PYTHONUNBUFFERED=1
```

### Security
- Use HTTPS (via Nginx, CloudFlare, or cloud provider)
- Keep dependencies updated
- Use environment variables for sensitive data
- Implement rate limiting
- Add authentication if needed

### Monitoring
```bash
# Setup log aggregation
# Monitor CPU and memory usage
# Setup alerts for errors
# Track user analytics
```

### Performance
- Use CDN for static files
- Cache Prophet models
- Optimize CSV file sizes
- Use pagination for large datasets

---

## 📊 Cost Comparison

| Platform | Free Tier | Startup Cost | Scaling |
|----------|-----------|--------------|---------|
| Streamlit Cloud | Yes | Free | Auto |
| Heroku | Limited | $0-7/month | Manual |
| AWS EC2 | 12 months | $0.0116/hour | Manual |
| GCP Cloud Run | 2M requests | Pay per use | Auto |
| Azure | $200 credit | Free tier | Auto |
| DigitalOcean | No | $5/month | Manual |
| Docker Local | N/A | Server cost | Manual |

---

## 🚀 Recommended Setup by Scenario

### For Development
```bash
Local machine or Docker
```

### For Small Projects (Low Traffic)
```
Streamlit Cloud (free) or Heroku
```

### For Medium Projects
```
Docker on AWS EC2 t2.medium
or GCP Cloud Run
```

### For Enterprise
```
Kubernetes cluster on AWS/GCP/Azure
with proper monitoring and CI/CD
```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Environment variables configured
- [ ] CSV data files accessible
- [ ] Secrets not in code (use .env)
- [ ] Error handling implemented
- [ ] Logging setup
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Domain name configured
- [ ] SSL/HTTPS enabled
- [ ] Backups configured
- [ ] Monitoring/alerts setup

---

## 🔧 Troubleshooting Deployment

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Memory issues
```bash
# Increase available memory or reduce data size
# Use data pagination
```

### Slow startup
```bash
# Prophet takes time on first run
# Consider model caching
```

### CSV file not found
```bash
# Ensure data directory is mounted/copied
# Check file permissions
```

---

## 📚 Additional Resources

- [Streamlit Deployment Documentation](https://docs.streamlit.io/streamlit-cloud/get-started)
- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Heroku Deployment Guide](https://devcenter.heroku.com/)

---

**Happy Deploying! 🚀**
