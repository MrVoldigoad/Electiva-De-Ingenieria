from flask import Flask, render_template, request, jsonify, session, redirect
from conexion import conectar, devolver_conexion, inicializar_pool, cerrar_pool
from datetime import datetime
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

# 🔥 MODO DESARROLLO (ACCESO SIN AUTENTICACION)
MODO_DESARROLLO = os.getenv("MODO_DESARROLLO", "False") == "True"

@app.before_request
def antes_request():
    """Se ejecuta antes de cada request"""
    pass

@app.teardown_appcontext
def teardown_db(exception):
    """Cierra las conexiones al final de cada request"""
    pass

# =========================
# 🏠 RUTA RAÍZ
# =========================
@app.route("/")
def home():
    """Redirige a login o al index dependiendo de la sesión"""
    if "usuario" in session:
        if session.get("rol") == "admin":
            return redirect("/admin")
        return redirect("/index_cliente")
    return redirect("/login")


# =========================
# 🔐 LOGIN SEGURO
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return render_template("login.html", error="Usuario y contraseña son requeridos")

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT * FROM usuarios WHERE username=%s",
                (username,)
            )
            user = cursor.fetchone()
            cursor.close()
            devolver_conexion(conexion)

            if user and check_password_hash(user[2], password):
                session["usuario"] = user[1]
                session["rol"] = user[3]

                if user[3] == "admin":
                    return redirect("/admin")
                else:
                    return redirect("/index_cliente")
            else:
                return render_template("login.html", error="Usuario o contraseña incorrectos")
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return render_template("login.html", error="Error de conexión con la base de datos")

    return render_template("login.html")


# =========================
# 🔓 LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =========================
# 🌐 INDEX CLIENTE (PROTEGIDO)
# =========================
@app.route("/index_cliente")
def index_cliente():
    if "usuario" not in session and not MODO_DESARROLLO:
        return redirect("/login")

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # 🔥 IMPORTANTE: traer imagen
        cursor.execute("SELECT id, nombre, precio, imagen FROM bebidas;")
        bebidas = cursor.fetchall()
        cursor.close()
        devolver_conexion(conexion)

        return render_template("index.html", bebidas=bebidas)
    except Exception as e:
        print(f"❌ Error en index: {e}")
        return f"Error al cargar bebidas: {e}", 500


# =========================
# 🔓 VISTA PREVIA SIN LOGIN (DESARROLLO)
# =========================
@app.route("/vista_previa")
def vista_previa():
    """Ruta para ver el formulario de compra sin autenticación"""
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, precio, imagen FROM bebidas;")
        bebidas = cursor.fetchall()
        cursor.close()
        devolver_conexion(conexion)

        # Usa la misma plantilla del cliente
        return render_template("index.html", bebidas=bebidas)
    except Exception as e:
        print(f"❌ Error en vista_previa: {e}")
        return f"<h1>Error al cargar bebidas: {e}</h1><p>Verifica la conexión a la BD</p>", 500


# =========================
# 🛒 COMPRAR
# =========================
@app.route("/comprar", methods=["POST"])
def comprar():
    if "usuario" not in session and not MODO_DESARROLLO:
        return redirect("/login")

    try:
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        domicilio = request.form.get("domicilio")

        if not nombre or not telefono:
            return "❌ Nombre y teléfono son requeridos", 400

        conexion = conectar()
        cursor = conexion.cursor()

        # 🔥 Obtener bebidas desde BD
        cursor.execute("SELECT id, nombre, precio FROM bebidas")
        bebidas = cursor.fetchall()

        productos = []
        total = 0

        # 🔥 NUEVA LOGICA CON CANTIDADES
        for bebida in bebidas:
            bebida_id = bebida[0]
            cantidad = int(request.form.get(f"cantidad_{bebida_id}", 0))

            if cantidad > 0:
                productos.append((bebida, cantidad))
                total += bebida[2] * cantidad

        # ❌ Si no seleccionó nada
        if not productos:
            cursor.close()
            devolver_conexion(conexion)
            return "❌ Debes seleccionar al menos una bebida", 400

        # Crear cliente
        cursor.execute(
            "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s) RETURNING id",
            (nombre, telefono)
        )
        cliente_id = cursor.fetchone()[0]

        costo_domicilio = 5000 if domicilio else 0
        total_final = total + costo_domicilio

        # Crear pedido
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, total, domicilio, total_final) VALUES (%s, %s, %s, %s) RETURNING id",
            (cliente_id, total, bool(domicilio), total_final)
        )
        pedido_id = cursor.fetchone()[0]

        # Guardar detalle con cantidad REAL
        for bebida, cantidad in productos:
            cursor.execute(
                "INSERT INTO detalle_pedidos (pedido_id, bebida_id, cantidad) VALUES (%s, %s, %s)",
                (pedido_id, bebida[0], cantidad)
            )

        conexion.commit()
        cursor.close()
        devolver_conexion(conexion)

        return render_template(
            "recibo.html",
            nombre=nombre,
            telefono=telefono,
            productos=productos,
            total=total,
            domicilio=costo_domicilio,
            total_final=total_final,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M")
        )
    except Exception as e:
        print(f"❌ Error en compra: {e}")
        return f"Error al procesar compra: {e}", 500


# =========================
# 📊 PANEL ADMIN PRO
# =========================
@app.route("/admin")
def admin():
    if "rol" not in session or session["rol"] != "admin":
        return redirect("/login")

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Pedidos
        cursor.execute("""
        SELECT 
            p.id,
            c.nombre,
            c.telefono,
            p.total_final
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.id DESC
        """)
        pedidos = cursor.fetchall()

        # Totales
        cursor.execute("SELECT COALESCE(SUM(total_final),0) FROM pedidos;")
        total_ventas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos;")
        total_pedidos = cursor.fetchone()[0]

        cursor.execute("""
        SELECT COUNT(DISTINCT c.id)
        FROM clientes c
        INNER JOIN pedidos p ON c.id = p.cliente_id
        """)
        total_clientes = cursor.fetchone()[0]

        # Gráfica clientes
        cursor.execute("""
        SELECT c.nombre, SUM(p.total_final)
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        GROUP BY c.nombre
        """)
        ventas_clientes = cursor.fetchall()

        # Gráfica productos
        cursor.execute("""
        SELECT b.nombre, SUM(dp.cantidad)
        FROM detalle_pedidos dp
        JOIN bebidas b ON dp.bebida_id = b.id
        GROUP BY b.nombre
        """)
        ventas_productos = cursor.fetchall()

        cursor.close()
        devolver_conexion(conexion)

        return render_template(
            "admin.html",
            pedidos=pedidos,
            total_ventas=total_ventas,
            total_pedidos=total_pedidos,
            total_clientes=total_clientes,
            ventas_clientes=ventas_clientes,
            ventas_productos=ventas_productos,
            usuario=session["usuario"]
        )
    except Exception as e:
        print(f"❌ Error en admin: {e}")
        return f"<h1>Error en panel admin: {e}</h1>", 500


# =========================
# 👁️ VER PEDIDO
# =========================
@app.route("/pedido/<int:id>")
def ver_pedido(id):
    if "rol" not in session or session["rol"] != "admin":
        return redirect("/login")

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT 
            p.id,
            c.nombre,
            c.telefono,
            p.total,
            p.domicilio,
            p.total_final
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.id=%s
        """, (id,))
        
        pedido = cursor.fetchone()

        cursor.execute("""
        SELECT b.nombre, b.precio
        FROM detalle_pedidos dp
        JOIN bebidas b ON dp.bebida_id = b.id
        WHERE dp.pedido_id=%s
        """, (id,))

        productos = cursor.fetchall()

        cursor.close()
        devolver_conexion(conexion)

        return render_template("detalle_pedido.html", pedido=pedido, productos=productos)
    except Exception as e:
        print(f"❌ Error al ver pedido: {e}")
        return f"Error al ver pedido: {e}", 500


# =========================
# 🗑️ ELIMINAR PEDIDO (CORREGIDO)
# =========================
@app.route("/eliminar_pedido/<int:id>")
def eliminar_pedido(id):
    if "rol" not in session or session["rol"] != "admin":
        return redirect("/login")

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Obtener cliente del pedido
        cursor.execute(
            "SELECT cliente_id FROM pedidos WHERE id=%s",
            (id,)
        )
        cliente = cursor.fetchone()

        if cliente:
            cliente_id = cliente[0]

            # Eliminar detalle del pedido
            cursor.execute(
                "DELETE FROM detalle_pedidos WHERE pedido_id=%s",
                (id,)
            )

            # Eliminar pedido
            cursor.execute(
                "DELETE FROM pedidos WHERE id=%s",
                (id,)
            )

            # 🔥 VERIFICAR SI EL CLIENTE AÚN TIENE PEDIDOS
            cursor.execute(
                "SELECT COUNT(*) FROM pedidos WHERE cliente_id=%s",
                (cliente_id,)
            )
            pedidos_restantes = cursor.fetchone()[0]

            # 🔥 SOLO ELIMINAR SI NO TIENE MÁS PEDIDOS
            if pedidos_restantes == 0:
                cursor.execute(
                    "DELETE FROM clientes WHERE id=%s",
                    (cliente_id,)
                )

        conexion.commit()
        cursor.close()
        devolver_conexion(conexion)

        return redirect("/admin")
    except Exception as e:
        print(f"❌ Error al eliminar pedido: {e}")
        return f"Error al eliminar pedido: {e}", 500


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    inicializar_pool()
    try:
        app.run(debug=True, host="127.0.0.1", port=5000)
    finally:
        cerrar_pool()