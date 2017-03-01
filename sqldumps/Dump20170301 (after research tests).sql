-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: tests
-- ------------------------------------------------------
-- Server version	5.7.17

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
-- Table structure for table `readingsOldCNN`
--

DROP TABLE IF EXISTS `readingsOldCNN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readingsOldCNN` (
  `doc_id` int(11) NOT NULL DEFAULT '0',
  `candidates` int(11) NOT NULL DEFAULT '0',
  `dimensions` int(11) NOT NULL DEFAULT '0',
  `samples` int(11) NOT NULL DEFAULT '0',
  `iterations` int(11) NOT NULL DEFAULT '0',
  `dropout` decimal(1,1) NOT NULL DEFAULT '0.0',
  `train_acc` decimal(11,10) DEFAULT NULL,
  `val_acc` decimal(11,10) DEFAULT NULL,
  `test` varchar(45) NOT NULL DEFAULT 'error',
  PRIMARY KEY (`doc_id`,`candidates`,`dimensions`,`samples`,`iterations`,`dropout`,`test`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readingsOldCNN`
--

LOCK TABLES `readingsOldCNN` WRITE;
/*!40000 ALTER TABLE `readingsOldCNN` DISABLE KEYS */;
INSERT INTO `readingsOldCNN` VALUES (1,2,200,3200,30,0.5,1.0000000000,0.9671875000,'candidate'),(1,2,200,3200,30,0.5,1.0000000000,0.9390625000,'run1-cand'),(1,3,200,3200,30,0.5,0.9998842590,0.9500000000,'candidate'),(1,3,200,3200,30,0.5,0.9995117188,0.9128906250,'run1-cand'),(1,4,200,3200,30,0.5,0.9887152780,0.9140625000,'candidate'),(1,4,200,3200,30,0.5,0.9967187500,0.9034375000,'run1-cand'),(1,5,50,3200,30,0.5,0.9918750000,0.8290625000,'dimensions'),(1,5,100,3200,30,0.5,0.9867187500,0.8734375000,'dimensions'),(1,5,200,320,30,0.5,0.9953125000,0.6812500000,'samples'),(1,5,200,1600,30,0.5,0.9996875000,0.8556250000,'samples'),(1,5,200,3200,30,0.0,0.9994531250,0.9009375000,'dropout'),(1,5,200,3200,30,0.1,1.0000000000,0.8996875000,'dropout'),(1,5,200,3200,30,0.2,0.9997656250,0.9021875000,'dropout'),(1,5,200,3200,30,0.3,0.9993750000,0.8903125000,'dropout'),(1,5,200,3200,30,0.4,0.9728906250,0.8978125000,'dropout'),(1,5,200,3200,30,0.5,0.9874305560,0.9037500000,'candidate'),(1,5,200,3200,30,0.5,0.9980468750,0.8931250000,'dimensions'),(1,5,200,3200,30,0.5,0.9959375000,0.9025000000,'dropout'),(1,5,200,3200,30,0.5,0.9976562500,0.9043750000,'run1-cand'),(1,5,200,3200,30,0.5,0.9915625000,0.9028125000,'samples'),(1,6,200,3200,30,0.5,0.9943287040,0.8906250000,'candidate'),(1,7,200,3200,30,0.5,0.9704861110,0.8200892860,'candidate'),(1,8,200,3200,30,0.5,0.9796006940,0.7570312500,'candidate'),(1,9,200,3200,30,0.5,0.9683256170,0.8173611110,'candidate');
/*!40000 ALTER TABLE `readingsOldCNN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readingsOldCNNCV`
--

DROP TABLE IF EXISTS `readingsOldCNNCV`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readingsOldCNNCV` (
  `doc_id` int(11) NOT NULL DEFAULT '0',
  `candidates` int(11) NOT NULL DEFAULT '0',
  `dimensions` int(11) NOT NULL DEFAULT '0',
  `samples` int(11) NOT NULL DEFAULT '0',
  `iterations` int(11) NOT NULL DEFAULT '0',
  `dropout` decimal(1,1) NOT NULL DEFAULT '0.0',
  `train_acc` decimal(11,10) DEFAULT NULL,
  `val_acc` decimal(11,10) DEFAULT NULL,
  `test` varchar(45) NOT NULL DEFAULT 'error',
  PRIMARY KEY (`doc_id`,`candidates`,`dimensions`,`samples`,`iterations`,`dropout`,`test`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readingsOldCNNCV`
--

LOCK TABLES `readingsOldCNNCV` WRITE;
/*!40000 ALTER TABLE `readingsOldCNNCV` DISABLE KEYS */;
INSERT INTO `readingsOldCNNCV` VALUES (1,5,200,320,30,0.5,1.0000000000,0.6750000000,'cv-fold-0'),(1,5,200,320,30,0.5,1.0000000000,0.6625000000,'cv-fold-1'),(1,5,200,320,30,0.5,1.0000000000,0.6575000000,'cv-fold-2'),(1,5,200,320,30,0.5,1.0000000000,0.6700000000,'cv-fold-3'),(1,5,200,320,30,0.5,1.0000000000,0.7050000000,'run1-fold-0'),(1,5,200,320,30,0.5,1.0000000000,0.6800000000,'run1-fold-1'),(1,5,200,1600,30,0.5,0.9990000000,0.8580000000,'cv-fold-0'),(1,5,200,1600,30,0.5,1.0000000000,0.8655000000,'cv-fold-1'),(1,5,200,1600,30,0.5,0.9993333333,0.8575000000,'cv-fold-2'),(1,5,200,1600,30,0.5,1.0000000000,0.8650000000,'cv-fold-3'),(1,5,200,1600,30,0.5,0.9993333333,0.8520000000,'run1-fold-0'),(1,5,200,1600,30,0.5,1.0000000000,0.8725000000,'run1-fold-1');
/*!40000 ALTER TABLE `readingsOldCNNCV` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-01 10:35:03
