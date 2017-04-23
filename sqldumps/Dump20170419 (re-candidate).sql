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

--
-- Table structure for table `readingsML`
--

DROP TABLE IF EXISTS `readingsML`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `readingsML` (
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
-- Dumping data for table `readingsML`
--
-- ORDER BY:  `doc_id`,`candidates`,`dimensions`,`samples`,`iterations`,`dropout`,`test`

LOCK TABLES `readingsML` WRITE;
/*!40000 ALTER TABLE `readingsML` DISABLE KEYS */;
INSERT INTO `readingsML` (`doc_id`, `candidates`, `dimensions`, `samples`, `iterations`, `dropout`, `train_acc`, `val_acc`, `test`) VALUES (1,2,0,1883,0,0.0,0.9980079681,0.9986737401,'ct_multi_nb'),(1,2,0,1883,0,0.0,1.0000000000,0.9973474801,'ct_svc'),(1,2,0,1883,0,0.0,0.9963479416,0.9946949602,'tfidf_multi_nb'),(1,2,0,1883,0,0.0,1.0000000000,1.0000000000,'tfidf_svc'),(1,3,0,711,0,0.0,0.9917936694,0.9882903981,'ct_multi_nb'),(1,3,0,711,0,0.0,1.0000000000,0.9859484778,'ct_svc'),(1,3,0,711,0,0.0,0.9812426729,0.9718969555,'tfidf_multi_nb'),(1,3,0,711,0,0.0,1.0000000000,1.0000000000,'tfidf_svc'),(1,4,0,711,0,0.0,0.9753846154,0.9156414763,'ct_multi_nb'),(1,4,0,711,0,0.0,1.0000000000,0.9630931459,'ct_svc'),(1,4,0,711,0,0.0,0.9459340659,0.8804920914,'tfidf_multi_nb'),(1,4,0,711,0,0.0,0.9991208791,0.9841827768,'tfidf_svc'),(1,5,0,711,0,0.0,0.9546413502,0.8720112518,'ct_multi_nb'),(1,5,0,711,0,0.0,1.0000000000,0.8804500703,'ct_svc'),(1,5,0,711,0,0.0,0.8945147679,0.8045007032,'tfidf_multi_nb'),(1,5,0,711,0,0.0,0.9933192686,0.9226441632,'tfidf_svc'),(1,6,0,535,0,0.0,0.9692367601,0.8146417445,'ct_multi_nb'),(1,6,0,535,0,0.0,1.0000000000,0.8473520249,'ct_svc'),(1,6,0,535,0,0.0,0.9104361371,0.7570093458,'tfidf_multi_nb'),(1,6,0,535,0,0.0,0.9961059190,0.8894080997,'tfidf_svc'),(1,7,0,535,0,0.0,0.9682910547,0.8785046729,'ct_multi_nb'),(1,7,0,535,0,0.0,1.0000000000,0.8958611482,'ct_svc'),(1,7,0,535,0,0.0,0.9198931909,0.8317757009,'tfidf_multi_nb'),(1,7,0,535,0,0.0,0.9939919893,0.9345794393,'tfidf_svc'),(1,8,0,535,0,0.0,0.9655373832,0.8808411215,'ct_multi_nb'),(1,8,0,535,0,0.0,1.0000000000,0.9042056075,'ct_svc'),(1,8,0,535,0,0.0,0.9249415888,0.8364485981,'tfidf_multi_nb'),(1,8,0,535,0,0.0,0.9962032710,0.9334112150,'tfidf_svc'),(1,9,0,535,0,0.0,0.9688473520,0.8753894081,'ct_multi_nb'),(1,9,0,535,0,0.0,1.0000000000,0.9096573209,'ct_svc'),(1,9,0,535,0,0.0,0.9286085151,0.8296988577,'tfidf_multi_nb'),(1,9,0,535,0,0.0,0.9974039460,0.9376947041,'tfidf_svc'),(1,10,0,535,0,0.0,0.9724299065,0.9149532710,'ct_multi_nb'),(1,10,0,535,0,0.0,1.0000000000,0.9261682243,'ct_svc'),(1,10,0,535,0,0.0,0.9285046729,0.8588785047,'tfidf_multi_nb'),(1,10,0,535,0,0.0,0.9978971963,0.9485981308,'tfidf_svc'),(1,11,0,535,0,0.0,0.9721750212,0.8895497026,'ct_multi_nb'),(1,11,0,535,0,0.0,1.0000000000,0.9073916737,'ct_svc'),(1,11,0,535,0,0.0,0.9311809686,0.8538657604,'tfidf_multi_nb'),(1,11,0,535,0,0.0,0.9972387426,0.9413763806,'tfidf_svc'),(1,12,0,535,0,0.0,0.9731308411,0.9096573209,'ct_multi_nb'),(1,12,0,535,0,0.0,1.0000000000,0.9267912773,'ct_svc'),(1,12,0,535,0,0.0,0.9369158879,0.8847352025,'tfidf_multi_nb'),(1,12,0,535,0,0.0,0.9972741433,0.9587227414,'tfidf_svc'),(1,13,0,535,0,0.0,0.9723220705,0.9137311287,'ct_multi_nb'),(1,13,0,535,0,0.0,1.0000000000,0.9273903666,'ct_svc'),(1,13,0,535,0,0.0,0.9369158879,0.8871315600,'tfidf_multi_nb'),(1,13,0,535,0,0.0,0.9980230050,0.9547088426,'tfidf_svc'),(1,14,0,535,0,0.0,0.9724632844,0.9018691589,'ct_multi_nb'),(1,14,0,535,0,0.0,1.0000000000,0.9339118825,'ct_svc'),(1,14,0,535,0,0.0,0.9385847797,0.8825100134,'tfidf_multi_nb'),(1,14,0,535,0,0.0,0.9981642190,0.9606141522,'tfidf_svc'),(1,15,0,528,0,0.0,0.9714330808,0.8983585859,'ct_multi_nb'),(1,15,0,528,0,0.0,1.0000000000,0.9248737374,'ct_svc'),(1,15,0,528,0,0.0,0.9299242424,0.8661616162,'tfidf_multi_nb'),(1,15,0,528,0,0.0,0.9977904040,0.9564393939,'tfidf_svc'),(1,16,0,528,0,0.0,0.9714412548,0.9082840237,'ct_multi_nb'),(1,16,0,528,0,0.0,1.0000000000,0.9218934911,'ct_svc'),(1,16,0,528,0,0.0,0.9331163066,0.8727810651,'tfidf_multi_nb'),(1,16,0,528,0,0.0,0.9980763540,0.9591715976,'tfidf_svc'),(1,17,0,528,0,0.0,0.9639275766,0.9003340757,'ct_multi_nb'),(1,17,0,528,0,0.0,1.0000000000,0.9248329621,'ct_svc'),(1,17,0,528,0,0.0,0.9274373259,0.8630289532,'tfidf_multi_nb'),(1,17,0,528,0,0.0,0.9976323120,0.9593541203,'tfidf_svc'),(1,18,0,528,0,0.0,0.9669867158,0.8916359811,'ct_multi_nb'),(1,18,0,528,0,0.0,1.0000000000,0.9284587059,'ct_svc'),(1,18,0,528,0,0.0,0.9346310667,0.8579694897,'tfidf_multi_nb'),(1,18,0,528,0,0.0,0.9975009865,0.9605470805,'tfidf_svc'),(1,19,0,528,0,0.0,0.9601246106,0.8774289985,'ct_multi_nb'),(1,19,0,528,0,0.0,1.0000000000,0.9053313403,'ct_svc'),(1,19,0,528,0,0.0,0.9196261682,0.8430493274,'tfidf_multi_nb'),(1,19,0,528,0,0.0,0.9980062305,0.9422022920,'tfidf_svc'),(1,20,0,528,0,0.0,0.9525331439,0.8678977273,'ct_multi_nb'),(1,20,0,528,0,0.0,1.0000000000,0.9228219697,'ct_svc'),(1,20,0,528,0,0.0,0.9100378788,0.8357007576,'tfidf_multi_nb'),(1,20,0,528,0,0.0,0.9982244318,0.9469696970,'tfidf_svc');
/*!40000 ALTER TABLE `readingsML` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-23 19:54:10
