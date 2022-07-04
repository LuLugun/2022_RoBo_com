-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1:3304
-- 產生時間： 2022-06-24 04:03:51
-- 伺服器版本： 10.4.24-MariaDB
-- PHP 版本： 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `robo_com`
--

-- --------------------------------------------------------

--
-- 資料表結構 `api_test`
--

CREATE TABLE `api_test` (
  `input time` timestamp NOT NULL DEFAULT current_timestamp(),
  `number` int(11) NOT NULL,
  `value` float NOT NULL,
  `remark` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 傾印資料表的資料 `api_test`
--

INSERT INTO `api_test` (`input time`, `number`, `value`, `remark`) VALUES
('2022-06-12 14:38:06', 2, 2.6, NULL),
('2022-06-12 14:38:15', 3, 5.5, NULL),
('2022-06-12 14:38:22', 4, 7.5, NULL),
('2022-06-12 14:50:30', 5, 7.5, 'postman');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `api_test`
--
ALTER TABLE `api_test`
  ADD PRIMARY KEY (`number`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `api_test`
--
ALTER TABLE `api_test`
  MODIFY `number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
