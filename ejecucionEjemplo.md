Aplica estos permisos:


```Bash
kubectl apply -f argo-rbac-fix.yaml -n argo
```

Paso 5: Ejecutar el Pipeline
Con todos los archivos creados y aplicados, lanza el workflow.


```Bash
# Envía el workflow y observa su progreso en tiempo real
argo submit --watch -n argo mi-workflow.yaml
```

Verás cómo cada tarea se ejecuta en orden. Si quieres una vista más gráfica, accede a la UI de Argo.

Paso 6: Ver los Resultados
6.1. Acceder a la Interfaz Gráfica (UI)

```Bash
# En una nueva terminal, ejecuta:
kubectl -n argo port-forward deployment/argo-server 2746:2746

# Abre tu navegador en https://localhost:2746
# (Ignora la advertencia de seguridad, es normal)
```
En la UI podrás ver el grafo de tu pipeline completado en verde.

6.2. Descargar el Resultado Final
Para obtener el archivo synthetic_data.csv generado:


```Bash
# 1. Obtén el nombre completo de tu último workflow
WORKFLOW_NAME=$(argo list -n argo -o name --status=Succeeded --limit=1)
echo "El último workflow exitoso es: $WORKFLOW_NAME"

# 2. Busca el nombre del Pod que ejecutó el último paso
POD_NAME=$(kubectl get pods -n argo -l workflows.argoproj.io/workflow=$WORKFLOW_NAME,workflows.argoproj.io/template-name=task-template -o jsonpath='{.items[?(@.metadata.labels.workflows\.argoproj\.io/dag-task-name=="generar-datos-sinteticos")].metadata.name}')
echo "El pod final es: $POD_NAME"

# 3. Copia el fichero desde el pod a tu máquina local
kubectl cp -n argo $POD_NAME:/tmp/data/synthetic_data.csv ./resultado_final.csv

echo "¡Éxito! El resultado está en ./resultado_final.csv"
```