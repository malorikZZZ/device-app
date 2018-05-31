CREATE DATABASE  IF NOT EXISTS `device` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `device`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: device
-- ------------------------------------------------------
-- Server version	5.7.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(301) NOT NULL,
  `description` longtext NOT NULL,
  `login` varchar(100) NOT NULL,
  `created` varchar(25) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `available` tinyint(1) NOT NULL,
  `image_url` longtext NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `devices_device_name` (`name`(255)),
  KEY `devices_category_id` (`category_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `devices_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'iPhone X','Apple iPhone','123','28-04-2018',1,1,'https://shop.gadgetufa.ru/images/upload/37562-iphone-x-64gb-space-gray_thumb256.jpg',1),(2,'Galaxy S9','Samsung Galaxy','123','28-04-2018',1,1,'http://img.x-hw.by/articles/382/small_logo.jpg',1),(3,'Xiaomi Mi5','Xiaomi Mi5','123','29-05-2018',1,1,'https://service.gadgetufa.ru/images/upload/products_xiaomi-mi5_thumb256.jpg',1);
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_category`
--

DROP TABLE IF EXISTS `devices_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(301) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `devices_category_category_name` (`name`(255))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_category`
--

LOCK TABLES `devices_category` WRITE;
/*!40000 ALTER TABLE `devices_category` DISABLE KEYS */;
INSERT INTO `devices_category` VALUES (1,'smartphone'),(2,'smartpad'),(3,'notebook');
/*!40000 ALTER TABLE `devices_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserv`
--

DROP TABLE IF EXISTS `reserv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reserv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(301) NOT NULL,
  `author` smallint(6) NOT NULL,
  `employee` smallint(6) NOT NULL,
  `device_id` int(11) NOT NULL,
  `day` varchar(20) NOT NULL,
  `created` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reserv_dev_id_id` (`device_id`),
  CONSTRAINT `reserv_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserv`
--

LOCK TABLES `reserv` WRITE;
/*!40000 ALTER TABLE `reserv` DISABLE KEYS */;
INSERT INTO `reserv` VALUES (14,'new',244,244,3,'2018-05-31','2018-05-31T04:27:30 '),(18,'new',244,244,2,'2018-06-02','2018-05-31T04:47:07 '),(19,'new',244,244,3,'2018-06-03','2018-05-31T04:47:13 '),(21,'new',244,244,1,'2018-06-01','2018-05-31T05:08:43 '),(24,'new',268,268,1,'2018-05-31','2018-05-31T05:16:25 '),(25,'new',268,268,2,'2018-05-31','2018-05-31T05:16:25 '),(26,'new',268,268,2,'2018-06-01','2018-05-31T05:16:25 ');
/*!40000 ALTER TABLE `reserv` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-31  5:52:33
