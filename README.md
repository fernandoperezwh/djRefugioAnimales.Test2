# djRefugioAnimalesServer

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
