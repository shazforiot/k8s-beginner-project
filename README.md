# Kubernetes Beginner Project

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=shazforiot_k8s-beginner-project&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=shazforiot_k8s-beginner-project)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=shazforiot_k8s-beginner-project&metric=bugs)](https://sonarcloud.io/summary/new_code?id=shazforiot_k8s-beginner-project)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=shazforiot_k8s-beginner-project&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=shazforiot_k8s-beginner-project)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=shazforiot_k8s-beginner-project&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=shazforiot_k8s-beginner-project)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=shazforiot_k8s-beginner-project&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=shazforiot_k8s-beginner-project)

A complete, production-ready Kubernetes demo project for beginners. Learn K8s by deploying a real application!

## Project Structure

```
k8s-beginner-project/
├── app/
│   ├── index.js          # Node.js application
│   └── package.json      # Dependencies
├── k8s/
│   ├── namespace.yaml    # Namespace definition
│   ├── configmap.yaml    # Configuration data
│   ├── deployment.yaml   # Pod deployment
│   ├── service.yaml      # Service exposure
│   ├── ingress.yaml      # HTTP routing (optional)
│   └── hpa.yaml          # Auto-scaling (optional)
├── .github/
│   └── workflows/
│       └── ci-cd.yaml    # GitHub Actions pipeline
├── Dockerfile            # Container image
└── README.md
```

## Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled
- OR [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) CLI

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/k8s-beginner-project.git
cd k8s-beginner-project
```

### 2. Build Docker Image (Local)

```bash
# Build the image
docker build -t k8s-demo-app:latest .

# Test locally
docker run -p 3000:3000 k8s-demo-app:latest
# Visit http://localhost:3000
```

### 3. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy all resources
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get all -n k8s-demo
```

### 4. Access the Application

```bash
# For LoadBalancer (Docker Desktop)
kubectl get svc -n k8s-demo
# Access via EXTERNAL-IP:80

# For Minikube
minikube service k8s-demo-service -n k8s-demo
```

## Kubernetes Concepts Covered

| File | Concept | Description |
|------|---------|-------------|
| `namespace.yaml` | Namespace | Logical isolation of resources |
| `configmap.yaml` | ConfigMap | External configuration storage |
| `deployment.yaml` | Deployment | Pod management & rolling updates |
| `service.yaml` | Service | Load balancing & service discovery |
| `ingress.yaml` | Ingress | HTTP/HTTPS routing |
| `hpa.yaml` | HPA | Horizontal Pod Autoscaling |

## Common Commands

### View Resources

```bash
# All resources in namespace
kubectl get all -n k8s-demo

# Pods with more details
kubectl get pods -n k8s-demo -o wide

# Watch pods in real-time
kubectl get pods -n k8s-demo -w
```

### Debugging

```bash
# Pod logs
kubectl logs -f <pod-name> -n k8s-demo

# Describe pod (events, status)
kubectl describe pod <pod-name> -n k8s-demo

# Execute command in pod
kubectl exec -it <pod-name> -n k8s-demo -- sh
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment k8s-demo-app -n k8s-demo --replicas=5

# Check HPA status (if enabled)
kubectl get hpa -n k8s-demo
```

### Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete namespace (removes everything)
kubectl delete namespace k8s-demo
```

## CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Build & Test** - Node.js build and tests
2. **Docker Build** - Multi-arch image (amd64/arm64)
3. **Security Scan** - Trivy vulnerability scanning
4. **Deploy** - Automatic deployment to K8s cluster

### Setup CI/CD

1. **Enable GitHub Packages** - Repository Settings → Actions → General

2. **Add Secrets** (Settings → Secrets → Actions):
   - `KUBE_CONFIG` - Base64 encoded kubeconfig file

3. **Get Kubeconfig**:
   ```bash
   cat ~/.kube/config | base64
   ```

## Free Kubernetes Platforms

| Platform | Credits | Best For |
|----------|---------|----------|
| [Killercoda](https://killercoda.com) | Free | Instant playground |
| [Google Cloud (GKE)](https://cloud.google.com/free) | $300 | Production-like |
| [Oracle Cloud (OKE)](https://www.oracle.com/cloud/free/) | Always Free | Long-term learning |
| [Civo](https://www.civo.com) | $250 | Fast K3s clusters |
| [Linode](https://www.linode.com) | $100 | Simple setup |

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main page with app info |
| `/health` | Liveness probe endpoint |
| `/ready` | Readiness probe endpoint |
| `/info` | Detailed app information (JSON) |

## Best Practices Implemented

- [x] Non-root container user
- [x] Resource limits (CPU/Memory)
- [x] Health checks (liveness/readiness)
- [x] Rolling update strategy
- [x] Security context
- [x] ConfigMap for configuration
- [x] Multi-stage Docker build
- [x] Graceful shutdown handling

## Next Steps

1. **Add Secrets** - Store sensitive data securely
2. **Add Persistent Storage** - PersistentVolumeClaims
3. **Add Network Policies** - Control pod-to-pod traffic
4. **Add Monitoring** - Prometheus + Grafana
5. **Add Service Mesh** - Istio or Linkerd

## License

MIT License - Feel free to use for learning!

---

**Questions?** Open an issue or reach out!
