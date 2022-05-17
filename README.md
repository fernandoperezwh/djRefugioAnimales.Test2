# djRefugioAnimales.Test2

Este proyecto tiene como proposito poner a prueba las formas de crear un endpoint:
  - api_view
  - ApiView
  - GenericView
  - ViewSets

# Instalación
- Elegir una directorio de facil acceso para clonar el proyecto. 
    ```bash
    cd ~/Escritorio/
    ```
- Clonar el proyecto ya sea por ssh o https
    ```bash
    # Clone via ssh
    git clone git@github.com:fernandoperezwh/djRefugioAnimales.Test2.git
    # Clone via https
    git clone https://github.com/fernandoperezwh/djRefugioAnimales.Test2.git
    ```
- Crear el entorno virtual utilizando python 3.8, e instalar las dependencias.
    ```bash
    pipenv install
    ```
- Realizar las migraciones del proyecto 
    ```bash 
    python manage.py migrate
    ```
- Opcionalmente puede crear un nuevo super usuario con el siguiente comando
    ```bash
    python manage.py createsuperuser
    ```    
- Para concluir, ejecute el proyecto
    ```bash
    python manage.py runserver
    ```

# Uso

En el archivo `.env` que se encuentra en el directorio `.cfg/environments/development/` puede modificar las siguientes variables para configurar el proyecto:

- **API_ENDPOINT** - Corresponde al host del proyecto para realizar peticiones por la libreria requests
- **API_VERSION**- Define la versión del API que esta ejecutandose.
Las opciones son: 'v1', 'v2', 'v3' y 'v4' las cuales se describren a
continuación
  - **v1**: Las views se crean utilizando el decorador @api_view.
  - **v2**: Las views se crean utilizando la clase ApiView.
  - **v3**: Las views se crean utilizando la clase GenericView.
  - **v4**: Las views se crean utilizando la clase ViewSet.

- **API_STRATEGY** - Define la estrategia a utilizar para obtener la información desde el API
Las opciones son: 'requests' | 'instance'
  - **'requests'**: Obtiene los datos desde el DRF realizando una petición con
                la libreria requests que sale a internet y vuelve a entrar
                al servidor.
                Esta estrategia es más tardada debido a que vuelve a salir
                la petición a internet.
  - **'instance'**: Obtiene los datos utilizando una instancia de la clase de
                DRF.
                Esta estrategia es más rápida debido a que no sale del
                servidor sino que internamente se resuelve.

- **API_PUBLIC** - Define si los recursos del api es de libre acceso o si se requiere una
autentificación por sesión
  - 0: Recursos con autentificación por sesión requerida
  - 1: Recursos sin autentificación requerida