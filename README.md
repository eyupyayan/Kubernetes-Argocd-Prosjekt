# Kubernetes + Argo CD Læringsprosjekt

Dette prosjektet er laget som en **praktisk lab** for å lære:

* Docker og container-bygging
* Kubernetes grunnressurser (Deployment, Service, ConfigMap, Secret)
* Kustomize (base + overlays)
* GitOps med Argo CD
* Flyten fra kode → image → cluster → GitOps deploy

Målet er å forstå **hvordan moderne DevOps / plattform-team jobber i praksis**.

---

## Teknologistack

* **WSL2** – Linux-miljø på Windows
* **Docker Desktop** – container-runtime og lokalt Kubernetes cluster
* **Kubernetes** – orkestrering av containere
* **Argo CD** – GitOps deployment-verktøy
* **Python + Flask** – enkel demo-applikasjon
* **Kustomize** – miljøtilpasning av YAML

---

## Prosjektstruktur

```
k8s-argocd-lab/
│
├─ app/
│  ├─ Dockerfile
│  ├─ server.py
│  └─ requirements.txt
│
├─ k8s/
│  ├─ base/
│  │  ├─ namespace.yaml
│  │  ├─ deployment.yaml
│  │  ├─ service.yaml
│  │  ├─ configmap.yaml
│  │  ├─ secret.yaml
│  │  └─ kustomization.yaml
│  │
│  └─ overlays/
│     ├─ dev/
│     │  ├─ kustomization.yaml
│     │  └─ patch-replicas.yaml
│     └─ prod/
│        ├─ kustomization.yaml
│        └─ patch-replicas.yaml
│
└─ argocd/
   ├─ application-dev.yaml
   └─ application-prod.yaml
```

### Forklaring

* **app/** – kildekode og Dockerfile
* **k8s/base/** – standard Kubernetes-ressurser
* **k8s/overlays/** – miljøspesifikke endringer (dev/prod)
* **argocd/** – Argo CD Application-definisjoner

---

## Forutsetninger

Installer følgende:

* WSL2 + Ubuntu
* Docker Desktop (med Kubernetes aktivert)
* kubectl
* Git
* Docker Hub eller annet container-registry

Test at Kubernetes fungerer:

```bash
kubectl get nodes
```

---

## 1. Bygg Docker Image

Fra prosjektroten:

```bash
docker build -t <bruker>/k8s-argocd-lab:0.1.0 ./app
```

Test lokalt:

```bash
docker run -p 8080:8080 <bruker>/k8s-argocd-lab:0.1.0
```

---

## 2. Push til Docker Registry

```bash
docker login
docker push <bruker>/k8s-argocd-lab:0.1.0
```

---

## 3. Deploy til Kubernetes (uten Argo CD først)

Dette steget er for å verifisere YAML-filene.

```bash
kubectl apply -k k8s/overlays/dev
kubectl -n batman-lab get all
```

Port-forward:

```bash
kubectl -n batman-lab port-forward svc/k8s-argocd-lab 8080:80
```

Åpne:
`http://localhost:8080`

---

## 4. Installer Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Port-forward UI:

```bash
kubectl -n argocd port-forward svc/argocd-server 8081:443
```

UI: `https://localhost:8081`

Hent admin-passord:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d; echo
```

---

## 5. Argo CD Application

Oppdater `repoURL` i `argocd/application-dev.yaml` til ditt Git-repo.

Apply:

```bash
kubectl apply -f argocd/application-dev.yaml
```

Argo CD vil nå:

* Lese YAML fra Git
* Deploye til cluster
* Holde cluster i sync med Git

---

## Arbeidsflyt (Daglig bruk)

1. Endre kode i `app/`
2. Bygg nytt image
3. Push til registry
4. Oppdater image-tag i overlay
5. Commit + push til Git
6. Argo CD syncer automatisk

Dette er **GitOps-flyten**.

---

## Kubernetes-Ressurser i Prosjektet

| Ressurs    | Formål                    |
| ---------- | ------------------------- |
| Namespace  | Isolasjon av miljø        |
| Deployment | Kjører pods               |
| Service    | Stabil nettverksadresse   |
| ConfigMap  | Konfig uten å bygge image |
| Secret     | Sensitiv data             |
| Probes     | Helsekontroll             |
| Resources  | CPU/Memory-kontroll       |
| Kustomize  | Miljøvariasjon            |
| Argo CD    | GitOps deploy             |

---

## Læringsøvelser

* Endre `replicas` i prod overlay
* Endre ConfigMap og se effekt
* Bryt readiness probe og observer
* Test rollback i Argo CD
* Endre resource limits og se OOMKill

---

## Vanlige Feil

| Problem             | Årsak                                |
| ------------------- | ------------------------------------ |
| ImagePullBackOff    | Image ikke pushed / feil tag         |
| 503 / Ingen respons | Service selector matcher ikke labels |
| Argo OutOfSync      | Manuell endring i cluster            |
| CrashLoopBackOff    | Feil i app / resource limits         |

---

## Videre Utvidelser

* Ingress Controller
* Horizontal Pod Autoscaler
* Network Policies
* RBAC
* External Secrets
* Helm

---

## Hensikt

Dette repoet er ment som en **full læringsreise i Kubernetes + GitOps**, ikke bare en demo.
Fokuset er å forstå *hvorfor* ting gjøres – ikke bare *hvordan*.

Når du mestrer dette prosjektet, forstår du kjernen i hvordan moderne plattform- og DevOps-team jobber.
