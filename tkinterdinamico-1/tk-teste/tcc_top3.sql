-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 02/12/2023 às 23:52
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `tcc_top3`
--
CREATE DATABASE IF NOT EXISTS tcc_top3;

use tcc_top3;

CREATE TABLE `usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(30) DEFAULT NULL,
  `senha` VARCHAR(16) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`)
);

INSERT INTO `usuario` (`id_usuario`, `username`, `senha`) VALUES
(1, 'user1', 'password1'),
(2, 'user2', 'password2'),
(3, 'user3', 'password3');

CREATE TABLE `cliente` (
  `id_cliente` INT NOT NULL AUTO_INCREMENT,
  `nome_cliente` VARCHAR(50) DEFAULT NULL,
  `cpf_cliente` VARCHAR(14) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `cpf_cliente` (`cpf_cliente`)
);

INSERT INTO `cliente` (`id_cliente`, `nome_cliente`, `cpf_cliente`) VALUES
(1, 'Fernanda Oliveira', '11122233345'),
(2, 'Rafaela Santos', '44455566678'),
(3, 'Gabriel Souza', '77788899912'),
(4, 'Luiz Pereira', '12345678900'),
(5, 'Paulo Vieira', '98765432100'),
(6, 'Amanda Lima', '33344455567'),
(7, 'Mariano Fernandes', '66677788812'),
(8, 'Jéssica Rodrigues', '22233344456'),
(9, 'Rodrigo Costa', '55566677712'),
(10, 'Carla Vieira', '88899912345');

CREATE TABLE `despachante` (
  `id_despachante` INT NOT NULL AUTO_INCREMENT,
  `nome_despachante` VARCHAR(50) DEFAULT NULL,
  `doc_despachante` VARCHAR(14) DEFAULT NULL,
  PRIMARY KEY (`id_despachante`),
  UNIQUE KEY `doc_despachante` (`doc_despachante`)
);

INSERT INTO `despachante` (`id_despachante`, `nome_despachante`, `doc_despachante`) VALUES
(1, 'João Silva', '12345678901'),
(2, 'Maria Santos', '98765432101'),
(3, 'Pedro Oliveira', '45678912301'),
(4, 'Ana Pereira', '78901234501'),
(5, 'Carlos Souza', '23456789012'),
(6, 'Mariana Lima', '89012345601'),
(7, 'Lucas Fernandes', '56789012301'),
(8, 'Camila Rodrigues', '90123456701'),
(9, 'Gustavo Vieira', '34567890123'),
(10, 'Larissa Costa', '67890123401');

CREATE TABLE `forma_pagamento` (
  `id_forma_pagamento` INT NOT NULL AUTO_INCREMENT,
  `nome_forma_pagamento` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_forma_pagamento`)
);

--
-- Despejando dados para a tabela `forma_pagamento`
--

CREATE TABLE `op_caixa` (
  `id_op_caixa` INT NOT NULL AUTO_INCREMENT,
  `nome_op_caixa` VARCHAR(30) DEFAULT NULL,
  `id_usuario` INT DEFAULT NULL,
  PRIMARY KEY (`id_op_caixa`),
  KEY `id_usuario` (`id_usuario`),
  FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
);

INSERT INTO `op_caixa` (`id_op_caixa`, `nome_op_caixa`, `id_usuario`) VALUES
(1, 'Bea', 1),
(2, 'Rodolfo', 2)
;

CREATE TABLE `saida` (
  `id_saida` INT NOT NULL AUTO_INCREMENT,
  `data_saida` DATE DEFAULT NULL,
  `descricao_saida` TEXT DEFAULT NULL,
  `valor_saida` FLOAT(5,2) DEFAULT NULL,
  `id_op_caixa` INT DEFAULT NULL,
  PRIMARY KEY (`id_saida`),
  KEY `id_op_caixa` (`id_op_caixa`),
  FOREIGN KEY (`id_op_caixa`) REFERENCES `op_caixa` (`id_op_caixa`)
);

INSERT INTO `saida` (`id_saida`, `data_saida`, `descricao_saida`, `valor_saida`, `id_op_caixa`) VALUES
(1, '2023-01-20', 'Papel', 30.00, 1),
(2, '2023-02-25', 'Lanche', 40.00, 2),
(3, '2023-03-30', 'Parafusos', 25.00, 1),
(4, '2023-04-15', 'Café', 35.00, 2),
(5, '2023-05-18', 'Energia', 45.00, 1),
(6, '2023-06-23', 'Água', 20.00, 2),
(7, '2023-07-28', 'Internet', 50.00, 1),
(8, '2023-08-31', 'Transporte', 55.00, 2),
(9, '2023-09-08', 'Transporte', 60.00, 1),
(10, '2023-10-18', 'Café', 70.00, 2)
;

CREATE TABLE `tipo_veiculo` (
  `id_tipo_veiculo` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`id_tipo_veiculo`)
);

INSERT INTO `tipo_veiculo` (`id_tipo_veiculo`, `nome`) VALUES
(1, 'Carro'),
(2, 'Moto'),
(3, 'Caminhão'),
(4, 'Van'),
(5, 'Ônibus')
;
-- Novas Tabelas
CREATE TABLE `servico_cliente` (
  `id_servico_cliente` INT NOT NULL AUTO_INCREMENT,
  `id_cliente` INT NOT NULL,
  `id_tipo_veiculo_cliente` INT NOT NULL,
  `id_op_caixa_cliente` INT NOT NULL,
  `placa` VARCHAR(7) NOT NULL,
  `valor_servico` FLOAT(5,2) NOT NULL,
  `data_entrada` DATE NOT NULL,
  PRIMARY KEY (`id_servico_cliente`)
);

CREATE TABLE `servico_despachante` (
  `id_servico_despachante` INT NOT NULL AUTO_INCREMENT,
  `id_despachante` INT NOT NULL,
  `id_tipo_veiculo_despachante` INT NOT NULL,
  `id_op_caixa_despachante` INT NOT NULL,
  `placa` VARCHAR(7) NOT NULL,
  `valor_servico` FLOAT(5,2) NOT NULL,
  `data_entrada` DATE NOT NULL,
  PRIMARY KEY (`id_servico_despachante`)
);

-- Adicionando chaves estrangeiras
ALTER TABLE `servico_cliente`
ADD CONSTRAINT `fk_cliente_servico_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
ADD CONSTRAINT `fk_tipo_veiculo_cliente_servico_cliente` FOREIGN KEY (`id_tipo_veiculo_cliente`) REFERENCES `tipo_veiculo` (`id_tipo_veiculo`),
ADD CONSTRAINT `fk_op_caixa_cliente_servico_cliente` FOREIGN KEY (`id_op_caixa_cliente`) REFERENCES `op_caixa` (`id_op_caixa`);

ALTER TABLE `servico_despachante`
ADD CONSTRAINT `fk_despachante_servico_despachante` FOREIGN KEY (`id_despachante`) REFERENCES `despachante` (`id_despachante`),
ADD CONSTRAINT `fk_tipo_veiculo_despachante_servico_despachante` FOREIGN KEY (`id_tipo_veiculo_despachante`) REFERENCES `tipo_veiculo` (`id_tipo_veiculo`),
ADD CONSTRAINT `fk_op_caixa_despachante_servico_despachante` FOREIGN KEY (`id_op_caixa_despachante`) REFERENCES `op_caixa` (`id_op_caixa`);

CREATE TABLE `entrada` (
  `id_entrada` INT NOT NULL AUTO_INCREMENT,
  `valor` FLOAT(5,2) DEFAULT NULL,
  `status_p` TINYINT(1) DEFAULT NULL,
  `id_servico_cliente` INT DEFAULT NULL,
  `id_servico_despachante` INT DEFAULT NULL,
  PRIMARY KEY (`id_entrada`),
  FOREIGN KEY (`id_servico_cliente`) REFERENCES `servico_cliente` (`id_servico_cliente`),
  FOREIGN KEY (`id_servico_despachante`) REFERENCES `servico_despachante` (`id_servico_despachante`)
);

INSERT INTO `servico_cliente` (`id_cliente`, `id_tipo_veiculo_cliente`, `id_op_caixa_cliente`, `placa`, `valor_servico`, `data_entrada`) VALUES
(1, 1, 1, 'ABC1234', 100.00, '2023-01-15'),
(2, 2, 2, 'DEF5678', 150.00, '2023-02-20'),
(3, 3, 1, 'GHI9012', 200.00, '2023-03-25'),
(4, 4, 2, 'JKL3456', 120.00, '2023-04-10'),
(5, 5, 1, 'MNO7890', 180.00, '2023-05-12'),
(6, 1, 2, 'PQR1234', 220.00, '2023-06-18'),
(7, 2, 1, 'STU5678', 130.00, '2023-07-22'),
(8, 3, 2, 'VWX9012', 190.00, '2023-08-30'),
(9, 4, 1, 'YZA3456', 210.00, '2023-09-05'),
(10, 5, 2, 'BCD7890', 140.00, '2023-10-14')
;

INSERT INTO `servico_despachante` (`id_despachante`, `id_tipo_veiculo_despachante`, `id_op_caixa_despachante`, `placa`, `valor_servico`, `data_entrada`) VALUES
(1, 1, 1, 'ABC1234', 100.00, '2023-01-15'),
(2, 2, 2, 'DEF5678', 150.00, '2023-02-20'),
(3, 3, 1, 'GHI9012', 200.00, '2023-03-25'),
(4, 4, 2, 'JKL3456', 120.00, '2023-04-10'),
(5, 5, 1, 'MNO7890', 180.00, '2023-05-12'),
(6, 1, 2, 'PQR1234', 220.00, '2023-06-18'),
(7, 2, 1, 'STU5678', 130.00, '2023-07-22'),
(8, 3, 2, 'VWX9012', 190.00, '2023-08-30'),
(9, 4, 1, 'YZA3456', 210.00, '2023-09-05'),
(10, 5, 2, 'BCD7890', 140.00, '2023-10-14')
;

INSERT INTO `entrada` (`id_entrada`, `valor`, `status_p`, `id_servico_cliente`, `id_servico_despachante`) VALUES
(1, 100.00, 1, 1, NULL),
(2, 150.00, 0, NULL, 2),
(3, 200.00, 1, 3, NULL),
(4, 120.00, 1, NULL, 4),
(5, 180.00, 0, 5, NULL),
(6, 220.00, 1, NULL, 6),
(7, 130.00, 0, 7, NULL),
(8, 190.00, 1, NULL, 8),
(9, 210.00, 0, 9, NULL),
(10, 140.00, 1, NULL, 10)
;



CREATE TABLE `relatorio_geral` (
`ID Entrada` int(11)
,`Data_Servico` date
,`Cliente_Despachante` varchar(50)
,`Valor_Serviço` FLOAT(5,2)
,`Pago` tinyint(1)
,`Data_Saída` date
,`Descrição_Saída` text
,`Valor_Saída` FLOAT(5,2)
);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `relatorio_individual`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `relatorio_individual` (
`ID Entrada` int(11)
,`Data_Servico` date
,`Cliente` varchar(50)
,`Despachante` varchar(50)
,`Tipo_Veículo` varchar(20)
,`Placa` varchar(7)
,`Valor_Serviço` FLOAT(5,2)
,`Pago` tinyint(1)
,`Nome_Op_Caixa` varchar(30)
);

-- --------------------------------------------------------
--
-- Estrutura para view `relatorio_geral`
--
DROP TABLE IF EXISTS `relatorio_geral`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `relatorio_geral` AS 
SELECT 
    `e`.`id_entrada` AS `ID Entrada`,
    `sc`.`data_entrada` AS `Data_Servico`,
    COALESCE(`c`.`nome_cliente`, `d`.`nome_despachante`) AS `Cliente_Despachante`,
    `sc`.`valor_servico` AS `Valor_Serviço`,
    `e`.`status_p` AS `Pago`,
    `sd`.`data_saida` AS `Data_Saída`,
    `sd`.`descricao_saida` AS `Descrição_Saída`,
    `sd`.`valor_saida` AS `Valor_Saída`
FROM
    `entrada` `e`
LEFT JOIN
    `servico_cliente` `sc` ON `e`.`id_servico_cliente` = `sc`.`id_servico_cliente`
LEFT JOIN
    `cliente` `c` ON `sc`.`id_cliente` = `c`.`id_cliente`
LEFT JOIN
    `saida` `sd` ON `sc`.`id_op_caixa_cliente` = `sd`.`id_op_caixa`
LEFT JOIN
    `servico_despachante` `sd2` ON `e`.`id_servico_despachante` = `sd2`.`id_servico_despachante`
LEFT JOIN
    `despachante` `d` ON `sd2`.`id_despachante` = `d`.`id_despachante`
WHERE
    `e`.`status_p` = 1;
-- --------------------------------------------------------

--
-- Estrutura para view `relatorio_individual`
--
DROP TABLE IF EXISTS `relatorio_individual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `relatorio_individual` AS 
SELECT 
    `e`.`id_entrada` AS `ID Entrada`,
    `sd`.`data_entrada` AS `Data_Servico`,
    NULL AS `Cliente`,
    `d`.`nome_despachante` AS `Despachante`,
    `tv`.`nome` AS `Tipo_Veículo`,
    `sd`.`placa` AS `Placa`,
    `sd`.`valor_servico` AS `Valor_Serviço`,
    `e`.`status_p` AS `Pago`,
    `op`.`nome_op_caixa` AS `Nome_Op_Caixa`
FROM 
    `entrada` `e`
LEFT JOIN 
    `servico_despachante` `sd` ON `e`.`id_servico_despachante` = `sd`.`id_servico_despachante`
LEFT JOIN 
    `despachante` `d` ON `sd`.`id_despachante` = `d`.`id_despachante`
LEFT JOIN 
    `tipo_veiculo` `tv` ON `sd`.`id_tipo_veiculo_despachante` = `tv`.`id_tipo_veiculo`
LEFT JOIN 
    `op_caixa` `op` ON `sd`.`id_op_caixa_despachante` = `op`.`id_op_caixa`
WHERE 
    `e`.`status_p` IS NULL OR `e`.`status_p` = 0;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
