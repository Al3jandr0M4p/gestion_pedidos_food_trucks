-- Creacion y uso de la base de datos
create database if not exists foodtruck;
use foodtruck;

-- Tabla de usuarios
create table if not exists users(
	id int primary key auto_increment,
    name varchar(100) not null,
    password varchar(255) not null,
    email varchar(100) not null,
    rol enum('admin') default 'admin',
    estado ENUM('activo', 'inactivo') DEFAULT 'activo' NOT NULL,
    numero varchar(100)
);

select * from users;

-- usuarios desabilitados
CREATE TABLE user_desabilitados (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    disabled_at TIMESTAMP NOT NULL
);

-- Tabla de food trucks
create table if not exists trucks(
	id int primary key auto_increment,
    nombre_truck varchar(100) not null,
    estado_truck enum('inactivo', 'activo') default 'activo' not null,
    imagen_foodtruck varchar(255) not null,
    info_foodtruck text,
    especialidad text not null
);

select * from trucks;

insert into trucks (nombre_truck, imagen_foodtruck, info_foodtruck, especialidad)
values 
('Pizza Paradise', 'https://plus.unsplash.com/premium_photo-1673823194966-629180bbfc92?q=80&w=2070&auto=format&fit=crop', 'Pizzeria Gourmet • Ingredientes Premium Selectos', 'Especialidad: Pizza Truffle & Blue Cheese con cebolla caramelizada al vino tinto');

insert into trucks (nombre_truck, imagen_foodtruck, info_foodtruck, especialidad)
values
('El Sabor Latino', 'https://images.unsplash.com/photo-1565123409695-7b5ef63a2efb?auto=format&fit=crop&q=80&w=2071', 'Cocina Mexicana Autentica • Premiado 2024', 'Especialidad: Tacos al Pastor con piña asada, guacamole artesanal y salsas secretas'),
('Asian Fusion Wheels', 'https://images.unsplash.com/photo-1509315811345-672d83ef2fbc?auto=format&fit=crop&q=80&w=2071', 'Fusión Asiática Moderna • Chef Premiado Internacional', 'Especialidad: Korean BBQ Bowls con kimchi artesanal y salsa umami secreta'),
('Burger Paradise', 'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&q=80&w=1965', 'Hamburguesas Gourmet • Ingredientes Premium Selectos', 'Especialidad: Burger Truffle & Blue Cheese con cebolla caramelizada al vino tinto');

insert into trucks (nombre_truck, imagen_foodtruck, info_foodtruck, especialidad)
VALUES
('Sweet Cravings', 'https://i.pinimg.com/736x/94/0e/ed/940eedd0daef734cf4d1d6cf1b66c6be.jpg', 'Postres irresistibles & café de especialidad', 'Especialidad: Donas artesanales rellenas & malteadas con toppings exóticos.'),
('Vegan Street Eats', 'https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y29taWRhJTIwdmVnYW5hfGVufDB8fDB8fHww', 'Opciones plant-based y sostenibles', 'Especialidad: Comida vegana de la mejor calidad.');

create table productos (
	id int primary key auto_increment,
    nombre_producto varchar(100) not null,
    descripcion text,
    precio decimal(10, 2) not null,
    imagen_producto varchar(255) not null,
    truck_id int not null,
    foreign key (truck_id) references trucks(id) on delete cascade
);

select * from productos;

INSERT INTO productos (nombre_producto, descripcion, precio, imagen_producto, truck_id)
VALUES
('Pizza Truffle', 'Pizza con trufa negra y queso azul', 12.99, 'https://images.unsplash.com/photo-1571091718767-18b511545477', 1),
('Margherita Clásica', 'Tomate, mozzarella y albahaca fresca', 10.50, 'https://images.unsplash.com/photo-1564936281260-3c1c30b52b37', 1),
('Taco al Pastor', 'Taco con cerdo adobado, piña y guacamole', 3.99, 'https://images.unsplash.com/photo-1608032077036-20d20084740f', 2),
('Quesadilla de Queso', 'Queso derretido en tortilla de harina', 5.50, 'https://images.unsplash.com/photo-1599974579681-0ac667a3e6be', 2),
('Korean BBQ Bowl', 'Arroz con carne BBQ coreana y kimchi', 11.99, 'https://images.unsplash.com/photo-1617196038641-06d98cce1a04', 3),
('Gyozas', 'Empanadillas rellenas de cerdo y vegetales', 6.99, 'https://images.unsplash.com/photo-1598866594237-21b86d0f5a43', 3),
('Truffle Burger', 'Hamburguesa con queso azul y cebolla caramelizada', 13.50, 'https://images.unsplash.com/photo-1561758033-d89a9ad46330', 4),
('Cheeseburger Clásica', 'Hamburguesa con queso cheddar y pepinillos', 9.99, 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38', 4);

-- Tabla de mesas
create table if not exists mesas(
	id int primary key auto_increment,
    estado ENUM('ocupada', 'libre') DEFAULT 'libre' NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_estado ON mesas(estado);
select * from mesas;

create table transacciones (
	id varchar(50) primary key,
    mesa_id int not null,
    metodo_pago varchar(20) not null,
    monto decimal(10, 2) not null,
    estado varchar(20) not null,
    fecha datetime not null,
    datos_adicionales json,
    token_confirmacion VARCHAR(255),
    fecha_confirmacion DATETIME,
    foreign key (mesa_id) references mesas(id)
);

create table transaccion_detalles (
	id int auto_increment primary key,
    transaccion_id varchar(50) not null,
    producto_id int not null,
    cantidad int not null,
    precio_unitario decimal(10, 2) not null,
    foreign key (transaccion_id) references transacciones(id),
    foreign key (producto_id) references productos(id)
);

delimiter //

create procedure asignar_mesa()
begin
	declare mesa_id int;
    
    select id into mesa_id from mesas where estado = 'libre' limit 1;
    if mesa_id is not null then
		update mesas set estado = 'ocupada' where id = mesa_id;
	else
        insert into mesas(estado) values ('ocupada');
        set mesa_id = last_insert_id();
	end if;

    select mesa_id as mesa_asignada;
end;
//

delimiter ;