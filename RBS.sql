-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: rbs
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `Customer_id` int NOT NULL AUTO_INCREMENT,
  `Account` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Phone` varchar(20) NOT NULL,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`Customer_id`),
  UNIQUE KEY `Account_UNIQUE` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'m17395','mmmm1997','0919990707','陳信紅'),(2,'a28406','aaaa0329','0920000707','溫上翊'),(3,'y39517','yyyy1997','0920010706','石錦行'),(4,'d40628','dddd0329','0920031111','蔡昇諺'),(5,'a51739','aaaa1997','0920041105','劉品冠'),(6,'y62804','yyyy0329','0920061229','黃士傑');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_food_favorite`
--

DROP TABLE IF EXISTS `customer_food_favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_food_favorite` (
  `Customer_id` int NOT NULL,
  `Restaurant_id` int NOT NULL,
  `Food_id` int NOT NULL,
  PRIMARY KEY (`Customer_id`,`Restaurant_id`,`Food_id`),
  KEY `Food_id_idx` (`Food_id`),
  KEY `Restaurant_id_idx` (`Restaurant_id`),
  CONSTRAINT `cff_estaurant_id_fk` FOREIGN KEY (`Restaurant_id`) REFERENCES `restaurant` (`Restaurant_id`),
  CONSTRAINT `cff_ustomer_id_fk` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`Customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_food_favorite`
--

LOCK TABLES `customer_food_favorite` WRITE;
/*!40000 ALTER TABLE `customer_food_favorite` DISABLE KEYS */;
INSERT INTO `customer_food_favorite` VALUES (1,1,1),(3,2,1),(2,1,2);
/*!40000 ALTER TABLE `customer_food_favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_restaurant_favorite`
--

DROP TABLE IF EXISTS `customer_restaurant_favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_restaurant_favorite` (
  `Customer_id` int NOT NULL,
  `Restaurant_id` int NOT NULL,
  PRIMARY KEY (`Customer_id`,`Restaurant_id`),
  KEY `restaurant_id_fk_idx` (`Restaurant_id`),
  CONSTRAINT `crf_customer_id_fk` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`Customer_id`),
  CONSTRAINT `crf_restaurant_id_fk` FOREIGN KEY (`Restaurant_id`) REFERENCES `restaurant` (`Restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_restaurant_favorite`
--

LOCK TABLES `customer_restaurant_favorite` WRITE;
/*!40000 ALTER TABLE `customer_restaurant_favorite` DISABLE KEYS */;
INSERT INTO `customer_restaurant_favorite` VALUES (1,1),(3,1),(1,2),(2,2),(2,3);
/*!40000 ALTER TABLE `customer_restaurant_favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food`
--

DROP TABLE IF EXISTS `food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food` (
  `Restaurant_id` int NOT NULL,
  `Food_id` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Available` int NOT NULL,
  `Notes` varchar(99) DEFAULT NULL,
  `URL` varchar(99) DEFAULT NULL,
  `Price` int NOT NULL,
  `Style` varchar(99) DEFAULT NULL,
  PRIMARY KEY (`Restaurant_id`,`Food_id`),
  CONSTRAINT `food_restaurant_fk` FOREIGN KEY (`Restaurant_id`) REFERENCES `restaurant` (`Restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food`
--

LOCK TABLES `food` WRITE;
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
INSERT INTO `food` VALUES (1,1,'滷肉飯',1,'','https://www.nccuandmeeatogether.com.tw/menu',30,'飯'),(1,2,'雞肉飯',1,'','https://www.nccuandmeeatogether.com.tw/menu',30,'飯'),(1,3,'陽春麵',0,'','https://www.nccuandmeeatogether.com.tw/menu',40,'麵'),(2,1,'牛肉丼飯',1,'','https://www.nccukiya.com.tw/menu',125,'飯'),(2,2,'豬肉丼飯',1,'','https://www.nccukiya.com.tw/menu',115,'飯'),(3,1,'蔬菜煎蛋飯',1,'','',65,'飯'),(3,2,'番茄牛肉飯',1,'','',95,'飯');
/*!40000 ALTER TABLE `food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group` (
  `Group_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`Group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
INSERT INTO `group` VALUES (1,'BinLive'),(2,'8ID'),(3,'GrassJelly');
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `Order_id` int NOT NULL,
  `Status` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `Order_time` datetime DEFAULT NULL,
  `Wait_time` int NOT NULL,
  `C_Comment` varchar(99) DEFAULT NULL,
  `C_Rating` int DEFAULT NULL,
  `C_comment_time` datetime DEFAULT NULL,
  `G_Comment` varchar(99) DEFAULT NULL,
  `G_Rating` int DEFAULT NULL,
  `G_comment_time` datetime DEFAULT NULL,
  `Customer_id` int DEFAULT NULL,
  `Restaurant_id` int NOT NULL,
  `Group_id` int DEFAULT NULL,
  PRIMARY KEY (`Order_id`),
  KEY `order_customer_id_fk_idx` (`Customer_id`),
  KEY `order_restaurant_id_fk_idx` (`Restaurant_id`),
  KEY `ordder_gp_id_fk_idx` (`Group_id`),
  CONSTRAINT `ordder_gp_id_fk` FOREIGN KEY (`Group_id`) REFERENCES `group` (`Group_id`),
  CONSTRAINT `order_customer_id_fk` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`Customer_id`),
  CONSTRAINT `order_restaurant_id_fk` FOREIGN KEY (`Restaurant_id`) REFERENCES `restaurant` (`Restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,'order','2023-05-08 17:16:15',5,'餐點完成速度很快',5,'2023-05-08 17:21:15',NULL,NULL,NULL,2,1,NULL),(2,'order','2023-05-09 12:13:25',10,NULL,4,'2023-05-09 12:21:12',NULL,NULL,NULL,3,3,NULL),(3,'order','2023-05-10 20:20:20',15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,3);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_food`
--

DROP TABLE IF EXISTS `order_food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_food` (
  `Order_id` int NOT NULL,
  `Restaurant_id` int NOT NULL,
  `Food_id` int NOT NULL,
  `Food_num` int NOT NULL,
  `Comment_time` datetime NOT NULL,
  `Rating` int DEFAULT NULL,
  `Comment` varchar(99) DEFAULT NULL,
  `Notes` varchar(99) DEFAULT NULL,
  PRIMARY KEY (`Order_id`,`Restaurant_id`,`Food_id`),
  KEY `of_restaurant_id_fk_idx` (`Restaurant_id`),
  CONSTRAINT `of_order_id_fk` FOREIGN KEY (`Order_id`) REFERENCES `order` (`Order_id`),
  CONSTRAINT `of_restaurant_id_fk` FOREIGN KEY (`Restaurant_id`) REFERENCES `restaurant` (`Restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_food`
--

LOCK TABLES `order_food` WRITE;
/*!40000 ALTER TABLE `order_food` DISABLE KEYS */;
INSERT INTO `order_food` VALUES (1,1,1,2,'2023-05-08 17:21:15',1,'我覺得不行',NULL),(1,1,2,2,'2023-05-08 17:23:15',2,'普通','加滷蛋'),(2,3,1,2,'2023-05-06 17:21:15',4,'好吃',NULL),(2,3,2,2,'2023-05-06 17:23:15',5,'超好吃','加大');
/*!40000 ALTER TABLE `order_food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `Group_id` int NOT NULL,
  `Customer_id` int NOT NULL,
  PRIMARY KEY (`Group_id`,`Customer_id`),
  KEY `regis_customer_id_fk_idx` (`Customer_id`),
  CONSTRAINT `regis_customer_id_fk` FOREIGN KEY (`Customer_id`) REFERENCES `customer` (`Customer_id`),
  CONSTRAINT `regis_gp_id_fk` FOREIGN KEY (`Group_id`) REFERENCES `group` (`Group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (1,1),(1,2),(2,3),(2,4),(3,5),(3,6);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `Restaurant_id` int NOT NULL AUTO_INCREMENT,
  `Account` varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Hours` varchar(45) NOT NULL,
  `Style` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Restaurant_id`),
  UNIQUE KEY `Account_UNIQUE` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,'k87654','kkkk8765','亨食天堂','臺北市文山區環山一道','10-22','中式'),(2,'j32109','jjjj3210','Ayikus','臺北市文山區指南路二段103號','10-22','日式'),(3,'y10987','yyyy1234','四五大街','臺北市文山區指南路二段45巷5號','11-21','中式');
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-21  1:47:36
