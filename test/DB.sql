-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Máy chủ: localhost
-- Thời gian đã tạo: Th7 17, 2018 lúc 03:05 AM
-- Phiên bản máy phục vụ: 10.1.34-MariaDB
-- Phiên bản PHP: 7.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `DB`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `data`
--

CREATE TABLE `data` (
  `data` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `data`
--

INSERT INTO `data` (`data`, `updated_date`) VALUES
('sxz', '2018-02-02'),
('sxz', '2018-02-02'),
('dád', '2018-03-03'),
('dfsdf', '2018-04-04'),
('xc', '2018-05-03'),
('fhgfh', '2018-06-20'),
('dfs', '2018-02-01'),
('dád', '2018-03-03'),
('dfsdf', '2018-04-04'),
('xc', '2018-05-03'),
('fhgfh', '2018-06-20'),
('dfs', '2018-02-01'),
('dsadsad', '2018-01-01'),
('dsadsad', '2018-01-01'),
('sfdsfsdfsd', '2018-01-01'),
('sdfsldkfjlksd', '2018-04-04'),
('sdfsldkfjlksd', '2018-04-04'),
('sdfsldkfjlksd', '2018-05-06'),
('lsmdflds', '2018-01-03'),
('à', '2018-01-03'),
('loan', '2018-03-10'),
('dsfsd', '2017-12-10'),
('but', '2017-12-10'),
('but', '2017-12-10'),
('bsdf', '2017-12-20'),
('dying', '2018-01-11'),
('chan', '2017-11-11'),
('tt', '2018-02-10'),
('google', '2018-06-10'),
('facebook', '2018-06-06'),
('tweet', '2018-05-11'),
('fine', '2018-05-04');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
