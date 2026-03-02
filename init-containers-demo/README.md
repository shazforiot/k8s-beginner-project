# Demo: Init Containers — Kubernetes Feature

Three production-ready patterns demonstrated live in the video.

## Prerequisites

- Kubernetes cluster (local: `minikube`, `kind`, or `k3d`)
- `kubectl` configured and connected
- `kubens` / `kubectx` recommended

---

## Demo 1 — Wait for Service

**Goal:** App container waits for MySQL DNS to resolve before starting.

```bash
cd demo/01-wait-for-service

# Apply the pod
kubectl apply -f pod.yaml

# Watch init container in action
kubectl get pod webapp -w
# STATUS: Init:0/1 → PodInitializing → Running

# Read init container logs
kubectl logs webapp -c wait-for-mysql

# Clean up
kubectl delete -f pod.yaml
```

**What to observe:**
- Status `Init:0/1` while init container polls
- Status transitions to `Running` only after DNS resolves
- If MySQL is never deployed, init loops indefinitely (intentional)

---

## Demo 2 — Database Migrations

**Goal:** Run schema migrations before any app replica starts serving traffic.

```bash
cd demo/02-db-migration

# 1. Create the database secret
kubectl create secret generic db-credentials \
  --from-literal=url="postgres://myuser:mypassword@postgres-service:5432/mydb"

# 2. Apply migrations ConfigMap
kubectl apply -f configmap.yaml

# 3. Deploy the app (init container runs migrations first)
kubectl apply -f deployment.yaml

# 4. Watch all 3 replicas come up sequentially through init
kubectl get pods -w

# 5. Check migration logs on one pod
kubectl logs deploy/webapp -c run-db-migration

# Clean up
kubectl delete -f deployment.yaml -f configmap.yaml
kubectl delete secret db-credentials
```

**What to observe:**
- All 3 replicas run init containers before app starts
- Migration output visible in init container logs
- App containers start only after migrations succeed

---

## Demo 3 — Config & Secret Injection

**Goal:** Inject runtime config into app via shared in-memory volume.

```bash
cd demo/03-config-setup

# 1. Create config token secret
kubectl create secret generic config-credentials \
  --from-literal=token="demo-token-12345"

# 2. Create ServiceAccount (replace with your cluster's SA)
kubectl create serviceaccount vault-reader

# 3. Deploy
kubectl apply -f deployment.yaml

# 4. Watch init container fetch and write config
kubectl logs deploy/config-app -c setup-config

# 5. Verify app can read the config
kubectl exec deploy/config-app -- cat /etc/myapp/config/app.json

# Clean up
kubectl delete -f deployment.yaml
kubectl delete secret config-credentials
kubectl delete serviceaccount vault-reader
```

**What to observe:**
- Config volume is in-memory (`emptyDir: memory`) — never hits disk
- App container is `readOnly: true` on the config volume
- App image contains zero secrets

---

## Quick Reference: Init Container kubectl Commands

```bash
# Check init container status
kubectl get pod <pod-name>
# STATUS column: Init:0/N = N init containers, 0 complete

# Describe pod — shows init container details
kubectl describe pod <pod-name>

# Logs from running/completed init container
kubectl logs <pod-name> -c <init-container-name>

# Logs from previously failed init container
kubectl logs <pod-name> -c <init-container-name> --previous

# Watch pod lifecycle in real time
kubectl get pod <pod-name> -w
```

---

## Key Points Covered

| Pattern | Image Used | Use Case |
|---------|-----------|----------|
| Wait for service | `busybox:1.36` | Poll DNS/TCP until ready |
| DB migrations | `migrate/migrate:v4.17.0` | Schema changes before app start |
| Config injection | `alpine:3.19` | Fetch secrets, write to shared volume |
