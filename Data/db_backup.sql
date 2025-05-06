-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: foodtruck
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `mesas`
--

DROP TABLE IF EXISTS `mesas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` enum('ocupada','libre') NOT NULL DEFAULT 'libre',
  `ultima_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesas`
--

LOCK TABLES `mesas` WRITE;
/*!40000 ALTER TABLE `mesas` DISABLE KEYS */;
INSERT INTO `mesas` VALUES (1,'ocupada','2025-04-15 19:06:01'),(2,'ocupada','2025-04-16 20:24:48'),(3,'ocupada','2025-04-17 03:09:04'),(4,'ocupada','2025-04-17 03:22:22'),(5,'ocupada','2025-04-17 12:04:05'),(6,'ocupada','2025-04-17 12:17:12'),(7,'ocupada','2025-04-17 13:08:19'),(8,'ocupada','2025-04-19 16:36:35'),(9,'ocupada','2025-04-21 11:47:54'),(10,'ocupada','2025-04-22 11:59:53'),(11,'ocupada','2025-04-23 15:55:58'),(12,'ocupada','2025-04-24 16:21:43'),(13,'ocupada','2025-04-25 17:23:51'),(14,'ocupada','2025-04-25 22:03:41'),(15,'ocupada','2025-04-27 16:23:27'),(16,'ocupada','2025-04-27 16:24:43'),(17,'ocupada','2025-04-28 22:12:15'),(18,'ocupada','2025-04-29 11:46:05'),(19,'ocupada','2025-04-29 13:01:29'),(20,'ocupada','2025-04-29 17:22:13'),(21,'ocupada','2025-04-30 10:32:45'),(22,'ocupada','2025-05-01 12:31:34'),(23,'ocupada','2025-05-01 16:37:12'),(24,'ocupada','2025-05-02 11:50:36'),(25,'ocupada','2025-05-03 21:15:46'),(26,'ocupada','2025-05-05 13:28:24'),(27,'ocupada','2025-05-05 19:51:23'),(28,'ocupada','2025-05-05 23:10:33'),(29,'ocupada','2025-05-06 12:12:07'),(30,'ocupada','2025-05-06 12:13:43'),(31,'ocupada','2025-05-06 17:29:59');
/*!40000 ALTER TABLE `mesas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` text,
  `precio` decimal(10,2) NOT NULL,
  `imagen_producto` varchar(255) NOT NULL,
  `truck_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `truck_id` (`truck_id`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`truck_id`) REFERENCES `trucks` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Pizza Truffle','Pizza con trufa negra y queso azul',12.99,'trufle.jpg',1),(2,'Margherita Clasica','Tomate, mozzarlla y albahaca fresca',10.50,'margherita.jpg',1),(3,'Taco al Pastor','Taco con cerdo adobado, piña y guacamole',3.99,'https://images.unsplash.com/photo-1608032077036-20d20084740f',2),(4,'Quesadilla de Queso','Queso derretido en tortilla de harina',5.50,'https://images.unsplash.com/photo-1599974579681-0ac667a3e6be',2),(5,'Korean BBQ Bowl','Arroz con carne BBQ coreana y kimchi',11.99,'https://images.unsplash.com/photo-1617196038641-06d98cce1a04',3),(6,'Gyozas','Empanadillas rellenas de cerdo y vegetales',6.99,'https://images.unsplash.com/photo-1598866594237-21b86d0f5a43',3),(7,'Truffle Burger','Hamburguesa con queso azul y cebolla caramelizada',13.50,'https://images.unsplash.com/photo-1561758033-d89a9ad46330',4),(8,'Cheeseburger Clásica','Hamburguesa con queso cheddar y pepinillos',9.99,'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38',4);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaccion_detalles`
--

DROP TABLE IF EXISTS `transaccion_detalles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaccion_detalles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `transaccion_id` varchar(50) NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaccion_id` (`transaccion_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `transaccion_detalles_ibfk_1` FOREIGN KEY (`transaccion_id`) REFERENCES `transacciones` (`id`),
  CONSTRAINT `transaccion_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaccion_detalles`
--

LOCK TABLES `transaccion_detalles` WRITE;
/*!40000 ALTER TABLE `transaccion_detalles` DISABLE KEYS */;
INSERT INTO `transaccion_detalles` VALUES (1,'ed6c0522-1643-480c-a44d-e3d88feda217',2,1,10.50),(2,'ed6c0522-1643-480c-a44d-e3d88feda217',1,1,12.99),(3,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',1,1,12.99),(4,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',2,1,10.50),(5,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',3,2,3.99),(6,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',4,5,5.50),(7,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',6,11,6.99),(8,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',5,2,11.99),(9,'79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',7,10,13.50),(10,'1e43664f-764c-420e-bdf5-e8b4a5ffac2f',4,85,5.50),(11,'1e43664f-764c-420e-bdf5-e8b4a5ffac2f',3,10,3.99),(12,'e3ac1c3e-33d1-44bf-b587-941c0750ac0f',1,1,12.99),(13,'e3ac1c3e-33d1-44bf-b587-941c0750ac0f',2,1,10.50),(14,'1919bbc1-4a20-4988-8c89-99b232fdba45',1,14,12.99),(15,'1919bbc1-4a20-4988-8c89-99b232fdba45',3,1,3.99),(16,'1919bbc1-4a20-4988-8c89-99b232fdba45',4,1,5.50),(17,'0d78fdc2-b16c-4a90-9c18-7acf7f2a4b95',1,1,12.99),(18,'acd9f1d8-f8ad-4018-ac70-e67e1ff77fcb',2,1,10.50),(19,'3caf7c22-1037-4a5d-9030-fc52c57214f1',2,1,10.50),(20,'7cebe580-4845-48f2-b083-79f1afac4606',1,1,12.99),(21,'7cebe580-4845-48f2-b083-79f1afac4606',2,1,10.50),(22,'23db5ef3-5406-41d3-894c-0dc3cf428776',3,1,3.99),(23,'23db5ef3-5406-41d3-894c-0dc3cf428776',4,1,5.50),(24,'23db5ef3-5406-41d3-894c-0dc3cf428776',1,1,12.99),(25,'23db5ef3-5406-41d3-894c-0dc3cf428776',2,1,10.50),(26,'0af119f0-511c-4818-a00e-2e65609bf520',1,8,12.99),(27,'0af119f0-511c-4818-a00e-2e65609bf520',2,4,10.50),(28,'0af119f0-511c-4818-a00e-2e65609bf520',5,1,11.99),(29,'0af119f0-511c-4818-a00e-2e65609bf520',6,1,6.99),(30,'0af119f0-511c-4818-a00e-2e65609bf520',7,1,13.50),(31,'b510df56-84d8-494f-8f6f-57112670d5e1',1,1,12.99),(32,'1cbf4d19-679c-439b-8ae9-dd389251ca01',1,1,12.99),(33,'1d98ddac-96ee-4b41-b1e2-b7964746422f',1,2,12.99),(34,'83a80297-4402-45b8-af94-32c376c4e515',1,2,12.99),(35,'79c0d196-3354-4074-8e09-b5e09df00cbd',1,2,12.99),(36,'4af36d92-fbc5-4e50-b970-d04d2b466408',1,2,12.99),(37,'c8c131d6-25b1-443b-ba70-753add29ac7d',1,1,12.99),(38,'080da779-edab-4cc7-aded-a9516aefd5f7',1,1,12.99),(39,'33e7ede3-c522-4086-a5d0-ace482a9e0dd',1,6,12.99),(40,'33e7ede3-c522-4086-a5d0-ace482a9e0dd',2,2,10.50),(41,'33e7ede3-c522-4086-a5d0-ace482a9e0dd',5,1,11.99),(42,'dd2064be-3fe1-4b0e-8799-eca9998e1ee2',2,1,10.50),(43,'e59ae338-26d8-4b72-ba98-0ba26789f6e6',2,1,10.50),(44,'3d18ae55-f9c0-49a6-bdef-eb3a467c0a3a',3,1,3.99),(45,'3d18ae55-f9c0-49a6-bdef-eb3a467c0a3a',4,1,5.50),(46,'377c3593-9b3a-4f11-a689-750f28ca2b33',3,1,3.99),(47,'377c3593-9b3a-4f11-a689-750f28ca2b33',4,1,5.50);
/*!40000 ALTER TABLE `transaccion_detalles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `id` varchar(50) NOT NULL,
  `mesa_id` int NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha` datetime NOT NULL,
  `datos_adicionales` json DEFAULT NULL,
  `token_confirmacion` varchar(255) DEFAULT NULL,
  `fecha_confirmacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mesa_id` (`mesa_id`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`mesa_id`) REFERENCES `mesas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES ('080da779-edab-4cc7-aded-a9516aefd5f7',24,'tranferencia',12.99,'pendiente','2025-05-02 09:07:07','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmsvtzYAh97D2\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJJ2C8mDrO4oIT19Yg594p\"}','a10d7976-7fb7-4556-8d47-65f296b101a4',NULL),('0af119f0-511c-4818-a00e-2e65609bf520',22,'tarjeta',178.40,'completado','2025-05-01 08:39:04',NULL,'cc4a2dfe-7f84-4170-8a37-7ab834be0309',NULL),('0d78fdc2-b16c-4a90-9c18-7acf7f2a4b95',21,'tranferencia',12.99,'pendiente','2025-04-30 09:59:44','{\"correo\": \"bryanfloresmolina08@gmail.com\", \"nombre\": \"bryan\", \"stripe_customer_id\": \"cus_SE3HahJiVLxJM2\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RJbAnC8mDrO4oIT1nWD4Zbk\"}','86a2c1e5-38ba-4ad5-ba69-9610bcbca4f8',NULL),('1919bbc1-4a20-4988-8c89-99b232fdba45',21,'tranferencia',191.35,'pendiente','2025-04-30 09:03:01','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"alejandro\", \"stripe_customer_id\": \"cus_SE2MjqjiKRlcSb\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RJaHuC8mDrO4oIT0Y8OrZxA\"}','62b629a3-bdd8-4091-94ec-fdf60ea8dd08',NULL),('1cbf4d19-679c-439b-8ae9-dd389251ca01',24,'tranferencia',12.99,'pendiente','2025-05-02 08:48:49','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmatGJHdWKXR0\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJ1KC8mDrO4oIT0mXwS2hw\"}','97b3a040-01b2-49d9-b125-1dff6919f4c1',NULL),('1d98ddac-96ee-4b41-b1e2-b7964746422f',24,'tranferencia',25.98,'pendiente','2025-05-02 08:53:32','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmf5kvTn2K5pA\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJ5tC8mDrO4oIT16Ys8Cs7\"}','5572f83a-2f81-426a-9141-ae296d3ad8ed',NULL),('1e43664f-764c-420e-bdf5-e8b4a5ffac2f',16,'tarjeta',507.40,'completado','2025-04-27 12:25:52',NULL,'8edf475e-ba6c-48a8-9e94-4d7e652072cf',NULL),('23db5ef3-5406-41d3-894c-0dc3cf428776',21,'tarjeta',32.98,'completado','2025-04-30 11:27:10',NULL,'b2ff5cd5-c653-44ab-ab7a-fbee1e0fca08',NULL),('33e7ede3-c522-4086-a5d0-ace482a9e0dd',28,'tarjeta',110.93,'completado','2025-05-05 19:15:31',NULL,'0b124d1a-d7a8-456c-bf11-dda7d1bfb0d7',NULL),('377c3593-9b3a-4f11-a689-750f28ca2b33',30,'tranferencia',9.49,'completado','2025-05-06 08:18:36','{\"correo\": \"juniorjaime721@gmail.com\", \"nombre\": \"Wilberto\", \"stripe_customer_id\": \"cus_SGH0pVXyVwZGKj\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RLkSGC8mDrO4oIT0RWMYMUL\"}','38e07167-e272-4ade-96a4-1c458922ae99','2025-05-06 08:19:20'),('3caf7c22-1037-4a5d-9030-fc52c57214f1',21,'tarjeta',10.50,'completado','2025-04-30 11:21:54',NULL,'dd938634-2f8f-491e-bc99-54a82478c48f',NULL),('3d18ae55-f9c0-49a6-bdef-eb3a467c0a3a',30,'tranferencia',9.49,'pendiente','2025-05-06 08:18:24','{\"correo\": \"juniorjaime721@gmail.com\", \"nombre\": \"Wilberto\", \"stripe_customer_id\": \"cus_SGH0o0MMXV5rT9\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RLkS5C8mDrO4oIT11BEKxUs\"}','63679788-b485-4eaf-b269-593827b5d9f7',NULL),('4af36d92-fbc5-4e50-b970-d04d2b466408',24,'tranferencia',25.98,'completado','2025-05-02 08:59:19','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmk0wSvGRfcc3\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJBUC8mDrO4oIT1SMYybEs\"}','f4758ba2-0720-4572-a61a-cb7cc7e61e66','2025-05-02 09:00:42'),('79002b86-5fe4-4f27-82b4-9b99d5b7d0f4',7,'tarjeta',294.84,'completado','2025-04-17 09:10:23',NULL,'cd897ce4-09de-433c-bf55-4f643b4a100a',NULL),('79c0d196-3354-4074-8e09-b5e09df00cbd',24,'tranferencia',25.98,'pendiente','2025-05-02 08:59:06','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmkq8olfqnUkP\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJBHC8mDrO4oIT1xdLCBMu\"}','5b09775f-5ea3-4540-8d06-06db1cd88a9d',NULL),('7cebe580-4845-48f2-b083-79f1afac4606',21,'tarjeta',23.49,'completado','2025-04-30 11:24:10',NULL,'2407d0ac-5e0f-438c-822d-1ea8682d57b1',NULL),('83a80297-4402-45b8-af94-32c376c4e515',24,'tranferencia',25.98,'pendiente','2025-05-02 08:53:44','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmfHHZnKLPljN\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJ66C8mDrO4oIT0epxnRnY\"}','15b85212-c033-4ed8-b337-73435683ea5b',NULL),('acd9f1d8-f8ad-4018-ac70-e67e1ff77fcb',21,'tarjeta',10.50,'completado','2025-04-30 11:15:40',NULL,'c6190b86-cd90-4f80-9a11-f208f63cff19',NULL),('b510df56-84d8-494f-8f6f-57112670d5e1',24,'tranferencia',12.99,'pendiente','2025-05-02 08:48:36','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmaMKxO6StgAL\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJ17C8mDrO4oIT0pNNEat9\"}','9268f0c5-d242-4a40-96f6-a7fdffb842c3',NULL),('c8c131d6-25b1-443b-ba70-753add29ac7d',24,'tranferencia',12.99,'pendiente','2025-05-02 09:06:55','{\"correo\": \"20230542@ipopsa.edu.do\", \"nombre\": \"Alejandro\", \"stripe_customer_id\": \"cus_SEmsVGjn2H8H4f\", \"instrucciones_bancarias\": null, \"stripe_payment_intent_id\": \"pi_3RKJIqC8mDrO4oIT1OSJ20Mb\"}','761b20b4-5eb6-4c65-a8f8-9885e95adc84',NULL),('dd2064be-3fe1-4b0e-8799-eca9998e1ee2',29,'tarjeta',10.50,'completado','2025-05-06 08:14:10',NULL,'823eff1d-8e1e-478d-8604-1da7e74639fa',NULL),('e3ac1c3e-33d1-44bf-b587-941c0750ac0f',21,'tarjeta',23.49,'completado','2025-04-30 07:06:58',NULL,'a89045bb-52f4-41a4-a1f1-13684fe5e047',NULL),('e59ae338-26d8-4b72-ba98-0ba26789f6e6',30,'tarjeta',10.50,'completado','2025-05-06 08:15:48',NULL,'4794516b-8434-4798-b75c-31668ca10646',NULL),('ed6c0522-1643-480c-a44d-e3d88feda217',4,'tarjeta',23.49,'completado','2025-04-16 23:23:01',NULL,'411ff31c-b181-4e09-8c39-6287e31993be',NULL);
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trucks`
--

DROP TABLE IF EXISTS `trucks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trucks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_truck` varchar(100) NOT NULL,
  `estado_truck` enum('inactivo','activo') NOT NULL DEFAULT 'activo',
  `imagen_foodtruck` varchar(255) NOT NULL,
  `info_foodtruck` text,
  `especialidad` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trucks`
--

LOCK TABLES `trucks` WRITE;
/*!40000 ALTER TABLE `trucks` DISABLE KEYS */;
INSERT INTO `trucks` VALUES (1,'Pizza Paradise','activo','pizza-foodtruck.jpg','Pizzeria Gourmet • Ingredientes Premium Selectos','Especialidad: Pizza Truffle & Blue Cheese con cebolla caramelizada al vino tinto'),(2,'El Sabor Latino','activo','sabor-latino.jpg','Cocina Mexicana Autentica • Premiado 2024','Especialidad: Tacos al Pastor con piña asada, guacamole artesanal y salsas secretas'),(3,'Asian Fusion','activo','asian-fusion.jpg','Fusión Asiática Moderna • Chef Premiado Internacional','Especialidad: Korean BBQ Bowls con kimchi artesanal y salsa umami secreta'),(4,'Burger Paradise','activo','burguer-paradise.jpg','Hamburguesas Gourmet • Ingredientes Premium Selectos','Especialidad: Burger Truffle & Blue Cheese con cebolla caramelizada al vino tinto'),(5,'Sweet Cravings','activo','sweet-cravings.jpg','Postres irresistibles & café de especialidad','Especialidad: Donas artesanales rellenas & malteadas con toppings exóticos.'),(6,'Vegan Street Eats','activo','vegan-eats.jpg','Opciones plant-based y delicias sostenibles','Especialidad: Comida vegana de la mejor calidad a tu paladar y a tu mesa.');
/*!40000 ALTER TABLE `trucks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_desabilitados`
--

DROP TABLE IF EXISTS `user_desabilitados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_desabilitados` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `disabled_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_desabilitados`
--

LOCK TABLES `user_desabilitados` WRITE;
/*!40000 ALTER TABLE `user_desabilitados` DISABLE KEYS */;
INSERT INTO `user_desabilitados` VALUES (2,'mora','pbkdf2:sha256:1000000$shr6jEsOHE9wvXR2$e1fb282a75d0fcc6988a12a14380a0ba7c45d1ea841ec96147d76e51822cf582','mora@gmail.com','admin','2025-05-01 13:17:01','2025-05-01 13:17:01','2025-05-01 13:17:01'),(3,'jose','pbkdf2:sha256:1000000$QIt6IIHGM7ogxtbQ$1dd6831c966cce968a7ac2c3b6755985c09cee57b647b48e99ee0cf2db77d6aa','20230542@ipopsa.edu.do','admin','2025-04-13 12:56:54','2025-04-13 12:56:54','2025-04-13 12:56:54'),(4,'dario','pbkdf2:sha256:1000000$jwSaDDCkwmqkPPzv$b00a5231e0108725a2531c6874831eeb43996dcc9e471835d095adfe947a5f01','20230542@ipopsa.edu.do','admin','2025-04-13 12:57:12','2025-04-13 12:57:12','2025-04-13 12:57:12'),(5,'pedro','pbkdf2:sha256:1000000$bC5czWjaoK8R9d0v$020f25f23008bdea5f47f6fed16378318a54562a5d61cb4ba52f810b38d55347','20230542@ipopsa.edu.do','admin','2025-04-13 12:57:19','2025-04-13 12:57:19','2025-04-13 12:57:19'),(6,'luffy','pbkdf2:sha256:1000000$dFXKH6tdv4UE7sWR$27cf601b9105115218a8e8ee0cfc74457addc4fa3413d662e79352ea38ede352','20230542@ipopsa.edu.do','admin','2025-04-13 12:57:24','2025-04-13 12:57:24','2025-04-13 12:57:24');
/*!40000 ALTER TABLE `user_desabilitados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` enum('admin','empleado') DEFAULT 'empleado',
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `numero` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'alejandro','pbkdf2:sha256:1000000$VPX1m8wJPHmRT1V2$81c63a5dc7b2ab5e50fb4f826453e76159ff42c274f614c09a332cb72066d3ba','20230542@ipopsa.edu.do','admin','activo',NULL),(2,'mora','pbkdf2:sha256:1000000$shr6jEsOHE9wvXR2$e1fb282a75d0fcc6988a12a14380a0ba7c45d1ea841ec96147d76e51822cf582','mora@gmail.com','admin','inactivo',NULL),(3,'jose','pbkdf2:sha256:1000000$QIt6IIHGM7ogxtbQ$1dd6831c966cce968a7ac2c3b6755985c09cee57b647b48e99ee0cf2db77d6aa','20230542@ipopsa.edu.do','admin','inactivo',NULL),(4,'dario','pbkdf2:sha256:1000000$jwSaDDCkwmqkPPzv$b00a5231e0108725a2531c6874831eeb43996dcc9e471835d095adfe947a5f01','20230542@ipopsa.edu.do','admin','inactivo',NULL),(5,'pedro','pbkdf2:sha256:1000000$bC5czWjaoK8R9d0v$020f25f23008bdea5f47f6fed16378318a54562a5d61cb4ba52f810b38d55347','20230542@ipopsa.edu.do','admin','inactivo',NULL),(6,'luffy','pbkdf2:sha256:1000000$dFXKH6tdv4UE7sWR$27cf601b9105115218a8e8ee0cfc74457addc4fa3413d662e79352ea38ede352','20230542@ipopsa.edu.do','admin','inactivo',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-06 14:20:04
