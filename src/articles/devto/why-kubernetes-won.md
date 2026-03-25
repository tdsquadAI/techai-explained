---
title: "Why Kubernetes Won — And What's Coming Next"
description: "Kubernetes crushed Docker Swarm, Mesos, and Nomad. Here's the three reasons it won so completely, the problems it still hasn't solved, and the three technologies reshaping container orchestration by 2028."
tags: ["kubernetes", "devops", "cloudnative", "platformengineering"]
canonical_url: https://tamirdresher.github.io/techai-explained/articles/why-kubernetes-won/
published: false
---

In 2014, Kubernetes was a Google side project. By 2020, it ran most of the internet's infrastructure. Docker Swarm is effectively dead. Mesos was archived. Even Nomad, the best alternative, is a niche tool.

How did Kubernetes win so completely? And more importantly — is it still the right choice for what's coming next?

## Why Kubernetes Won

Three factors combined to make Kubernetes unstoppable.

### Factor 1: The Declarative API Model

Kubernetes' killer feature isn't containers — it's the **declarative API model**.

You describe desired state, the system reconciles to that state. This turned out to be the right abstraction for infrastructure at scale.

Compare the two approaches:

```bash
# Docker Swarm: imperative command
docker service create --replicas 3 nginx

# Kubernetes: declarative manifest
# (desired state — system figures out how to get there)
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
```

Docker Swarm let you run containers. Kubernetes let you define your entire infrastructure as code and extend it infinitely. That's the difference between a tool and a platform.

Custom Resource Definitions (CRDs) let anyone extend the Kubernetes API with their own resource types — databases, message queues, ML pipelines — anything.

### Factor 2: Ecosystem Network Effects

CNCF created a neutral governance model, unlike Docker Inc., which was a commercial entity with conflicting incentives. This mattered.

Then every cloud provider invested in managed Kubernetes:
- Amazon → EKS
- Microsoft → AKS
- Google → GKE (they already had it)

Once AWS, Azure, and Google all offered managed Kubernetes, it was over. Companies didn't have to choose a cloud AND an orchestrator. Kubernetes was the orchestrator, on every cloud.

The tooling ecosystem amplified this: Helm, Kustomize, ArgoCD, Flux, Istio — all Kubernetes-native, all making K8s more useful than any competitor.

### Factor 3: The CRD Extensibility Model

This is the real genius: CRDs + Operators let Kubernetes manage databases, message queues, and ML pipelines — not just containers.

Examples:
- **PostgreSQL Operator** — manages database clusters, failover, backups
- **Kafka Operator** — handles broker scaling, topic management, replication
- **Spark Operator** — submits and monitors distributed compute jobs
- **Kubeflow** — runs entire ML training pipelines

Kubernetes went from "container orchestrator" to "anything orchestrator." That extensibility made it impossible to compete with.

```yaml
# Kubernetes managing a PostgreSQL cluster (via CRD)
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: production-db
spec:
  instances: 3
  storage:
    size: 100Gi
  backup:
    barmanObjectStore:
      destinationPath: s3://my-bucket/backups
```

## What Kubernetes Still Gets Wrong

Let's be honest about the problems.

### Problem 1: Complexity Tax

Running a three-container web app shouldn't require understanding Deployments, Services, Ingresses, ConfigMaps, Secrets, PersistentVolumeClaims, NetworkPolicies, and ServiceAccounts.

The average Kubernetes deployment involves **200+ lines of YAML for a single service**. Compare that to `docker compose up`.

### Problem 2: Developer Experience

Local development on Kubernetes is painful. Minikube, Kind, k3d — these are all workarounds. The inner loop (write code → see results) is 10x slower than non-K8s development.

Tools like Tilt, Skaffold, and Telepresence help but add complexity. The fact that an entire discipline — **platform engineering** — exists largely to make Kubernetes usable by application developers tells you something about the developer experience problem.

### Problem 3: Cost Optimization

Kubernetes makes it easy to over-provision (just add more nodes!) but doesn't help you right-size. Resource requests and limits are guessed by most teams. FinOps for Kubernetes is an entire industry.

Teams regularly run clusters where 40–60% of capacity is idle, at significant cost.

## What's Next for Container Orchestration

### Trend 1: WebAssembly on the Edge

Containers start in seconds. WebAssembly components start in **microseconds**. For edge computing and serverless functions, Wasm isn't competing with Kubernetes — it's extending it to places containers can't go.

```
Startup time comparison:
VM         → minutes
Container  → seconds
Wasm       → microseconds
```

Projects like SpinKube run Wasm workloads on Kubernetes. Cloudflare Workers, Fastly, and Fermyon are building Wasm-native platforms at the edge.

### Trend 2: AI Infrastructure Workloads

GPU scheduling on Kubernetes is immature compared to CPU scheduling. AI training workloads need fundamentally different scheduling semantics:

- **Gang scheduling** — all pods must start together or none start
- **Preemption priority** — training jobs vs. inference jobs
- **GPU partitioning** — sharing GPU resources across multiple workloads

Projects like KubeRay, vLLM operator, and GPU partitioning are closing the gap, but the abstractions aren't right yet. This is the most active area of K8s development in 2026.

### Trend 3: Platform-as-a-Product

The answer to Kubernetes complexity is **Internal Developer Platforms (IDPs)**. Backstage, Port, and Humanitec are building golden paths that hide K8s behind a simplified API tailored to each organization.

```
Layer diagram:
Developer Portal     ← what developers see
Platform API         ← your organization's abstractions
Kubernetes           ← the actual runtime
```

> "Kubernetes is the kernel; your platform is the operating system."

The future isn't less Kubernetes — it's better abstractions on top of Kubernetes. Developers shouldn't need to know about pod anti-affinity rules. They should push code and it should deploy.

## Summary

**Why Kubernetes won:**
- Declarative API model (the right abstraction for infrastructure)
- Neutral governance + cloud provider investment
- CRD extensibility (became the orchestrator for everything, not just containers)

**Where it still struggles:**
- Complexity for simple workloads
- Developer experience (platform engineering exists to solve this)
- Cost optimization

**What's next:**
- WebAssembly for sub-second edge workloads
- Better GPU scheduling for AI workloads
- Platform engineering to hide K8s complexity

If you're starting a new project today, Kubernetes is still the right default for production workloads. But don't use it directly — build a platform on top of it, or use a managed platform that already does.

---

*Published by the **TechAI Explained** team. Follow us for Kubernetes deep dives and platform engineering insights.*
