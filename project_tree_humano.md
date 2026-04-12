# Estructura del proyecto (explicacion humana)

Nota: Descripciones basadas en nombres de archivos y estructura. Si quieres mas detalle por archivo, dime y lo ampliamos.

Flight-management-system/
|- readme.md                          - Como correr frontend y backend
|- Proyecto Estructuras de Datos - Arboles.pdf - Documento del proyecto
|- backend/
|  |- main.py                          - Entrada del backend (FastAPI, rutas, CORS)
|  |- requirements.txt                 - Dependencias de Python
|  |- VALIDATION_REPORT.py             - Reporte o script de validacion
|  |- controllers/
|  |  |- simulation_controller.py      - Logica para simulacion (cola de vuelos)
|  |  |- tree_controller.py            - Logica simple para operaciones de arbol
|  |  |- version_controller.py         - Orquesta versiones (guardar/restaurar)
|  |- core/
|  |  |- shared_instances.py           - Instancias compartidas (arbol/cola)
|  |  |- structures/
|  |  |  |- avl_tree/
|  |  |  |  |- __init__.py               - Exporta la clase AVL
|  |  |  |  |- balance.py                - Balanceo del AVL
|  |  |  |  |- cancel.py                 - Cancelaciones en AVL
|  |  |  |  |- delete.py                 - Eliminacion en AVL
|  |  |  |  |- insert.py                 - Insercion en AVL
|  |  |  |  |- rotations.py              - Rotaciones del AVL
|  |  |  |  |- search.py                 - Busqueda en AVL
|  |  |  |  |- traversal.py              - Recorridos del arbol
|  |  |  |  |- tree.py                   - Clase AVL y metodos base
|  |  |  |- bst_tree/
|  |  |  |  |- __init__.py               - Paquete BST
|  |  |  |  |- bst.py                    - Implementacion BST
|  |  |  |  |- delete.py                 - Eliminacion en BST
|  |  |  |  |- insert.py                 - Insercion en BST
|  |  |  |  |- search.py                 - Busqueda en BST
|  |  |  |  |- tree.py                   - Clase BST y metodos base
|  |  |  |- node/
|  |  |  |  |- node.py                   - Nodo de arbol (datos y punteros)
|  |  |  |- queue/
|  |  |  |  |- queue.py                  - Cola FIFO
|  |  |  |- stack/
|  |  |  |  |- stack.py                  - Pila LIFO (undo/redo)
|  |- data/
|  |  |- InsercionEjemplo.json          - Ejemplo de insercion
|  |  |- ModoInsercion.json             - Archivo para modo insercion
|  |  |- ModoTopologia.json             - Archivo para modo topologia
|  |  |- TopologiaEjemplo.json          - Ejemplo de topologia
|  |- docs/
|  |  |- readme.MD                      - Documentacion del backend (vacio)
|  |- examples/                         - Carpeta para ejemplos
|  |- models/
|  |  |- flight.py                      - Modelo de vuelo
|  |- routes/
|  |  |- avl_routes.py                  - Endpoints para AVL
|  |  |- flight_routes.py               - Endpoints para vuelos
|  |  |- queue_routes.py                - Endpoints para cola
|  |  |- version_routes.py              - Endpoints para versiones
|  |- services/
|  |  |- avl_service.py                 - Servicios para operar el arbol
|  |  |- json_manager.py                - Carga/guardado de JSON
|  |  |- metrics.py                     - Calculo de metricas
|  |  |- price_calculator.py            - Calculo de precios
|  |  |- profitability_service.py       - Rentabilidad de vuelos
|  |  |- queue_service.py               - Logica de cola
|  |  |- serialize_tree.py              - Serializacion del arbol
|  |  |- stress_mode_service.py         - Logica de stress mode
|  |  |- tree_repository.py             - CRUD del arbol + undo/redo
|  |  |- validator.py                   - Validaciones
|  |  |- version_service.py             - Logica de versionado
|  |- tests/
|  |  |- test_flight_endpoints.py       - Pruebas de endpoints de vuelos
|  |  |- test_versions.py               - Pruebas de versionado
|- frontend/
|  |- index.html                         - Entrada HTML del frontend
|  |- package.json                       - Dependencias y scripts
|  |- package-lock.json                  - Versiones exactas npm
|  |- eslint.config.js                   - Config ESLint
|  |- vite.config.js                     - Config Vite
|  |- README.md                          - README de Vite
|  |- public/
|  |  |- vite.svg                        - Icono Vite
|  |- src/
|  |  |- App.jsx                         - App principal (JS)
|  |  |- App.tsx                         - Variante TS (probablemente no usada)
|  |  |- App.css                         - Estilos App
|  |  |- App.css.d.ts                    - Tipos CSS (TS)
|  |  |- index.css                       - Estilos globales
|  |  |- main.jsx                        - Punto de entrada React
|  |  |- assets/
|  |  |  |- react.svg                     - Icono React
|  |  |- components/
|  |  |  |- MetricsPanel.jsx             - Panel de metricas
|  |  |  |- MetricsPanel.css             - Estilos de metricas
|  |  |  |- QueueControlComponent.jsx    - Controles de cola
|  |  |  |- QueueControlComponent.css    - Estilos de cola
|  |  |  |- QueuePanel.jsx               - Vista de la cola
|  |  |  |- TreeComparison.jsx           - Comparacion AVL vs BST
|  |  |  |- TreeInfo.jsx                 - Info del arbol
|  |  |  |- TreeViewer.jsx               - Visualizador del arbol
|  |  |  |- UploadControls.jsx           - Subida de archivos
|  |  |  |- VersionPanel.jsx             - Panel de versiones
|  |  |  |- controls/
|  |  |  |  |- TraversalControls.jsx      - Controles de recorridos
|  |  |  |  |- TreeOperations.jsx         - Botones de operaciones
|  |  |  |  |- UploadControls.jsx         - Subida (control)
|  |  |- config/
|  |  |  |- api.js                       - Config de API
|  |  |- hooks/
|  |  |  |- useAvlTree.js                - Hook para AVL
|  |  |  |- useTreeOperations.js         - Hook para operaciones
|  |  |  |- useTreeState.js              - Hook de estado general
|  |  |- models/
|  |  |  |- treeModes.js                 - Modos de arbol
|  |  |- pages/
|  |  |  |- HomePage.jsx                 - Pagina principal
|  |  |- services/
|  |  |  |- avlService.js                - Llamadas al backend
|  |  |- utils/
|  |  |  |- treeHelpers.js               - Helpers del arbol
