CREATE DATABASE  IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mydb`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answers` (
  `s_no` smallint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `user_guess` varchar(50) DEFAULT NULL,
  `q1` enum('1','2','3','4','5') DEFAULT NULL,
  `q2` enum('1','2','3','4','5') DEFAULT NULL,
  `q3` enum('1','2','3','4','5') DEFAULT NULL,
  `q4` enum('1','2','3','4','5') DEFAULT NULL,
  `q5` enum('1','2','3','4','5') DEFAULT NULL,
  `q6` enum('1','2','3','4','5') DEFAULT NULL,
  `q7` enum('1','2','3','4','5') DEFAULT NULL,
  `q8` enum('1','2','3','4','5') DEFAULT NULL,
  `q9` enum('1','2','3','4','5') DEFAULT NULL,
  `q10` enum('1','2','3','4','5') DEFAULT NULL,
  `q11` enum('1','2','3','4','5') DEFAULT NULL,
  `q12` enum('1','2','3','4','5') DEFAULT NULL,
  `q13` enum('1','2','3','4','5') DEFAULT NULL,
  `q14` enum('1','2','3','4','5') DEFAULT NULL,
  `q15` enum('1','2','3','4','5') DEFAULT NULL,
  `q16` enum('1','2','3','4','5') DEFAULT NULL,
  `q17` enum('1','2','3','4','5') DEFAULT NULL,
  `q18` enum('1','2','3','4','5') DEFAULT NULL,
  `q19` enum('1','2','3','4','5') DEFAULT NULL,
  `q20` enum('1','2','3','4','5') DEFAULT NULL,
  `q21` enum('1','2','3','4','5') DEFAULT NULL,
  `q22` enum('1','2','3','4','5') DEFAULT NULL,
  `q23` enum('1','2','3','4','5') DEFAULT NULL,
  `q24` enum('1','2','3','4','5') DEFAULT NULL,
  `q25` enum('1','2','3','4','5') DEFAULT NULL,
  `q26` enum('1','2','3','4','5') DEFAULT NULL,
  `q27` enum('1','2','3','4','5') DEFAULT NULL,
  `q28` enum('1','2','3','4','5') DEFAULT NULL,
  `q29` enum('1','2','3','4','5') DEFAULT NULL,
  `q30` enum('1','2','3','4','5') DEFAULT NULL,
  `q31` enum('1','2','3','4','5') DEFAULT NULL,
  `q32` enum('1','2','3','4','5') DEFAULT NULL,
  `q33` enum('1','2','3','4','5') DEFAULT NULL,
  `q34` enum('1','2','3','4','5') DEFAULT NULL,
  `q35` enum('1','2','3','4','5') DEFAULT NULL,
  `q36` enum('1','2','3','4','5') DEFAULT NULL,
  `q37` enum('1','2','3','4','5') DEFAULT NULL,
  `q38` enum('1','2','3','4','5') DEFAULT NULL,
  `q39` enum('1','2','3','4','5') DEFAULT NULL,
  `q40` enum('1','2','3','4','5') DEFAULT NULL,
  `q41` enum('1','2','3','4','5') DEFAULT NULL,
  `q42` enum('1','2','3','4','5') DEFAULT NULL,
  `q43` enum('1','2','3','4','5') DEFAULT NULL,
  `q44` enum('1','2','3','4','5') DEFAULT NULL,
  `q45` enum('1','2','3','4','5') DEFAULT NULL,
  `q46` enum('1','2','3','4','5') DEFAULT NULL,
  `q47` enum('1','2','3','4','5') DEFAULT NULL,
  `q48` enum('1','2','3','4','5') DEFAULT NULL,
  `q49` enum('1','2','3','4','5') DEFAULT NULL,
  `q50` enum('1','2','3','4','5') DEFAULT NULL,
  `q51` enum('1','2','3','4','5') DEFAULT NULL,
  `q52` enum('1','2','3','4','5') DEFAULT NULL,
  `q53` enum('1','2','3','4','5') DEFAULT NULL,
  `q54` enum('1','2','3','4','5') DEFAULT NULL,
  `q55` enum('1','2','3','4','5') DEFAULT NULL,
  `q56` enum('1','2','3','4','5') DEFAULT NULL,
  `q57` enum('1','2','3','4','5') DEFAULT NULL,
  `q58` enum('1','2','3','4','5') DEFAULT NULL,
  `q59` enum('1','2','3','4','5') DEFAULT NULL,
  `q60` enum('1','2','3','4','5') DEFAULT NULL,
  `career1` varchar(50) DEFAULT NULL,
  `career2` varchar(50) DEFAULT NULL,
  `career3` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`s_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest_questions`
--

DROP TABLE IF EXISTS `interest_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interest_questions` (
  `q_no` smallint NOT NULL AUTO_INCREMENT,
  `question` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`q_no`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest_questions`
--

LOCK TABLES `interest_questions` WRITE;
/*!40000 ALTER TABLE `interest_questions` DISABLE KEYS */;
INSERT INTO `interest_questions` VALUES (1,'I enjoy working with numbers and data'),(2,'I am interested in science and how things work'),(3,'I enjoy creative activities like art, music or writing'),(4,'I like helping people improve their lives'),(5,'I am interested in business and entrepreneurship'),(6,'I enjoy working outdoors'),(7,'I am interested in technology and innovation'),(8,'I enjoy teaching or guiding others'),(9,'I am interested in healthcare or medicine'),(10,'I like building or fixing things'),(11,'I enjoy debating and discussing ideas'),(12,'I am interested in finance and investments'),(13,'I enjoy working on computers or coding'),(14,'I like studying human behaviour and psychology'),(15,'I am interested in media, marketing or advertising'),(16,'I enjoy planning events or managing projects'),(17,'I am interested in law, justice or governance'),(18,'I enjoy in environmental or social causes'),(19,'I enjoy conducting experiments or research'),(20,'I enjoy exploring new cultures and travelling');
/*!40000 ALTER TABLE `interest_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personality_questions`
--

DROP TABLE IF EXISTS `personality_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personality_questions` (
  `q_no` smallint NOT NULL AUTO_INCREMENT,
  `question` varchar(100) DEFAULT NULL,
  `option1` varchar(100) DEFAULT NULL,
  `option2` varchar(100) DEFAULT NULL,
  `option3` varchar(100) DEFAULT NULL,
  `option4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`q_no`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personality_questions`
--

LOCK TABLES `personality_questions` WRITE;
/*!40000 ALTER TABLE `personality_questions` DISABLE KEYS */;
INSERT INTO `personality_questions` VALUES (1,'If you had access to a time machine, would you rather travel to','The past','The future','I\'d sell it','To new places, not in time'),(2,'What sounds like the worst idea to you?','Give away your social media','Travelling to the same place every vacation','You can\'t choose your outfit','Annoying boss'),(3,'You feel happiest when you','Solve technical issue','Solve friend\'s problem','Perform on stage','Create something'),(4,'Your friends will be at your place in 30 minutes, your actions?','Let\'s see what I can cook','Clean up ASAP','Gotta pick the right music','Guests? I don\'t think so'),(5,'Close your eyes and think of a happy place, what do you see?','A little mountain cabin far from any crowd','Some busy crossroads sparkling in neon lights','A private jet taking me somewhere','My own backyard with all my loved ones around'),(6,'You just won unlimited access to your favorite ride at the funfair. What is it going to be?','Bumper cars','Roller coaster','Merry-go-round','Swap for craft material'),(7,'Describe your ideal workout','Gym','No workout','Yoga','Running'),(8,'How much time do you spend on social media daily?','No time for that','< 1 hour','About three hours','24/7'),(9,'Which of those sounds most like your social media behavior?','Post a lot about myself','Scroll the feed','Share memes and posts','No social media'),(10,'You decide to paint the walls in your room for a change. Is it going to be?','Grey','Variety of colours','Blue','Green'),(11,'Pick your mood','Peaceful sunrise. Happy with where I am at','At the crossroads. Don\'t know where to go','Busy city. Something\'s always going on','Thunderstorm. Things aren\'t easy right now'),(12,'Time to fill that new empty wall. Will you go with','Abstract and simple art','A favourite quote','A photo collage','Something work-related'),(13,'You got a surprise bonus at work. How are you going to spend it?','Designer outlet','Throw a party','Private jet','Invest it'),(14,'Describe the perfect office space for you','My own office/workshop','Informal lounge','Cubicle','Coffee shop'),(15,'Would you rather be','World famous villian','Unrecognised hero','Always happy but poor','Richest one but forever alone'),(16,'Reward yourself. Pick one item','Brownies','Sundae','Salad','Fancy cake'),(17,'How important is friendship to you?','I have some close friends who mean the world to me, but I don\'t let people in my heart easily','I am my own best friend','I make friends easily, the more the merrier','I see every new person as a useful prospective contact for the future'),(18,'At school, you were mostly praised for','Patience and perseverance','Your ability to organize group work and help others','Your ability to make decisions and choices quickly','Your creativity'),(19,'On social media, you are mostly subsribed to','Travel and celebrity profiles','Everything fitness-related','I don\'t use social media','Motivating profiles of successful people'),(20,'How do you feel about failures in your life?','Past has passed. I keep moving forward','I\'ll write about it in my diary and maybe share it with others','I\'ll go for a good long run - always helps me reset my mind','I never fail - I take unexpected turns to succeed');
/*!40000 ALTER TABLE `personality_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills_questions`
--

DROP TABLE IF EXISTS `skills_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills_questions` (
  `q_no` smallint NOT NULL AUTO_INCREMENT,
  `question` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`q_no`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills_questions`
--

LOCK TABLES `skills_questions` WRITE;
/*!40000 ALTER TABLE `skills_questions` DISABLE KEYS */;
INSERT INTO `skills_questions` VALUES (1,'I am good at solving mathematical problems'),(2,'I can clearly explain ideas to others'),(3,'I am skilled at writing (essays, reports, stories)'),(4,'I can analyze complex information effectively'),(5,'I am good at using technology and digital tools'),(6,'I can manage my time effectively'),(7,'I am skilled at negotiating or persuading others'),(8,'I can work well under tight deadlines'),(9,'I am good at designing or creating visual content'),(10,'I can learn new skills quickly'),(11,'I am good at troubleshooting problems'),(12,'I can work effectively in a team'),(13,'I am skilled in research and gathering information'),(14,'I can handle multiple tasks at once'),(15,'I am good at making decisions based on data'),(16,'I can teach or mentor others effectively'),(17,'I am good at organising information systematically'),(18,'I can think critically and question assumptions'),(19,'I am skilled in hands-on or practical work'),(20,'I can stay focused for long periods');
/*!40000 ALTER TABLE `skills_questions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-17 19:58:10
