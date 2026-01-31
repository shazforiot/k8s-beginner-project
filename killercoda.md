# Deploy to Killercoda (Free K8s Playground)

Killercoda provides a free, browser-based Kubernetes cluster. No signup required!

## Quick Start

### 1. Open Killercoda Playground

👉 **https://killercoda.com/playgrounds/scenario/kubernetes**

---

### 2. Deploy with Kustomize (Recommended)

```bash
# Clone the repo
git clone https://github.com/shazforiot/k8s-beginner-project.git
cd k8s-beginner-project

# Deploy all resources with Kustomize
kubectl apply -k k8s/

# Watch pods come up (Ctrl+C when all Running)
kubectl get pods -n k8s-demo -w
```

---

### 3. Access the Application

```bash
# Port forward to access the app
kubectl port-forward svc/k8s-demo-service 8080:80 -n k8s-demo --address 0.0.0.0 &

# Test with curl
curl localhost:8080

# Or view JSON info
curl localhost:8080/info
```

**Browser Access:** Click **"Traffic / Ports"** tab in Killercoda → Add port `8080`

---

## One-Liner (Copy & Paste)

```bash
git clone https://github.com/shazforiot/k8s-beginner-project.git && cd k8s-beginner-project && kubectl apply -k k8s/ && sleep 15 && kubectl get pods -n k8s-demo && kubectl port-forward svc/k8s-demo-service 8080:80 -n k8s-demo --address 0.0.0.0
```

---

## Alternative: Deploy Without Kustomize

```bash
git clone https://github.com/shazforiot/k8s-beginner-project.git
cd k8s-beginner-project

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## Useful Commands

### Check Resources

```bash
# All resources in namespace
kubectl get all -n k8s-demo

# Pods with details
kubectl get pods -n k8s-demo -o wide

# Services
kubectl get svc -n k8s-demo
```

### Debugging

```bash
# Pod logs
kubectl logs -f deployment/k8s-demo-app -n k8s-demo

# Describe pod
kubectl describe pod -l app=k8s-demo -n k8s-demo

# Exec into pod
kubectl exec -it deployment/k8s-demo-app -n k8s-demo -- sh
```

### Scaling

```bash
# Scale to 5 replicas
kubectl scale deployment k8s-demo-app -n k8s-demo --replicas=5

# Watch scaling
kubectl get pods -n k8s-demo -w
```

### Test Self-Healing

```bash
# Delete a pod and watch K8s recreate it
kubectl delete pod -l app=k8s-demo -n k8s-demo --wait=false
kubectl get pods -n k8s-demo -w
```

---

## Cleanup

```bash
# Delete all resources
kubectl delete -k k8s/

# Or delete namespace (removes everything)
kubectl delete namespace k8s-demo
```

---

## Expected Output

When you access the app, you'll see:

```
☸️ K8s Demo App
Version: 1.0.0
Running on Kubernetes!

Hostname: k8s-demo-app-xxxxx-xxxxx
Platform: linux
```

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main page (HTML) |
| `/health` | Liveness probe |
| `/ready` | Readiness probe |
| `/info` | App info (JSON) |

---

## Why Kustomize?

Kustomize is built into kubectl and lets you:

- ✅ Deploy all YAML files with one command
- ✅ Override images, labels, namespaces
- ✅ No extra tools needed (`kubectl apply -k`)

```bash
# Instead of applying each file:
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Just run:
kubectl apply -k k8s/
```

---

## Troubleshooting

### Pods stuck in Pending
```bash
kubectl describe pod -l app=k8s-demo -n k8s-demo
```

### ImagePullBackOff
```bash
# Check if image is accessible
kubectl get events -n k8s-demo
```

### Port forward not working
```bash
# Kill existing port-forward and retry
pkill -f "port-forward"
kubectl port-forward svc/k8s-demo-service 8080:80 -n k8s-demo --address 0.0.0.0
```

---

Happy Learning! 🚀
