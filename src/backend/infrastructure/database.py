import sqlite3
import pandas as pd
import json
from datetime import datetime

def iniciar_db():
    conn = sqlite3.connect('kingspan_pedidos.db')
    cursor = conn.cursor()
    # Agregamos la columna 'resultado_optimizacion'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_registro TEXT,
            cliente TEXT,
            producto TEXT,
            datos_completos TEXT,
            resultado_optimizacion TEXT
        )
    ''')

    conn.commit()
    conn.close()

def obtener_siguiente_orden():
    conn = sqlite3.connect('kingspan_pedidos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM pedidos')
    resultado = cursor.fetchone()[0]
    conn.close()
    # Si es el primer pedido, empezamos en 1, sino sumamos 1
    return (resultado + 1) if resultado else 1

def guardar_pedido(cliente, producto, datos_json):
    conn = sqlite3.connect('kingspan_pedidos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos (fecha_registro, cliente, producto, datos_completos)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cliente, producto, str(datos_json)))
    conn.commit()
    conn.close()
    
def consultar_historial():
    conn = sqlite3.connect('kingspan_pedidos.db')
    # Usamos pandas para leer la tabla directamente
    df = pd.read_sql_query("SELECT id as 'N° Orden', fecha_registro as 'Fecha Registro', cliente as 'Cliente', producto as 'Producto' FROM pedidos ORDER BY id DESC", conn)
    conn.close()
    return df

def guardar_pedido(cliente, producto, datos_dict, resultado_list):
    conn = sqlite3.connect('kingspan_pedidos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos (fecha_registro, cliente, producto, datos_completos, resultado_optimizacion)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        cliente, 
        producto, 
        json.dumps(datos_dict),      # Guardamos como texto JSON
        json.dumps(resultado_list)   # Guardamos como texto JSON
    ))
    conn.commit()
    conn.close()

def obtener_detalle_pedido(id_pedido):
    conn = sqlite3.connect('kingspan_pedidos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT datos_completos, resultado_optimizacion FROM pedidos WHERE id = ?', (id_pedido,))
    res = cursor.fetchone()
    conn.close()
    if res:
        return json.loads(res[0]), json.loads(res[1])
    return None, None