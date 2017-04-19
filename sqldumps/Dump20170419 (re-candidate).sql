-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
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
-- Table structure for table `readingsCNN`
--

DROP TABLE IF EXISTS `readingsCNN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readingsCNN` (
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
-- Dumping data for table `readingsCNN`
--
-- ORDER BY:  `doc_id`,`candidates`,`dimensions`,`samples`,`iterations`,`dropout`,`test`

LOCK TABLES `readingsCNN` WRITE;
/*!40000 ALTER TABLE `readingsCNN` DISABLE KEYS */;
INSERT INTO `readingsCNN` (`doc_id`, `candidates`, `dimensions`, `samples`, `iterations`, `dropout`, `train_acc`, `val_acc`, `test`) VALUES (1,2,200,1883,30,0.5,1.0000000000,0.9920424403,'candidate'),(1,3,200,711,30,0.5,1.0000000000,0.9414519906,'candidate'),(1,4,200,711,30,0.5,1.0000000000,0.8066783829,'candidate'),(1,5,200,711,30,0.5,1.0000000000,0.6863572435,'candidate'),(1,6,200,535,30,0.5,0.9996105919,0.6806853583,'candidate'),(1,7,200,535,30,0.5,1.0000000000,0.6822429918,'candidate'),(1,8,200,535,30,0.5,0.9997079439,0.6401869164,'candidate'),(1,9,200,535,30,0.5,1.0000000000,0.6220145380,'candidate'),(1,10,200,535,30,0.5,1.0000000000,0.5943925237,'candidate'),(1,11,200,535,30,0.5,0.9993627867,0.5802888698,'candidate'),(1,12,200,535,30,0.5,0.9737149533,0.5451713396,'candidate'),(1,13,200,535,30,0.5,0.9929906543,0.5269590227,'candidate'),(1,14,200,535,30,0.5,0.9951602136,0.5881174905,'candidate'),(1,15,200,528,30,0.5,0.9946338384,0.5473484848,'candidate'),(1,16,200,528,30,0.5,0.9887540693,0.5532544387,'candidate'),(1,17,200,528,30,0.5,0.9764623955,0.5222717149,'candidate'),(1,18,200,528,30,0.5,0.9539655400,0.5339295110,'candidate'),(1,19,200,528,30,0.5,0.9914018692,0.5196811160,'candidate'),(1,20,200,528,30,0.5,0.9290956439,0.5047348485,'candidate');
/*!40000 ALTER TABLE `readingsCNN` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-19 12:39:18
