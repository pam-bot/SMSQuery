-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: smsante
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

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
-- Current Database: `smsante`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `smsante` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `smsante`;

--
-- Table structure for table `outbreaks`
--

DROP TABLE IF EXISTS `outbreaks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outbreaks` (
  `location` varchar(100) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `longitude` decimal(8,6) DEFAULT NULL,
  `latitude` decimal(8,6) DEFAULT NULL,
  `presence` char(1) DEFAULT NULL,
  PRIMARY KEY (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outbreaks`
--

LOCK TABLES `outbreaks` WRITE;
/*!40000 ALTER TABLE `outbreaks` DISABLE KEYS */;
INSERT INTO `outbreaks` VALUES ('Bamako','Mali','locality',-8.000000,12.650000,'N'),('Beyla','Guinea','locality',-8.633333,8.683333,'Y'),('Bo','Sierra Leone','locality',11.740995,7.955179,'Y'),('Boende','Democratic Republic of the Congo','locality',19.200000,-0.733333,'Y'),('Boende Moke','Democratic Republic of the Congo','locality',20.750031,-0.381414,'N'),('Boffa','Guinea','locality',-14.039162,10.180825,'Y'),('Bombali','Sierra Leone','administrative_area_level_2',-12.163272,9.247584,'Y'),('Bomi','Liberia','administrative_area_level_1',-10.845147,6.756293,'Y'),('Bonthe','Sierra Leone','locality',-12.505000,7.526389,'Y'),('Conakry','Guinea','locality',-13.712222,9.509167,'Y'),('Coyah','Guinea','locality',-13.383333,9.700000,'Y'),('Dabola','Guinea','locality',-11.116667,10.750000,'Y'),('Dalaba','Guinea','locality',-9.383333,10.166667,'Y'),('Dinguiraye','Guinea','locality',-10.716667,11.300000,'N'),('Dubreka','Guinea','locality',-13.516667,9.783333,'Y'),('Forecariah','Guinea','locality',-13.083333,9.433333,'Y'),('Gbarpolu','Liberia','administrative_area_level_1',-10.080730,7.495264,'Y'),('Grand Bassa','Liberia','administrative_area_level_1',-9.812494,6.230845,'Y'),('Grand Cape Mount','Liberia','administrative_area_level_1',-11.071176,7.046776,'Y'),('Grand Gedeh','Liberia','administrative_area_level_1',-8.221298,5.922208,'Y'),('Grand Kru','Liberia','administrative_area_level_1',-8.221298,4.761386,'Y'),('Gueckedou','Guinea','locality',-10.133333,8.566667,'Y'),('Kailahun','Sierra Leone','locality',-10.573889,8.277222,'Y'),('Kambia','Sierra Leone','locality',-12.917652,9.126166,'Y'),('Kayes','Mali','locality',-11.445272,14.436788,'Y'),('Kenema','Sierra Leone','locality',-11.195717,7.863215,'Y'),('Kerouane','Guinea','locality',-9.016667,9.266667,'Y'),('Kindia','Guinea','locality',-12.850000,10.066667,'Y'),('Kissidougou','Guinea','locality',-10.100000,9.183333,'Y'),('Koinadugu','Sierra Leone','locality',-11.363630,9.516877,'Y'),('Kono','Sierra Leone','locality',-10.890310,8.766329,'Y'),('Kouroussa','Guinea','locality',-9.883333,10.650000,'Y'),('Lofa','Liberia','administrative_area_level_1',-9.723267,8.191118,'Y'),('Lokolia','Democratic Republic of the Congo','locality',20.562519,-0.631684,'Y'),('Lokula','Democratic Republic of the Congo','locality',20.653891,-0.420979,'N'),('Lola','Guinea','locality',-88.307812,37.318664,'Y'),('Macenta','Guinea','locality',-9.466667,8.550000,'Y'),('Margibi','Liberia','administrative_area_level_1',-10.304890,6.515187,'Y'),('Maryland','Liberia','administrative_area_level_1',-7.741670,4.725888,'Y'),('Mondombe','Democratic Republic of the Congo','locality',22.753945,-0.775840,'N'),('Montserrado','Liberia','administrative_area_level_1',-10.529611,6.552581,'Y'),('Moyamba','Sierra Leone','locality',-12.433333,8.160556,'Y'),('Nimba','Liberia','administrative_area_level_1',-8.660059,6.842761,'Y'),('Nzerekore','Guinea','locality',-8.816667,7.750000,'Y'),('Pita','Guinea','locality',-12.395582,11.059568,'Y'),('Port Loko','Sierra Leone','locality',-12.787500,8.766667,'Y'),('Pujehun','Sierra Leone','locality',-11.718056,7.350556,'Y'),('River Cess','Liberia','administrative_area_level_1',-9.456155,5.902533,'Y'),('River Gee','Liberia','administrative_area_level_1',-7.872160,5.260489,'Y'),('Siguiri','Guinea','locality',-9.166667,11.416667,'Y'),('Sikasso','Mali','locality',-5.666667,11.316667,'N'),('Sinoe','Liberia','administrative_area_level_1',-8.660059,5.498710,'Y'),('Telimele','Guinea','locality',-13.033333,10.900000,'Y'),('Tonkolili','Sierra Leone','locality',-11.794756,8.980427,'Y'),('Watsikengo','Democratic Republic of the Congo','locality',20.563259,-0.843500,'N'),('Yomou','Guinea','locality',-9.253300,7.566000,'Y');
/*!40000 ALTER TABLE `outbreaks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-30 15:45:03
