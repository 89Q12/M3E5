-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
-- Host: localhost:3306
-- Generation Time: Jun 16, 2020 at 04:28 PM
-- Server version: 8.0.20-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `M3E5`
--

-- --------------------------------------------------------

--
-- Table structure for table `Error`
--

CREATE TABLE `Error` (
  `id` bigint NOT NULL,
  `guild_id` bigint NOT NULL,
  `error` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `guilds`
--

CREATE TABLE `guilds` (
  `guild_id` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` bigint NOT NULL,
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `guild_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  `role_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `guild_id` bigint NOT NULL,
  `standard_role_id` bigint NOT NULL DEFAULT '0',
  `dev_role_id` bigint NOT NULL DEFAULT '0',
  `mod_role_id` bigint NOT NULL DEFAULT '0',
  `admin_role_id` bigint NOT NULL DEFAULT '0',
  `imgwelcome_toggle` tinyint(1) NOT NULL DEFAULT '0',
  `imgwelcome_text` varchar(2000) NOT NULL DEFAULT 'V2VsY29tZSB0byB0aGUgc2VydmVyIHlvdSBsaXR0bGUgdXNlcg==',
  `levelsystem_toggle` tinyint(1) NOT NULL DEFAULT '0',
  `welcome_channel_id` bigint NOT NULL DEFAULT '0',
  `leave_channel_id` bigint NOT NULL DEFAULT '0',
  `lvl_channel_id` bigint NOT NULL DEFAULT '0',
  `cmd_channel_id` bigint NOT NULL DEFAULT '0',
  `prefix` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'LQ==',
  `Color` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'default()'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_info`
--

CREATE TABLE `user_info` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `guild_id` bigint NOT NULL,
  `warnings` int NOT NULL DEFAULT '0',
  `text_xp` bigint NOT NULL DEFAULT '0',
  `text_lvl` int NOT NULL DEFAULT '0',
  `voice_xp` int NOT NULL DEFAULT '0',
  `voice_lvl` int NOT NULL DEFAULT '0',
  `banned_at` datetime DEFAULT NULL,
  `banned_until` datetime DEFAULT NULL,
  `muted_at` datetime DEFAULT NULL,
  `muted_until` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Error`
--
ALTER TABLE `Error`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guild_id` (`guild_id`) USING BTREE,
  ADD KEY `date` (`date`) USING BTREE;

--
-- Indexes for table `guilds`
--
ALTER TABLE `guilds`
  ADD PRIMARY KEY (`guild_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guild_id` (`guild_id`) USING BTREE,
  ADD KEY `user_id` (`user_id`) USING BTREE;

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD UNIQUE KEY `role_id` (`role_id`),
  ADD KEY `guild_id` (`guild_id`) USING BTREE;

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD UNIQUE KEY `guild_id` (`guild_id`);

--
-- Indexes for table `user_info`
--
ALTER TABLE `user_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `muted_at` (`muted_at`),
  ADD KEY `banned_at` (`banned_at`) USING BTREE,
  ADD KEY `user_info_ibfk_1` (`guild_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Error`
--
ALTER TABLE `Error`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_info`
--
ALTER TABLE `user_info`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Error`
--
ALTER TABLE `Error`
  ADD CONSTRAINT `Error_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `roles`
--
ALTER TABLE `roles`
  ADD CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`) ON UPDATE CASCADE;

--
-- Constraints for table `settings`
--
ALTER TABLE `settings`
  ADD CONSTRAINT `settings_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_info`
--
ALTER TABLE `user_info`
  ADD CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guilds` (`guild_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
