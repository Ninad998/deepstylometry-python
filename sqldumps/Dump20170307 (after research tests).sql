-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: localdb
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
INSERT INTO `readingsOldCNN` VALUES (1,2,200,3200,30,0.5,1.0000000000,0.9671875000,'candidate'),(1,3,200,3200,30,0.5,0.9998842590,0.9500000000,'candidate'),(1,4,200,3200,30,0.5,0.9887152780,0.9140625000,'candidate'),(1,5,50,3200,30,0.5,0.9918750000,0.8290625000,'dimensions'),(1,5,100,3200,30,0.5,0.9867187500,0.8734375000,'dimensions'),(1,5,200,320,30,0.5,0.9953125000,0.6812500000,'samples'),(1,5,200,1600,30,0.5,0.9996875000,0.8556250000,'samples'),(1,5,200,3200,30,0.0,0.9994531250,0.9009375000,'dropout'),(1,5,200,3200,30,0.1,1.0000000000,0.8996875000,'dropout'),(1,5,200,3200,30,0.2,0.9997656250,0.9021875000,'dropout'),(1,5,200,3200,30,0.3,0.9993750000,0.8903125000,'dropout'),(1,5,200,3200,30,0.4,0.9728906250,0.8978125000,'dropout'),(1,5,200,3200,30,0.5,0.9874305560,0.9037500000,'candidate'),(1,5,200,3200,30,0.5,0.9980468750,0.8931250000,'dimensions'),(1,5,200,3200,30,0.5,0.9959375000,0.9025000000,'dropout'),(1,5,200,3200,30,0.5,0.9915625000,0.9028125000,'samples'),(1,6,200,3200,30,0.5,0.9943287040,0.8906250000,'candidate'),(1,7,200,3200,30,0.5,0.9704861110,0.8200892860,'candidate'),(1,8,200,3200,30,0.5,0.9796006940,0.7570312500,'candidate'),(1,9,200,3200,30,0.5,0.9683256170,0.8173611110,'candidate');
/*!40000 ALTER TABLE `readingsOldCNN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readingsOldCNNcv`
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
-- Dumping data for table `readingsOldCNNcv`
--

LOCK TABLES `readingsOldCNNCV` WRITE;
/*!40000 ALTER TABLE `readingsOldCNNcv` DISABLE KEYS */;
INSERT INTO `readingsOldCNNCV` VALUES (1,5,200,320,30,0.5,1.0000000000,0.6750000000,'cv-fold-0'),(1,5,200,320,30,0.5,1.0000000000,0.6625000000,'cv-fold-1'),(1,5,200,320,30,0.5,1.0000000000,0.6575000000,'cv-fold-2'),(1,5,200,320,30,0.5,1.0000000000,0.6700000000,'cv-fold-3'),(1,5,200,1600,30,0.5,0.9990000000,0.8580000000,'cv-fold-0'),(1,5,200,1600,30,0.5,1.0000000000,0.8655000000,'cv-fold-1'),(1,5,200,1600,30,0.5,0.9993333333,0.8575000000,'cv-fold-2'),(1,5,200,1600,30,0.5,1.0000000000,0.8650000000,'cv-fold-3');
/*!40000 ALTER TABLE `readingsOldCNNcv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readingsOldML`
--

DROP TABLE IF EXISTS `readingsOldML`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readingsOldML` (
  `doc_id` int(11) NOT NULL DEFAULT '0',
  `candidates` int(11) NOT NULL DEFAULT '0',
  `samples` int(11) NOT NULL DEFAULT '0',
  `train_acc` decimal(11,10) DEFAULT NULL,
  `val_acc` decimal(11,10) DEFAULT NULL,
  `test` varchar(45) NOT NULL DEFAULT 'error',
  PRIMARY KEY (`doc_id`,`candidates`,`samples`,`test`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readingsOldML`
--

LOCK TABLES `readingsOldML` WRITE;
/*!40000 ALTER TABLE `readingsOldML` DISABLE KEYS */;
INSERT INTO `readingsOldML` VALUES (1,2,3200,0.9744140625,0.9695312500,'candidate-ct_multi_nb'),(1,2,3200,1.0000000000,0.9968750000,'candidate-ct_svc'),(1,2,3200,0.9751953125,0.9703125000,'candidate-tfidf_multi_nb'),(1,2,3200,1.0000000000,0.9992187500,'candidate-tfidf_svc'),(1,3,3200,0.9756510417,0.9687500000,'candidate-ct_multi_nb'),(1,3,3200,1.0000000000,0.9942708333,'candidate-ct_svc'),(1,3,3200,0.9738281250,0.9718750000,'candidate-tfidf_multi_nb'),(1,3,3200,1.0000000000,1.0000000000,'candidate-tfidf_svc'),(1,4,3200,0.9719726563,0.9625000000,'candidate-ct_multi_nb'),(1,4,3200,1.0000000000,0.9925781250,'candidate-ct_svc'),(1,4,3200,0.9704101563,0.9617187500,'candidate-tfidf_multi_nb'),(1,4,3200,0.9999023438,1.0000000000,'candidate-tfidf_svc'),(1,5,320,0.9937500000,0.9468750000,'samples-ct_multi_nb'),(1,5,320,1.0000000000,0.9687500000,'samples-ct_svc'),(1,5,320,0.9906250000,0.9312500000,'samples-tfidf_multi_nb'),(1,5,320,1.0000000000,0.9843750000,'samples-tfidf_svc'),(1,5,1600,0.9782812500,0.9712500000,'samples-ct_multi_nb'),(1,5,1600,1.0000000000,0.9875000000,'samples-ct_svc'),(1,5,1600,0.9721875000,0.9631250000,'samples-tfidf_multi_nb'),(1,5,1600,1.0000000000,0.9968750000,'samples-tfidf_svc'),(1,5,3200,0.9755468750,0.9681250000,'candidate-ct_multi_nb'),(1,5,3200,1.0000000000,0.9890625000,'candidate-ct_svc'),(1,5,3200,0.9703906250,0.9665625000,'candidate-tfidf_multi_nb'),(1,5,3200,0.9999218750,0.9996875000,'candidate-tfidf_svc'),(1,5,3200,0.9725000000,0.9665625000,'samples-ct_multi_nb'),(1,5,3200,1.0000000000,0.9865625000,'samples-ct_svc'),(1,5,3200,0.9688281250,0.9628125000,'samples-tfidf_multi_nb'),(1,5,3200,0.9999218750,0.9996875000,'samples-tfidf_svc'),(1,6,3200,0.9734375000,0.9643229167,'candidate-ct_multi_nb'),(1,6,3200,1.0000000000,0.9875000000,'candidate-ct_svc'),(1,6,3200,0.9742187500,0.9697916667,'candidate-tfidf_multi_nb'),(1,6,3200,1.0000000000,0.9997395833,'candidate-tfidf_svc');
/*!40000 ALTER TABLE `readingsOldML` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-08 12:54:41
