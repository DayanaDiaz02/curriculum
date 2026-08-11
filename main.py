from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Mi Currículum Vitae API",
    description="API interactiva con mi información profesional",
    version="1.0.0"
)

class Proyecto(BaseModel):
    id: int
    nombre: str
    tipo: str
    descripcion: str
    tecnologias: Optional[List[str]] = []

MI_PERFIL = {
    "datos_personales": {
        "nombre_completo": "Luisa Dayana Díaz Ibarra",
        "rol": "Desarrolladora de Software / Estudiante",
        "ubicacion": "Chihuahua, México",
        "contacto": {
            "email": "dayanadiaz0802@gmail.com",
            "github": "https://github.com/DayanaDiaz02?tab=overview&from=2026-07-01&to=2026-07-15",
        }
    },
    "Experiencia_laboral": {
        "Opticas_de_Chihuahua": "2024-actualidad"
    },
    "logros_y_proyectos": [
        {
            "id": 1,
            "nombre": "Nawesari",
            "tipo": "Proyecto Integrador",
            "descripcion": "Aplicación web que te enseña la pronunciacion y gramatica raramuri, una lengua muerta",
            "tecnologias": ["React", "Larabase", "Supabase"]
        },
    ],
    "educacion": {
        "institucion": "Universidad Tecnológica de Chihuahua",
        "estado": "Estudiante 2024-actualidad",
        "enfoque": "Desarrollo software y multiplataforma"
    }
}

# --- ENDPOINTS GENERALES (GET) ---

@app.get("/", tags=["General"])
def obtener_inicio():
    """Mensaje de bienvenida a la API."""
    return {
        "mensaje": "¡Bienvenido!",
        "instrucciones": "Visita /docs para interactuar con los endpoints y conocer más sobre mi perfil.",
        "status": "Online y listo para la acción"
    }

@app.get("/cv", tags=["Completo"])
def obtener_cv_completo():
    """Devuelve todo el currículum en un solo objeto JSON."""
    return MI_PERFIL

@app.get("/cv/perfil", tags=["Secciones"])
def obtener_datos_personales():
    """Obtiene únicamente los datos de contacto y presentación."""
    return MI_PERFIL["datos_personales"]

@app.get("/cv/habilidades", tags=["Secciones"])
def obtener_habilidades():
    """Lista de tecnologías y metodologías dominadas."""
    return MI_PERFIL["habilidades_tecnicas"]


# --- CRUD PARA LOGROS Y PROYECTOS ---

#  GET: Leer proyectos
@app.get("/cv/logros", response_model=List[Proyecto], tags=["Gestión de Proyectos"])
def obtener_logros_y_proyectos():
    """Lista detallada de proyectos destacados y éxitos académicos."""
    return MI_PERFIL["logros_y_proyectos"]


#  POST: Crear / Añadir un proyecto nuevo
@app.post("/cv/logros", response_model=Proyecto, status_code=201, tags=["Gestión de Proyectos"])
def agregar_proyecto(nuevo_proyecto: Proyecto):
    """Añade un nuevo proyecto a la lista del CV."""
    # Evitar IDs duplicados
    for proyecto in MI_PERFIL["logros_y_proyectos"]:
        if proyecto["id"] == nuevo_proyecto.id:
            raise HTTPException(status_code=400, detail="¡Este ID de proyecto ya existe! ._.")
            
    MI_PERFIL["logros_y_proyectos"].append(nuevo_proyecto.model_dump())
    return nuevo_proyecto


#  PUT: Modificar un proyecto existente
@app.put("/cv/logros/{proyecto_id}", response_model=Proyecto, tags=["Gestión de Proyectos"])
def actualizar_proyecto(proyecto_id: int, proyecto_actualizado: Proyecto):
    """Busca un proyecto por ID y actualiza su contenido."""
    for index, proyecto in enumerate(MI_PERFIL["logros_y_proyectos"]):
        if proyecto["id"] == proyecto_id:
            MI_PERFIL["logros_y_proyectos"][index] = proyecto_actualizado.model_dump()
            return proyecto_actualizado
            
    raise HTTPException(status_code=404, detail="Proyecto no encontrado para actualizar ;-; ")


#  DELETE: Eliminar un proyecto
@app.delete("/cv/logros/{proyecto_id}", tags=["Gestión de Proyectos"])
def eliminar_proyecto(proyecto_id: int):
    """Elimina un proyecto del listado usando su ID."""
    for index, proyecto in enumerate(MI_PERFIL["logros_y_proyectos"]):
        if proyecto["id"] == proyecto_id:
            MI_PERFIL["logros_y_proyectos"].pop(index)
            return {"mensaje": f"Proyecto con ID {proyecto_id} borrado exitosamente OwO"}
            
    raise HTTPException(status_code=404, detail="El proyecto que buscas borrar no existe X_X")


# --- EL TRUCO MAGNÍFICO PARA EL BOTÓN DE PLAY ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)