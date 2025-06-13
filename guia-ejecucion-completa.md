# Guía Completa para Ejecutar el Pipeline de Series Temporales con Argo Workflows

Esta guía te llevará paso a paso desde el inicio de Minikube hasta la ejecución exitosa del pipeline de series temporales usando Argo Workflows y MinIO como almacenamiento de artifacts.

## Prerrequisitos

- Docker instalado
- Minikube instalado
- kubectl instalado
- Argo CLI instalado

## Paso 1: Iniciar Minikube

```bash
# Iniciar Minikube con recursos suficientes
minikube start --memory=4096 --cpus=2

# Verificar que Minikube está funcionando
minikube status

# Configurar el contexto de kubectl
kubectl config use-context minikube
```

## Paso 2: Instalar Argo Workflows

```bash
# Crear el namespace de Argo
kubectl create namespace argo

# Instalar Argo Workflows
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.6.10/install.yaml

# Verificar que los pods están ejecutándose
kubectl get pods -n argo

# Esperar a que todos los pods estén en estado Running
kubectl wait --for=condition=ready pod --all -n argo --timeout=300s
```

## Paso 3: Configurar RBAC para Argo

```bash
# Aplicar configuración RBAC (si tienes el archivo argo-rbac-fix.yaml)
kubectl apply -f argo-rbac-fix.yaml

# O crear manualmente los permisos básicos
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=argo:default -n argo
```

## Paso 4: Construir la Imagen Docker del Pipeline

```bash
# Configurar Docker para usar el daemon de Minikube
eval $(minikube docker-env)

# Construir la imagen Docker del pipeline
docker build -t pipeline-ts:0.1 .

# Verificar que la imagen se construyó correctamente
docker images | grep pipeline-ts
```

## Paso 5: Desplegar MinIO (Almacenamiento de Artifacts)

```bash
# Desplegar MinIO
kubectl apply -f minio/minio-deployment.yaml
kubectl apply -f minio/minio-service.yaml

# Verificar que MinIO está ejecutándose
kubectl get pods -n argo | grep minio
kubectl wait --for=condition=ready pod -l app=minio -n argo --timeout=300s
```

## Paso 6: Configurar el Almacenamiento de Artifacts

### 6.1 Crear el secreto para las credenciales de MinIO

```bash
# Crear secreto con las credenciales de MinIO
kubectl create secret generic minio-secret -n argo \
  --from-literal=accesskey=minioadmin \
  --from-literal=secretkey=minioadmin
```

### 6.2 Crear el bucket en MinIO

```bash
# Obtener el nombre del pod de MinIO
MINIO_POD=$(kubectl get pods -n argo | grep minio | awk '{print $1}')

# Configurar el cliente MinIO dentro del pod
kubectl exec -n argo $MINIO_POD -- mc alias set local http://localhost:9000 minioadmin minioadmin

# Crear el bucket necesario
kubectl exec -n argo $MINIO_POD -- mc mb local/my-bucket

# Verificar que el bucket se creó
kubectl exec -n argo $MINIO_POD -- mc ls local/
```

### 6.3 Configurar el repositorio de artifacts

```bash
# Aplicar la configuración del repositorio de artifacts
kubectl apply -f artifact-repository-config.yaml

# Aplicar la configuración del workflow controller
kubectl apply -f workflow-controller-configmap.yaml

# Reiniciar el workflow controller para que tome la nueva configuración
kubectl rollout restart deployment/workflow-controller -n argo

# Esperar a que el controller esté listo
kubectl wait --for=condition=available deployment/workflow-controller -n argo --timeout=300s
```

## Paso 7: Verificar la Configuración

```bash
# Verificar que todos los componentes están funcionando
echo "=== Verificando Argo Workflows ==="
kubectl get pods -n argo

echo "=== Verificando MinIO ==="
kubectl get svc -n argo | grep minio

echo "=== Verificando ConfigMaps ==="
kubectl get configmap -n argo

echo "=== Verificando Secretos ==="
kubectl get secrets -n argo | grep minio
```

## Paso 8: Ejecutar el Pipeline

```bash
# Ejecutar el workflow
argo submit --watch -n argo mi-workflow.yaml

# Ver el estado del workflow
argo list -n argo

# Ver detalles de un workflow específico (sustituir WORKFLOW_NAME)
argo get -n argo WORKFLOW_NAME

# Ver logs de un paso específico (sustituir WORKFLOW_NAME y STEP_NAME)
argo logs -n argo WORKFLOW_NAME -c STEP_NAME
```

## Paso 9: Acceder a la Interfaz Web de Argo (Opcional)

```bash
# Hacer port-forward para acceder a la UI de Argo
kubectl port-forward -n argo svc/argo-server 2746:2746 &

# Acceder a la interfaz web
echo "Accede a: https://localhost:2746"
```

## Paso 10: Acceder a MinIO Console (Opcional)

```bash
# Hacer port-forward para acceder a MinIO
kubectl port-forward -n argo svc/minio-service 9001:9001 &

# Acceder a la consola de MinIO
echo "Accede a: http://localhost:9001"
echo "Usuario: minioadmin"
echo "Contraseña: minioadmin"
```

## Comandos de Troubleshooting

### Ver logs del workflow controller
```bash
kubectl logs -n argo deployment/workflow-controller --tail=50
```

### Ver logs de MinIO
```bash
kubectl logs -n argo $(kubectl get pods -n argo | grep minio | awk '{print $1}') --tail=50
```

### Verificar configuración de artifacts
```bash
kubectl get configmap artifact-repositories -n argo -o yaml
kubectl get configmap workflow-controller-configmap -n argo -o yaml
```

### Limpiar workflows fallidos
```bash
# Eliminar todos los workflows
argo delete --all -n argo

# Eliminar workflows por estado
argo delete --completed -n argo
argo delete --failed -n argo
```

### Reiniciar componentes si hay problemas
```bash
# Reiniciar workflow controller
kubectl rollout restart deployment/workflow-controller -n argo

# Reiniciar argo server
kubectl rollout restart deployment/argo-server -n argo

# Reiniciar MinIO
kubectl rollout restart deployment/minio -n argo
```

## Estructura de Archivos Necesarios

Asegúrate de tener los siguientes archivos en tu directorio:

```
.
├── Dockerfile                           # Imagen del pipeline
├── mi-workflow.yaml                     # Definición del workflow
├── artifact-repository-config.yaml     # Configuración de MinIO
├── workflow-controller-configmap.yaml  # Configuración del controller
├── argo-rbac-fix.yaml                  # Permisos RBAC
├── requirements.txt                     # Dependencias Python
├── app.py                              # Aplicación principal
├── 01_create_initial_data.py           # Script 1 del pipeline
├── 02_select_columns.py                # Script 2 del pipeline
├── 03_train_model.py                   # Script 3 del pipeline
├── 04_generate_data.py                 # Script 4 del pipeline
└── minio/
    ├── minio-deployment.yaml           # Despliegue de MinIO
    └── minio-service.yaml              # Servicio de MinIO
```

## Notas Importantes

1. **Docker Environment**: Recuerda configurar el entorno Docker para Minikube con `eval $(minikube docker-env)` antes de construir imágenes.

2. **Recursos**: Asegúrate de que Minikube tiene suficientes recursos (memoria y CPU) para ejecutar todos los componentes.

3. **Artifacts**: El almacenamiento de artifacts es crucial para que los workflows funcionen correctamente. MinIO debe estar funcionando antes de ejecutar workflows.

4. **Permisos**: Los permisos RBAC son necesarios para que Argo pueda crear y gestionar pods.

5. **Networking**: Todos los servicios deben poder comunicarse entre sí dentro del cluster de Kubernetes.

## Verificación Final

Antes de ejecutar tu pipeline, verifica que:

- [ ] Minikube está ejecutándose
- [ ] Todos los pods de Argo están en estado Running
- [ ] MinIO está funcionando y el bucket existe
- [ ] La imagen Docker del pipeline está construida
- [ ] Los ConfigMaps y Secrets están creados
- [ ] El workflow controller se reinició después de la configuración

¡Una vez completados todos estos pasos, tu pipeline de series temporales debería ejecutarse correctamente con Argo Workflows!
