# Gestion de pedidos de Food Trucks (FoodOrder)

## Sobre La app <a name = "about"></a>

La esto es una aplicacion hecha para solucionar la forma de pedidos  en los food trucks
para hacer ese trabajo tedioso y lento mas rapido y solucionar la problematica para que
los clientes se sientan mejor a la hora de realizar sus productos y pagar.

Buscamos que el usuario pueda familiarisarse con la aplicacion y la pueda sentirse mejor
en la aplicacion teniendo una grandiosa experienda de el mismo en dicha aplicacion.

## Como iniciar <a name = "getting_started"></a>

Aqui veremos como podemos inicar en la aplicacion por los tipos de usuarios de la aplicacion.

- Admin: Si eres un administrador la aplicacion contiene una ruta admin donde aloja un
formulario de login en la ruta `http://localhost:5000/login`
o lo pondras dependiendo en que dominio estes usando la aplicacion ej: `http://<dominio>:<puerto_donde_corre>/login`
ese sera el lugar donde podras iniciar sesion en la aplicacion con las credenciales que te halla otorgado
el administrador o jefe en tu email donde si colocas las credenciales correspondientes podras aceder a la aplicacion
donde como administrador podras administrar la aplicacion como agregar mas empleados "administradores", administrar food trucks
ver reportes de la app, los pedidos de la app del usuario donde podras ver la mesa que los pidio la cantidad el precio, etc.

- Usuario: Si es para los usuarios en si el usuario no podra entrar a la aplicacion a menos que sea por el qrCode que se le
entregara en su mesa donde al scanearlo el usuario podra ver el menu de los diferentes food trucks y podra elegir el de su
conveniencia y el que mas le apetesca la ruta donde los usuarios entraran a la aplicacion vendria a ser `http://localhost:5000/user/splash`
en esta ruta se le estara entregando una mesa al usuario donde el podra navegar en la aplicacion comprar, pagar y 
disfrutar de la aplicacion, etc.

## Pre-Requisistos que se necesita para poder usar la app

La empresa o personas que tengan la aplicacion y la quieran tener para el publico tendran que tener cierta cosas para tener el buen
funcionamiento de la aplicacion y su buen manejo u poder mantener una buena experiencia de usuario y mejorar la interfaz del usuario
a su conveniencia.

> Tendra que tener python instalado en su servidor local donde podra mostrar su web o trabajar con ella. En la pagina oficial de python <a href="https://www.python.org/" target="_blank" rel="noopener noreferrer">https://www.python.org/</a> podras instalar python despues que tenga python podra instalar flask el framewrok usado para desarrollar la aplicacion.

Instalar flask:

```bash
pip install flask
```

Instalar MySQL Connector si usa MySQL si no tendra que hacer una migracion de la aplicacion al gestor de base de datos que usted use ya que la aplicacion fue desarrollada para MySQL:

```bash
pip install python-mysql-connector
```

Instalar dotenv para las variables de entorno de la aplicacion ya que la aplicacion y la api de ella misma usan variables de entorno para mas seguridad:

```bash
pip install dotenv
```

## Instalacion <a name = "instalation"></a>

Para instalar todas las dependencias de la aplicacion y poder usar la aplicacion solo se tendra que clonar este repositorio en su sistema con git asegurese de tener git instalado

```bash
git clone https://github.com/Al3jandr0M4p/gestion_pedidos_food_trucks
```

Despues de tener clonado el repositorio en una carpeta de su sitema y ya con python instalado solo tiene que hacer el siguiente comando para instalar las dependencias

```bash
pip install -r requirements.txt
```

y si las quieres actualizar solo tienes que poner el siguiente comando

```bash
pip install --upgrade -r requirements.txt
```

## Usos <a name = "usage"></a>

Despues que ya tenga todas dependencias necesarias de la aplicacion podra correrla y probarla o usarla con el siguiente comando

En una terminal pondra:

```bash
python run.py
```

## Tecnologias utilizadas <a name = "Tecnologies"></a>

Esta aplicacion fue desarrollada usando las siguientes tecnologias:

- ***Python*** - Lenguaje principal para desarrollar la aplicacion.
- ***Flask*** – Microframework para el backend y el manejo de rutas.
- ***MySQL*** – Base de datos relacional para almacenar la información de pedidos, usuarios, etc.
- ***Jinja2*** – Motor de plantillas usado para renderizar HTML dinámico.
- ***JavaScript*** – Para interacciones del lado del cliente (front-end).
- ***HTML/CSS*** – Para la estructura y estilo de las páginas web.
- ***dotenv*** – Manejo seguro de variables de entorno.
- ***Chart.js*** – Para la visualización de gráficos estadísticos en el panel de admin.
- ***QR Code*** – Sistema de acceso por escaneo a la app para usuarios.

## Licencia <a name = "license"></a>
Este proyecto esta bajo la licencia MIT lo podras ver en el archivo LICENSE

## Contacto <a name = "Contact"></a>
- Email empresarial <a href="mailto:20230542@ipopsa.edu.do" target="_blank" rel="noopener noreferrer">20230542@ipopsa.edu.do</a>
- Email propio <a href="mailto:molle0711@gmail.com" target="_blank" rel="noopener noreferrer">molle0711@gmail.com</a>
- GitHub <a href="https://github.com/Al3jandr0M4p" target="_blank" rel="noopener noreferrer">https://github.com/Al3jandr0M4p</a>