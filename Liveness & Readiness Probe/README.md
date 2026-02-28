# Kubernetes Probes Demo

Live demo for the YouTube video: **"Kubernetes Probes: Liveness vs Readiness"**

## What this demo shows

| Probe | Endpoint | On Failure |
|---|---|---|
| **Liveness** | `GET /healthz` | Pod **restarts** |
| **Readiness** | `GET /readyz` | Pod **removed from load balancer** |
| **Startup** | `GET /healthz` | Liveness/Readiness **disabled** until passes |

---

## Prerequisites

- Docker Desktop or a local Docker daemon
- A Kubernetes cluster (`minikube`, `kind`, `k3d`, or any cloud cluster)
- `kubectl` configured

---

## Quick Start

### 1. Build the Docker image

```bash
cd demo/
docker build -t probes-demo:latest .
```

If using **minikube**:
```bash
eval $(minikube docker-env)
docker build -t probes-demo:latest .
```

If using **kind**:
```bash
docker build -t probes-demo:latest .
kind load docker-image probes-demo:latest
kind load docker-image probes-demo:latest --name <Cluster name>
```

---

### 2. Deploy to Kubernetes

```bash
kubectl apply -f deployment.yaml
```

Watch pods come up:
```bash
kubectl get pods -w -l app=probes-demo
```

You'll see the pod stay in `0/1 Running` for ~10 seconds (readiness warming up), then flip to `1/1 Running`.

---

### 3. Demo: Watch Liveness Failure → Pod Restart

Open two terminals:

**Terminal 1** — Watch pods:
```bash
kubectl get pods -w -l app=probes-demo
```

**Terminal 2** — Trigger liveness failure:
```bash
# Get the pod name
POD=$(kubectl get pod -l app=probes-demo -o jsonpath='{.items[0].metadata.name}')

# Trigger liveness failure (app now returns 500 on /healthz)
kubectl exec -it $POD -- curl -s localhost:8080/kill
kubectl exec -it $POD -- python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8080/kill').read())"
```

Watch Terminal 1: after 30 seconds (3 failures × 10s period), Kubernetes restarts the pod. The `RESTARTS` counter increments.

---

### 4. Demo: Watch Readiness — Pod Removed from Traffic

```bash
# Port-forward the service
kubectl port-forward svc/probes-demo-svc 8080:80 &

# While app is starting, watch readiness fail
curl -s localhost:8080/readyz | python3 -m json.tool
```

During the 10-second warmup window you'll see:
```json
{
  "status": "not_ready",
  "reason": "warming_up",
  "message": "App is warming up. Ready in ~7s"
}
```

After 10s, it becomes ready and traffic is routed to the pod.

---

### 5. Inspect Probe Events

```bash
kubectl describe pod -l app=probes-demo
```

Look for events like:
```
Liveness probe failed: HTTP probe failed with statuscode: 500
Killing container with a grace period override of 1
```

---

## Cleanup

```bash
kubectl delete -f deployment.yaml
```

---

## File Structure

```
demo/
├── app.py            # Flask app with /healthz, /readyz, /kill, /reset
├── Dockerfile        # Multi-stage Docker build
├── requirements.txt  # Python dependencies
├── deployment.yaml   # K8s Deployment + Service with all 3 probes
└── README.md         # This file
```

---

## Key YAML Parameters Reference

| Parameter | Liveness | Readiness | Notes |
|---|---|---|---|
| `initialDelaySeconds` | 15 | 5 | How long to wait before first probe |
| `periodSeconds` | 10 | 5 | How often to probe |
| `timeoutSeconds` | 5 | 3 | Max time to wait for response |
| `failureThreshold` | 3 | 3 | Failures before action taken |
| `successThreshold` | 1 | 1 | Successes to consider healthy |
