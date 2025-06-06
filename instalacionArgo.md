# Instalación de Argo CD en Minikube

Este mini tutorial te guía para instalar Argo CD en tu clúster local de Minikube, siguiendo los pasos recomendados por la documentación oficial.

---

## 1. Iniciar Minikube (si aún no está activo)

```bash
minikube start
```

## 2. Crear el Namespace para Argo CD
Argo CD se instala en su propio namespace para mantener los recursos organizados.

```bash
kubectl create namespace argocd
```

## 3. Aplicar el Manifiesto de Instalación
Descarga y aplica los recursos de Argo CD directamente desde el repositorio oficial.

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 4. Acceder a la Interfaz Web (UI)
Para entornos locales como Minikube, puedes usar port-forward para acceder al servicio web de Argo CD.

En una terminal separada, ejecuta:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

## Obtener la Contraseña Inicial
El usuario por defecto es admin. La contraseña inicial se encuentra en un secret de Kubernetes:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```