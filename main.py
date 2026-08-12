from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Mi Currículum Vitae API",
    description="API interactiva con mi información profesional",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Proyecto(BaseModel):
    id: int
    nombre: str
    tipo: str
    descripcion: str
    tecnologias: Optional[List[str]] = []

MI_PERFIL = {
    "datos_personales": {
        "nombre_completo": " ",
        "rol": " ",
        "ubicacion": " ",
        "contacto": {
            "email": " ",
            "github": " ",
        }
    },
    "Experiencia_laboral": {
        " empresa": " ",
    },
    "logros_y_proyectos": [
        {
            "id": 1,
            "nombre": "ejemplo de proyecto",
            "tipo": " ",
            "descripcion": " ",
            "tecnologias": []
        },
    ],
    "educacion": {
        "institucion": " ",
        "estado": " ",
        "enfoque": " "
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

@app.get("/curriculum", tags=["Completo"])
def obtener_curriculum():
    """Alias para compatibilidad con clientes que esperan /curriculum."""
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
            raise HTTPException(status_code=400, detail="¡Este ID de proyecto ya existe!")
            
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
            
    raise HTTPException(status_code=404, detail="Proyecto no encontrado para actualizar")


#  DELETE: Eliminar un proyecto
@app.delete("/cv/logros/{proyecto_id}", tags=["Gestión de Proyectos"])
def eliminar_proyecto(proyecto_id: int):
    """Elimina un proyecto del listado usando su ID."""
    for index, proyecto in enumerate(MI_PERFIL["logros_y_proyectos"]):
        if proyecto["id"] == proyecto_id:
            MI_PERFIL["logros_y_proyectos"].pop(index)
            return {"mensaje": f"Proyecto con ID {proyecto_id} borrado exitosamente"}
            
    raise HTTPException(status_code=404, detail="El proyecto que buscas borrar no existe")


# --- EL TRUCO MAGNÍFICO PARA EL BOTÓN DE PLAY ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
