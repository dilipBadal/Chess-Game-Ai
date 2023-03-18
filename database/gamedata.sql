-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 18, 2023 at 05:40 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gamedata`
--

-- --------------------------------------------------------

--
-- Table structure for table `black_pieces`
--

CREATE TABLE `black_pieces` (
  `pawn1` varchar(255) NOT NULL DEFAULT '0',
  `pawn2` varchar(255) NOT NULL DEFAULT '0',
  `pawn3` varchar(255) NOT NULL DEFAULT '0',
  `pawn4` varchar(255) NOT NULL DEFAULT '0',
  `pawn5` varchar(255) NOT NULL DEFAULT '0',
  `pawn6` varchar(255) NOT NULL DEFAULT '0',
  `pawn7` varchar(255) NOT NULL DEFAULT '0',
  `pawn8` varchar(255) NOT NULL DEFAULT '0',
  `rook1` varchar(255) NOT NULL DEFAULT '0',
  `rook2` varchar(255) NOT NULL DEFAULT '0',
  `bishop1` varchar(255) NOT NULL DEFAULT '0',
  `bishop2` varchar(255) NOT NULL DEFAULT '0',
  `knight1` varchar(255) NOT NULL DEFAULT '0',
  `knight2` varchar(255) NOT NULL DEFAULT '0',
  `king1` varchar(255) NOT NULL DEFAULT '0',
  `queen1` varchar(255) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `black_pieces`
--

INSERT INTO `black_pieces` (`pawn1`, `pawn2`, `pawn3`, `pawn4`, `pawn5`, `pawn6`, `pawn7`, `pawn8`, `rook1`, `rook2`, `bishop1`, `bishop2`, `knight1`, `knight2`, `king1`, `queen1`, `user_id`) VALUES
('101', '111', '121', '131', '341', '151', '161', '171', '1', '71', '21', '51', '11', '61', '41', '31', 5),
('101', '111', '121', '131', '141', '151', '161', '171', '1', '71', '21', '51', '11', '61', '41', '31', 7);

-- --------------------------------------------------------

--
-- Table structure for table `user_data`
--

CREATE TABLE `user_data` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `username` varchar(16) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_data`
--

INSERT INTO `user_data` (`id`, `name`, `username`, `email`, `password`) VALUES
(5, 'Kavya', 'kavana123', 'princegamer48@gmail.com', 'db85c3ef11ceb11c'),
(7, 'Dilip', 'dbadal33', 'dilipbadal33@gmail.com', 'ccead32cb06ed98e');

-- --------------------------------------------------------

--
-- Table structure for table `white_pieces`
--

CREATE TABLE `white_pieces` (
  `pawn1` varchar(255) NOT NULL DEFAULT '0',
  `pawn2` varchar(255) NOT NULL DEFAULT '0',
  `pawn3` varchar(255) NOT NULL DEFAULT '0',
  `pawn4` varchar(255) NOT NULL DEFAULT '0',
  `pawn5` varchar(255) NOT NULL DEFAULT '0',
  `pawn6` varchar(255) NOT NULL DEFAULT '0',
  `pawn7` varchar(255) NOT NULL DEFAULT '0',
  `pawn8` varchar(255) NOT NULL DEFAULT '0',
  `rook1` varchar(255) NOT NULL DEFAULT '0',
  `rook2` varchar(255) NOT NULL DEFAULT '0',
  `bishop1` varchar(255) NOT NULL DEFAULT '0',
  `bishop2` varchar(255) NOT NULL DEFAULT '0',
  `knight1` varchar(255) NOT NULL DEFAULT '0',
  `knight2` varchar(255) NOT NULL DEFAULT '0',
  `king1` varchar(255) NOT NULL DEFAULT '0',
  `queen1` varchar(255) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `white_pieces`
--

INSERT INTO `white_pieces` (`pawn1`, `pawn2`, `pawn3`, `pawn4`, `pawn5`, `pawn6`, `pawn7`, `pawn8`, `rook1`, `rook2`, `bishop1`, `bishop2`, `knight1`, `knight2`, `king1`, `queen1`, `user_id`) VALUES
('601', '611', '621', '631', '641', '451', '661', '671', '701', '771', '721', '751', '711', '761', '741', '731', 5),
('601', '611', '621', '631', '641', '651', '461', '671', '701', '771', '721', '751', '711', '761', '741', '731', 7);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `black_pieces`
--
ALTER TABLE `black_pieces`
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `white_pieces`
--
ALTER TABLE `white_pieces`
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user_data`
--
ALTER TABLE `user_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `black_pieces`
--
ALTER TABLE `black_pieces`
  ADD CONSTRAINT `black_pieces_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Constraints for table `white_pieces`
--
ALTER TABLE `white_pieces`
  ADD CONSTRAINT `white_pieces_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
