## Snake Game - Flask + Kubernetes + ArgoCD

A simple **Snake Game** built with **Flask**, Dockerized, deployed with **Helm**, and managed with **ArgoCD**.

## 📂 Project Structure

```

├── argocd/
│   └── application.yaml
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── _helpers.tpl
├── snake-flask/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/css/
│       └── style.css
├── tests/
├── Dockerfile
├── requirements.txt
└── sonar-project.properties
```

