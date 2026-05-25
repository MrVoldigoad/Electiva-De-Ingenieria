# ⚡ Guía de Inicio Rápido

## 1️⃣ Instalación (5 minutos)

### Paso 1: Asegúrate de tener PostgreSQL corriendo
```bash
# En Windows, PostgreSQL debe estar en servicios
# O ejecuta desde cmd: pg_ctl start
```

### Paso 2: Instala dependencias
```bash
cd "c:\Users\Soporte\Documents\Repo\Electiva-De-Ingenieria"
pip install -r requirements.txt
```

### Paso 3: Crea la base de datos
```bash
python tablas.py
```
**Verás:** `✅ Base de datos completa creada correctamente`

### Paso 4: Inserta bebidas
```bash
python insertar_bebidas.py
```
**Verás:** `✅ Bebidas insertadas correctamente`

---

## 2️⃣ Ejecutar la Aplicación

### Opción A: Acceso Completo (Con Login)
```bash
python app.py
```
**Abre:** http://localhost:5000/login

**Credenciales:**
- Usuario: `daniel` | Contraseña: `407491`
- Usuario: `alex` | Contraseña: `407055`

### Opción B: Pruebas Sin Login (Para Desarrollo)
```bash
# En PowerShell:
$env:MODO_DESARROLLO="True"
python app.py

# O en CMD:
set MODO_DESARROLLO=True
python app.py
```
**Abre:** http://localhost:5000/vista_previa

---

## 3️⃣ Rutas Disponibles

| Ruta | Descripción | Requiere Login |
|------|-------------|---|
| `/login` | Página de login | ❌ No |
| `/vista_previa` | Ver bebidas (desarrollo) | ❌ No |
| `/index_cliente` | Catálogo de bebidas | ✅ Sí |
| `/admin` | Panel administrativo | ✅ Sí (Admin) |
| `/logout` | Cerrar sesión | ✅ Sí |

---

## 4️⃣ Solucionar Problemas

### Error: "Base de datos no existe"
```bash
# Verifica que PostgreSQL esté corriendo
# Luego ejecuta nuevamente:
python tablas.py
```

### Error: "psycopg2 no encontrado"
```bash
pip install psycopg2-binary
```

### Error: "Puerto 5000 en uso"
```python
# Cambia el puerto en app.py:
app.run(debug=True, host="127.0.0.1", port=5001)
```

### Error: "Conexión rechazada"
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en `conexion.py`
- Verifica que la BD `bebidas_pacifico` existe

---

## 5️⃣ Cambios Principales Realizados

✅ **Pool de Conexiones** - Mejor rendimiento
✅ **Timeout en BD** - No se cuelga
✅ **Manejo de Errores** - Mensajes claros
✅ **Ruta sin Login** - Probar sin autenticación
✅ **Documentación** - README y CAMBIOS.md

---

## 📚 Más Información

- **README.md** - Documentación completa
- **CAMBIOS.md** - Registro detallado de cambios
- **app.py** - Código comentado con emojis

---

**¡Listo! Tu aplicación está lista para usar.** 🎉
