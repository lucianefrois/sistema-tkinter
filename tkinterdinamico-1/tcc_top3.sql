-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 12/12/2023 às 05:50
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

-- --------------------------------------------------------

--
-- Estrutura para tabela `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `nome_cliente` varchar(50) NOT NULL,
  `doc_cliente` varchar(14) NOT NULL,
  `tipo_cliente` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nome_cliente`, `doc_cliente`, `tipo_cliente`) VALUES
(1, 'Fernanda Oliveira', '11122233345', 'despachante'),
(2, 'Rafaela Santos', '44455566678', 'despachante'),
(3, 'Gabriel Souza', '77788899912', 'despachante'),
(4, 'Luiz Pereira', '12345678900', 'despachante'),
(5, 'Paulo Vieira', '98765432100', 'despachante'),
(6, 'Amanda Lima', '33344455567', 'cliente'),
(7, 'Mariano Fernandes', '66677788812', 'cliente'),
(8, 'Jéssica Rodrigues', '22233344456', 'cliente'),
(9, 'Rodrigo Costa', '55566677712', 'Cliente'),
(10, 'Carla Vieira', '88899912345', 'Cliente'),
(11, 'joao almeida', '123456789', 'Clientes');

-- --------------------------------------------------------

--
-- Estrutura para tabela `entrada`
--

CREATE TABLE `entrada` (
  `id_entrada` int(11) NOT NULL,
  `id_servico_cliente` int(11) NOT NULL,
  `id_forma_pagamento` int(11) NOT NULL,
  `valor` float NOT NULL,
  `status_p` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `entrada`
--

INSERT INTO `entrada` (`id_entrada`, `id_servico_cliente`, `id_forma_pagamento`, `valor`, `status_p`) VALUES
(1, 1, 1, 100, 1),
(2, 2, 2, 150, 0),
(3, 3, 3, 200, 1),
(4, 4, 1, 120, 1),
(5, 5, 2, 180, 0),
(6, 6, 1, 220, 1),
(7, 7, 3, 130, 0),
(8, 8, 4, 190, 1),
(9, 9, 5, 210, 0),
(10, 10, 5, 140, 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `forma_pagamento`
--

CREATE TABLE `forma_pagamento` (
  `id_forma_pagamento` int(11) NOT NULL,
  `nome_forma_pagamento` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `forma_pagamento`
--

INSERT INTO `forma_pagamento` (`id_forma_pagamento`, `nome_forma_pagamento`) VALUES
(1, 'Débito'),
(2, 'Crédito'),
(3, 'Dinheiro'),
(4, 'Faturado'),
(5, 'PIX');

-- --------------------------------------------------------

--
-- Estrutura para tabela `op_caixa`
--

CREATE TABLE `op_caixa` (
  `id_op_caixa` int(11) NOT NULL,
  `nome_op_caixa` varchar(30) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `op_caixa`
--

INSERT INTO `op_caixa` (`id_op_caixa`, `nome_op_caixa`, `id_usuario`) VALUES
(1, 'Bea', 1),
(2, 'Rodolfo', 2);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `relatorio_geral`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `relatorio_geral` (
`ID Entrada` int(11)
,`Data_Servico` date
,`Cliente_Despachante` varchar(50)
,`Valor_Serviço` float
,`Pago` tinyint(1)
);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `relatorio_individual`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `relatorio_individual` (
`ID Entrada` int(11)
,`Data_Servico` date
,`Cliente_Despachante` varchar(50)
,`Tipo_Veículo` varchar(20)
,`Placa` varchar(7)
,`Valor_Serviço` float
,`Pago` tinyint(1)
,`Nome_Op_Caixa` varchar(30)
);

-- --------------------------------------------------------

--
-- Estrutura para tabela `saida`
--

CREATE TABLE `saida` (
  `id_saida` int(11) NOT NULL,
  `data_saida` date DEFAULT NULL,
  `descricao_saida` text DEFAULT NULL,
  `valor_saida` float DEFAULT NULL,
  `id_op_caixa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `saida`
--

INSERT INTO `saida` (`id_saida`, `data_saida`, `descricao_saida`, `valor_saida`, `id_op_caixa`) VALUES
(1, '2023-01-20', 'Papel', 30, 1),
(2, '2023-02-25', 'Lanche', 40, 2),
(3, '2023-03-30', 'Parafusos', 25, 1),
(4, '2023-04-15', 'Café', 35, 2),
(5, '2023-05-18', 'Energia', 45, 1),
(6, '2023-06-23', 'Água', 20, 2),
(7, '2023-07-28', 'Internet', 50, 1),
(8, '2023-08-31', 'Transporte', 55, 2),
(9, '2023-09-08', 'Chifre', 60, 1),
(10, '2023-10-18', 'Limpeza', 70, 2);

-- --------------------------------------------------------

--
-- Estrutura para tabela `servico_cliente`
--

CREATE TABLE `servico_cliente` (
  `id_servico_cliente` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_tipo_veiculo_cliente` int(11) NOT NULL,
  `id_op_caixa_cliente` int(11) NOT NULL,
  `placa` varchar(7) NOT NULL,
  `valor_servico` float NOT NULL,
  `data_entrada` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `servico_cliente`
--

INSERT INTO `servico_cliente` (`id_servico_cliente`, `id_cliente`, `id_tipo_veiculo_cliente`, `id_op_caixa_cliente`, `placa`, `valor_servico`, `data_entrada`) VALUES
(1, 1, 1, 1, 'ABC1234', 100, '2023-01-15'),
(2, 2, 2, 2, 'DEF5678', 150, '2023-02-20'),
(3, 3, 3, 1, 'GHI9012', 200, '2023-03-25'),
(4, 4, 4, 2, 'JKL3456', 120, '2023-04-10'),
(5, 5, 5, 1, 'MNO7890', 180, '2023-05-12'),
(6, 6, 1, 2, 'PQR1234', 220, '2023-06-18'),
(7, 7, 2, 1, 'STU5678', 130, '2023-07-22'),
(8, 8, 3, 2, 'VWX9012', 190, '2023-08-30'),
(9, 9, 4, 1, 'YZA3456', 210, '2023-09-05'),
(10, 10, 5, 2, 'BCD7890', 140, '2023-10-14');

-- --------------------------------------------------------

--
-- Estrutura para tabela `tipo_veiculo`
--

CREATE TABLE `tipo_veiculo` (
  `id_tipo_veiculo` int(11) NOT NULL,
  `nome` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `tipo_veiculo`
--

INSERT INTO `tipo_veiculo` (`id_tipo_veiculo`, `nome`) VALUES
(1, 'Carro'),
(2, 'Moto'),
(3, 'Caminhão'),
(4, 'Van'),
(5, 'Ônibus');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `username` varchar(30) DEFAULT NULL,
  `senha` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `username`, `senha`) VALUES
(1, 'user1', 'password1'),
(2, 'user2', 'password2'),
(3, 'user3', 'password3');

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `view_saidas`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `view_saidas` (
`id_saida` int(11)
,`data_saida` date
,`descricao_saida` text
,`valor_saida` float
,`nome_op_caixa` varchar(30)
);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `view_servico_cliente`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `view_servico_cliente` (
`id_servico` int(11)
,`Cliente` varchar(50)
,`Tipo Veiculo` varchar(20)
,`Placa` varchar(7)
,`Nome caixa` varchar(30)
,`Valor Servico` float
,`Data Entrada` date
);

-- --------------------------------------------------------

--
-- Estrutura para view `relatorio_geral`
--
DROP TABLE IF EXISTS `relatorio_geral`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `relatorio_geral`  AS SELECT `e`.`id_entrada` AS `ID Entrada`, `sc`.`data_entrada` AS `Data_Servico`, `c`.`nome_cliente` AS `Cliente_Despachante`, `sc`.`valor_servico` AS `Valor_Serviço`, `e`.`status_p` AS `Pago` FROM ((`entrada` `e` left join `servico_cliente` `sc` on(`e`.`id_servico_cliente` = `sc`.`id_servico_cliente`)) left join `cliente` `c` on(`sc`.`id_cliente` = `c`.`id_cliente`)) WHERE `e`.`status_p` = 1 ;

-- --------------------------------------------------------

--
-- Estrutura para view `relatorio_individual`
--
DROP TABLE IF EXISTS `relatorio_individual`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `relatorio_individual`  AS SELECT `e`.`id_entrada` AS `ID Entrada`, `sc`.`data_entrada` AS `Data_Servico`, `c`.`nome_cliente` AS `Cliente_Despachante`, `tv`.`nome` AS `Tipo_Veículo`, `sc`.`placa` AS `Placa`, `sc`.`valor_servico` AS `Valor_Serviço`, `e`.`status_p` AS `Pago`, `op`.`nome_op_caixa` AS `Nome_Op_Caixa` FROM ((((`entrada` `e` left join `servico_cliente` `sc` on(`e`.`id_servico_cliente` = `sc`.`id_servico_cliente`)) left join `cliente` `c` on(`sc`.`id_cliente` = `c`.`id_cliente`)) left join `tipo_veiculo` `tv` on(`sc`.`id_tipo_veiculo_cliente` = `tv`.`id_tipo_veiculo`)) left join `op_caixa` `op` on(`sc`.`id_op_caixa_cliente` = `op`.`id_op_caixa`)) WHERE `e`.`status_p` is null OR `e`.`status_p` = 0 ;

-- --------------------------------------------------------

--
-- Estrutura para view `view_saidas`
--
DROP TABLE IF EXISTS `view_saidas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_saidas`  AS SELECT `s`.`id_saida` AS `id_saida`, `s`.`data_saida` AS `data_saida`, `s`.`descricao_saida` AS `descricao_saida`, `s`.`valor_saida` AS `valor_saida`, `oc`.`nome_op_caixa` AS `nome_op_caixa` FROM (`saida` `s` left join `op_caixa` `oc` on(`s`.`id_op_caixa` = `oc`.`id_op_caixa`)) ;

-- --------------------------------------------------------

--
-- Estrutura para view `view_servico_cliente`
--
DROP TABLE IF EXISTS `view_servico_cliente`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `view_servico_cliente`  AS SELECT `sc`.`id_servico_cliente` AS `id_servico`, `c`.`nome_cliente` AS `Cliente`, `tv`.`nome` AS `Tipo Veiculo`, `sc`.`placa` AS `Placa`, `oc`.`nome_op_caixa` AS `Nome caixa`, `sc`.`valor_servico` AS `Valor Servico`, `sc`.`data_entrada` AS `Data Entrada` FROM (((`servico_cliente` `sc` left join `cliente` `c` on(`sc`.`id_cliente` = `c`.`id_cliente`)) left join `tipo_veiculo` `tv` on(`sc`.`id_tipo_veiculo_cliente` = `tv`.`id_tipo_veiculo`)) left join `op_caixa` `oc` on(`sc`.`id_op_caixa_cliente` = `oc`.`id_op_caixa`)) ;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `doc_cliente` (`doc_cliente`);

--
-- Índices de tabela `entrada`
--
ALTER TABLE `entrada`
  ADD PRIMARY KEY (`id_entrada`),
  ADD KEY `id_forma_pagamento` (`id_forma_pagamento`),
  ADD KEY `id_servico_cliente` (`id_servico_cliente`);

--
-- Índices de tabela `forma_pagamento`
--
ALTER TABLE `forma_pagamento`
  ADD PRIMARY KEY (`id_forma_pagamento`);

--
-- Índices de tabela `op_caixa`
--
ALTER TABLE `op_caixa`
  ADD PRIMARY KEY (`id_op_caixa`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Índices de tabela `saida`
--
ALTER TABLE `saida`
  ADD PRIMARY KEY (`id_saida`),
  ADD KEY `id_op_caixa` (`id_op_caixa`);

--
-- Índices de tabela `servico_cliente`
--
ALTER TABLE `servico_cliente`
  ADD PRIMARY KEY (`id_servico_cliente`),
  ADD KEY `fk_cliente_servico_cliente` (`id_cliente`),
  ADD KEY `fk_tipo_veiculo_cliente_servico_cliente` (`id_tipo_veiculo_cliente`),
  ADD KEY `fk_op_caixa_cliente_servico_cliente` (`id_op_caixa_cliente`);

--
-- Índices de tabela `tipo_veiculo`
--
ALTER TABLE `tipo_veiculo`
  ADD PRIMARY KEY (`id_tipo_veiculo`);

--
-- Índices de tabela `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de tabela `entrada`
--
ALTER TABLE `entrada`
  MODIFY `id_entrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `forma_pagamento`
--
ALTER TABLE `forma_pagamento`
  MODIFY `id_forma_pagamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `op_caixa`
--
ALTER TABLE `op_caixa`
  MODIFY `id_op_caixa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `saida`
--
ALTER TABLE `saida`
  MODIFY `id_saida` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `servico_cliente`
--
ALTER TABLE `servico_cliente`
  MODIFY `id_servico_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de tabela `tipo_veiculo`
--
ALTER TABLE `tipo_veiculo`
  MODIFY `id_tipo_veiculo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `entrada`
--
ALTER TABLE `entrada`
  ADD CONSTRAINT `entrada_ibfk_1` FOREIGN KEY (`id_forma_pagamento`) REFERENCES `forma_pagamento` (`id_forma_pagamento`),
  ADD CONSTRAINT `entrada_ibfk_2` FOREIGN KEY (`id_servico_cliente`) REFERENCES `servico_cliente` (`id_servico_cliente`);

--
-- Restrições para tabelas `op_caixa`
--
ALTER TABLE `op_caixa`
  ADD CONSTRAINT `op_caixa_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Restrições para tabelas `saida`
--
ALTER TABLE `saida`
  ADD CONSTRAINT `saida_ibfk_1` FOREIGN KEY (`id_op_caixa`) REFERENCES `op_caixa` (`id_op_caixa`);

--
-- Restrições para tabelas `servico_cliente`
--
ALTER TABLE `servico_cliente`
  ADD CONSTRAINT `fk_cliente_servico_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `fk_op_caixa_cliente_servico_cliente` FOREIGN KEY (`id_op_caixa_cliente`) REFERENCES `op_caixa` (`id_op_caixa`),
  ADD CONSTRAINT `fk_tipo_veiculo_cliente_servico_cliente` FOREIGN KEY (`id_tipo_veiculo_cliente`) REFERENCES `tipo_veiculo` (`id_tipo_veiculo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
