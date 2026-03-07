# Deployment Strategies — Demo Files

> Source code for: **"Blue-Green vs Canary vs Rolling — Which Deploy Strategy Should You Use?"**

## Files

| File | Strategy | Traffic Split |
|------|----------|--------------|
| `rolling-deployment.yaml` | Rolling | Gradual pod-by-pod replacement |
| `blue-green-deployment.yaml` | Blue-Green | Instant 0%→100% flip via Service selector |
| `canary-deployment.yaml` | Canary | Controlled % split via replica ratio |

## Prerequisites

- kubectl installed and connected to a cluster
- Local cluster: [minikube](https://minikube.sigs.k8s.io/) or [kind](https://kind.sigs.k8s.io/)

```bash
# Start a local cluster (pick one)
minikube start
# OR
kind create cluster
```

---

## Rolling Deploy

```bash
# Deploy
kubectl apply -f rolling-deployment.yaml

# Trigger a rolling update (change image tag)
kubectl set image deployment/my-app nginx=nginx:1.26

# Watch live
kubectl rollout status deployment/my-app

# Rollback
kubectl rollout undo deployment/my-app
```

---

## Blue-Green Deploy

```bash
# Deploy both blue and green (blue is live)
kubectl apply -f blue-green-deployment.yaml

# Test green internally — no user traffic
kubectl port-forward deployment/my-app-green 8080:80
curl http://localhost:8080/

# Flip traffic to green (instant)
kubectl patch service my-app -p '{"spec":{"selector":{"slot":"green"}}}'

# Rollback — flip back to blue
kubectl patch service my-app -p '{"spec":{"selector":{"slot":"blue"}}}'

# After confirming green is stable, scale down blue
kubectl scale deployment my-app-blue --replicas=0
```

---

## Canary Deploy

```bash
# Start: 5% canary (1 of 20 pods)
kubectl apply -f canary-deployment.yaml

# Watch pod distribution
kubectl get pods -l app=my-app

# Promote to 25%
kubectl scale deployment my-app-canary --replicas=5
kubectl scale deployment my-app-stable --replicas=15

# Promote to 50%
kubectl scale deployment my-app-canary --replicas=10
kubectl scale deployment my-app-stable --replicas=10

# Full cutover
kubectl scale deployment my-app-canary --replicas=20
kubectl scale deployment my-app-stable --replicas=0

# Rollback at any stage
kubectl scale deployment my-app-canary --replicas=0
kubectl scale deployment my-app-stable --replicas=20
```

---

## Quick Decision Guide

```
Is your change backward-compatible?
  YES → Rolling (default, zero config)
  NO  → Is instant rollback critical?
          YES → Blue-Green
          NO  → Is the change high-risk with a large user base?
                  YES → Canary
                  NO  → Blue-Green
```
