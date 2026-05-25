# 🍹 Brisa y Ron del Pacífico - Sistema de Pedidos

**Desarrollado por:**
- Alex David Angulo - ID: 407055
- Daniel Becerra - ID: 407491

## 📋 Descripción
Sistema web de compra y venta de bebidas tradicionales con panel administrativo, desarrollado con Flask y PostgreSQL.

---

## 🚀 Instalación y Configuración

### 1️⃣ Requisitos
- **Python** 3.8+
- **PostgreSQL** 12+
- **pip** (gestor de paquetes)

### 2️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar Base de Datos
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python tablas.py
```

Esto creará automáticamente todas las tablas necesarias.

### 4️⃣ Insertar Bebidas
```bash
python insertar_bebidas.py
```

Esto cargará las bebidas disponibles en la base de datos.

### 5️⃣ Verificar Credenciales
Las credenciales de admin se generan con:
```bash
python generar_hash.py
```

**Usuarios por defecto:**
- Usuario: `daniel` | Contraseña: `407491`
- Usuario: `alex` | Contraseña: `407055`

---

## ⚙️ Configuración de Conexión a BD
Edita el archivo `conexion.py` si necesitas cambiar los parámetros de conexión:

```python
host="localhost"           # Host de PostgreSQL
database="bebidas_pacifico" # Nombre de la BD
user="postgres"            # Usuario
password="1109920832"      # Contraseña
port="5432"               # Puerto
```

---

## 🌐 Ejecutar la Aplicación

### Modo Normal
```bash
python app.py
```
La aplicación estará disponible en: **http://localhost:5000/login**

### Modo Desarrollo (Ver formularios sin login)
```bash
set MODO_DESARROLLO=True
python app.py
```
Accede a: **http://localhost:5000/vista_previa**

---

## 📍 Rutas Disponibles

### 🔐 Autenticación
- `GET /login` - Página de login
- `POST /login` - Procesar login
- `GET /logout` - Cerrar sesión

### 👥 Cliente
- `GET /` - Redirige a login o home
- `GET /index_cliente` - Catálogo de bebidas (protegido)
- `POST /comprar` - Procesar compra
- `GET /vista_previa` - Vista previa sin login (desarrollo)

### 📊 Administrador
- `GET /admin` - Panel de estadísticas (protegido)
- `GET /pedido/<id>` - Detalles del pedido (protegido)
- `GET /eliminar_pedido/<id>` - Eliminar pedido (protegido)

---

## 🔧 Mejoras Implementadas

### ✅ Conexión a BD
- ✔️ Pool de conexiones para mejor rendimiento
- ✔️ Timeout de conexión (5 segundos)
- ✔️ Manejo robusto de errores
- ✔️ Logging de errores para debugging

### ✅ Autenticación
- ✔️ Validación de campos requeridos
- ✔️ Mensajes de error claros
- ✔️ Contraseñas hasheadas con Werkzeug

### ✅ Rutas
- ✔️ Ruta `/vista_previa` para probar sin login
- ✔️ Ruta `/` mejorada que redirige correctamente
- ✔️ Manejo de excepciones en todas las rutas
- ✔️ Nombres de ruta claros (`/index_cliente` en lugar de `/`)

### ✅ Base de Datos
- ✔️ Columna `imagen` agregada a tabla `bebidas`
- ✔️ Validaciones en inserción de datos
- ✔️ Eliminación en cascada de clientes sin pedidos

### ✅ Documentación
- ✔️ Archivo `requirements.txt` creado
- ✔️ Código comentado
- ✔️ Este README completo

---

## 🐛 Solución del Problema de Carga Lenta

**Problema Original:**
- La aplicación solo cargaba el login
- Tardaba varios intentos en cargar

**Causa:**
1. No había validación de conexión a BD en el inicio
2. Los errores de conexión no eran manejados correctamente
3. Faltaba pool de conexiones

**Soluciones Implementadas:**
1. ✅ Pool de conexiones con `psycopg2.pool.SimpleConnectionPool`
2. ✅ Timeout en conexiones (5 segundos)
3. ✅ Manejo de excepciones con mensajes claros
4. ✅ Logging para debugging
5. ✅ Devolución de conexiones al pool después de cada uso

---

## 🧪 Probar sin Login

Para ver el formulario de compra sin necesidad de autenticación:

1. Abre: `http://localhost:5000/vista_previa`
2. Verás el catálogo de bebidas y podrás hacer una compra de prueba
3. Los datos se guardarán en la BD normalmente

---

## 🆘 Solucionar Problemas

### Error: "psycopg2.OperationalError"
- Verifica que PostgreSQL esté corriendo
- Confirma las credenciales en `conexion.py`
- Verifica que la BD `bebidas_pacifico` existe

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Conexión muy lenta
- La aplicación ahora usa pool de conexiones
- Si aún es lenta, verifica tu conexión a BD

---

## 📦 Estructura del Proyecto
```
.
├── app.py                    # Aplicación principal Flask
├── conexion.py              # Gestión de conexiones a BD
├── tablas.py                # Creación de tablas
├── insertar_bebidas.py      # Inserción de bebidas
├── generar_hash.py          # Generación de contraseñas hasheadas
├── requirements.txt         # Dependencias Python
├── templates/               # Plantillas HTML
│   ├── login.html
│   ├── index.html
│   ├── admin.html
│   ├── detalle_pedido.html
│   └── recibo.html
└── static/                  # Archivos estáticos
    └── img/
```

---

## 📝 Notas Importantes
- Las contraseñas se almacenan hasheadas con Werkzeug
- El pool de conexiones se inicializa al arrancar la app
- Los errores se registran en la consola para debugging
- La sesión se guarda con `secret_key` (cambiar en producción)

---

**Última actualización:** 25 de mayo de 2026
