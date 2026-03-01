# Kustomize Demo Project — Full Walkthrough

Demo code for the YouTube video: **"What is Kustomize? Kubernetes Config Management (2026)"**

---

## Project Structure

```
demo/
├── base/                        ← Shared source of truth
│   ├── kustomization.yaml       ← Index + transformers
│   ├── namespace.yaml
│   ├── deployment.yaml          ← 1 replica, dev-sized resources
│   └── service.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml   ← dev image tag, debug log level
    │   └── patch-replicas.yaml  ← 1 replica
    ├── staging/
    │   ├── kustomization.yaml   ← rc image tag
    │   └── patch-replicas.yaml  ← 2 replicas
    └── prod/
        ├── kustomization.yaml   ← pinned v1.4.2, namespace override
        ├── patch-replicas.yaml  ← 5 replicas
        └── patch-resources.yaml ← prod-sized CPU/memory
```

---

## Prerequisites

- kubectl >= 1.14 (kustomize built-in) OR kustomize CLI standalone
- A Kubernetes cluster (minikube, kind, or any cloud cluster)

### Install kustomize standalone (optional)

```bash
# macOS
brew install kustomize

# Linux
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/

# Verify
kustomize version
# v5.4.0
```

---

## Quick Start

### 1. Preview the merged YAML (no cluster needed)

```bash
# See what kustomize generates for each environment
kubectl kustomize overlays/dev
kubectl kustomize overlays/staging
kubectl kustomize overlays/prod

# Or with the standalone CLI
kustomize build overlays/prod
```

### 2. Compare environments side by side

```bash
# Compare dev vs prod output
diff <(kubectl kustomize overlays/dev) <(kubectl kustomize overlays/prod)
```

**Expected diff output:**
- `replicas: 1` → `replicas: 5`
- `image: ...webapp:dev-abc1234` → `...webapp:v1.4.2`
- `cpu: "100m"` → `cpu: "500m"` (and limits added)
- `ENV=development` → `ENV=production`

### 3. Apply to a cluster

```bash
# Apply dev overlay
kubectl apply -k overlays/dev

# Apply prod overlay
kubectl apply -k overlays/prod

# Verify
kubectl get deployments -n webapp
kubectl get configmaps -n webapp     # notice the hash suffix!
```

### 4. Check what would change (diff against live cluster)

```bash
# Shows the diff between what's running and what kustomize would apply
kubectl diff -k overlays/prod
```

---

## Key Concepts Demonstrated

### Base (overlays/base/)
- Standard, valid Kubernetes YAML — no template syntax
- `kustomization.yaml` registers resources and defines transformers
- `commonLabels` and `commonAnnotations` inject metadata into ALL resources
- `images[]` defines the image name placeholder

### Overlays (overlays/*)
- Each overlay references the base via `bases: [../../base]`
- Only specifies what **changes** — not the full manifest
- `patch-replicas.yaml` is a Strategic Merge Patch — 3 lines replaces 100

### Strategic Merge Patches
Kustomize supports two patch types:
1. **Strategic Merge Patch** (used here) — write a partial object, Kustomize merges it
2. **JSON Patch (RFC 6902)** — explicit `op: replace` instructions, more precise

### ConfigMapGenerator
The generated ConfigMap name gets a content hash appended:
```
app-env-7g4k2m8f   ← hash changes when content changes → forces pod rollout
```
This solves the silent "stale config" problem where pods keep running with old environment variables.

---

## ArgoCD Integration

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: webapp-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/k8s-configs
    targetRevision: main
    path: overlays/prod          # ← point to the overlay directory
    kustomize:
      version: v5.4.0
      images:
        - registry.example.com/webapp:v2.0.0  # override image at deploy time
  destination:
    server: https://kubernetes.default.svc
    namespace: webapp-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Apply with:
```bash
kubectl apply -f argocd-application.yaml -n argocd
argocd app sync webapp-prod
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `no such file or directory` when running `apply -k` | Make sure you're pointing at the overlay directory, not a YAML file |
| Resource not patched | Verify the patch has the same `name` as the base resource |
| ConfigMap not updating pods | Kustomize hash works only with `configMapGenerator`, not manually created ConfigMaps |
| `bases` field deprecated warning | In kustomize v5+, use `resources` instead of `bases` |
