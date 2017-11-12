-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema sisgee
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sisgee
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sisgee` DEFAULT CHARACTER SET utf8 ;
USE `sisgee` ;

-- -----------------------------------------------------
-- Table `sisgee`.`Campus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Campus` (
  `idCampus` INT NOT NULL,
  `nomeCampus` CHAR(100) NOT NULL,
  PRIMARY KEY (`idCampus`),
  UNIQUE INDEX `idCampus_UNIQUE` (`idCampus` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`Curso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Curso` (
  `idCurso` INT NOT NULL AUTO_INCREMENT,
  `codigoCurso` VARCHAR(50) NOT NULL,
  `nomeCurso` VARCHAR(255) NOT NULL,
  `idCampus` INT NOT NULL,
  PRIMARY KEY (`idCurso`, `idCampus`),
  UNIQUE INDEX `codigoCurso_UNIQUE` (`codigoCurso` ASC),
  UNIQUE INDEX `idCurso_UNIQUE` (`idCurso` ASC),
  INDEX `fk_Curso_Campus1_idx` (`idCampus` ASC),
  CONSTRAINT `fk_Curso_Campus1`
    FOREIGN KEY (`idCampus`)
    REFERENCES `sisgee`.`Campus` (`idCampus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`Pessoa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Pessoa` (
  `idPessoa` INT NOT NULL,
  `cpf` CHAR(14) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `dataNascimento` DATE NULL,
  `tipoEndereco` VARCHAR(100) NULL,
  `endereco` VARCHAR(255) NULL,
  `numeroEndereco` VARCHAR(10) NULL,
  `complementoEndereco` VARCHAR(150) NULL,
  `bairroEndereco` VARCHAR(150) NULL,
  `cepEndereco` VARCHAR(15) NULL,
  `distritoEndereco` VARCHAR(150) NULL,
  `cidadeEndereco` VARCHAR(150) NULL,
  `estadoEndereco` VARCHAR(2) NULL,
  `paisEndereco` VARCHAR(100) NULL,
  `email` VARCHAR(150) NULL,
  `ddiResidencial` INT NULL,
  `dddResidencial` INT NULL,
  `telefoneResidencial` VARCHAR(30) NULL,
  `ddiComercial` INT NULL,
  `dddComercial` INT NULL,
  `telefoneComercial` VARCHAR(30) NULL,
  `ddiCelular` INT NULL,
  `dddCelular` INT NULL,
  `telefoneCelular` VARCHAR(30) NULL,
  PRIMARY KEY (`idPessoa`),
  UNIQUE INDEX `cpf_UNIQUE` (`cpf` ASC),
  UNIQUE INDEX `idPessoa_UNIQUE` (`idPessoa` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`Aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Aluno` (
  `idAluno` INT NOT NULL AUTO_INCREMENT,
  `matricula` VARCHAR(100) NOT NULL,
  `situacao` VARCHAR(25) NOT NULL,
  `idCurso` INT NOT NULL,
  `idPessoa` INT NOT NULL,
  PRIMARY KEY (`idAluno`, `idCurso`, `idPessoa`),
  INDEX `fk_Aluno_Curso1_idx` (`idCurso` ASC),
  INDEX `fk_Aluno_Pessoa1_idx` (`idPessoa` ASC),
  UNIQUE INDEX `idAluno_UNIQUE` (`idAluno` ASC),
  UNIQUE INDEX `matricula_UNIQUE` (`matricula` ASC),
  CONSTRAINT `fk_Aluno_Curso1`
    FOREIGN KEY (`idCurso`)
    REFERENCES `sisgee`.`Curso` (`idCurso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Aluno_Pessoa1`
    FOREIGN KEY (`idPessoa`)
    REFERENCES `sisgee`.`Pessoa` (`idPessoa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`AgenteIntegracao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`AgenteIntegracao` (
  `idAgenteIntegracao` INT NOT NULL AUTO_INCREMENT,
  `cnpjAgenteIntegracao` CHAR(14) NOT NULL,
  `nomeAgenteIntegracao` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idAgenteIntegracao`),
  UNIQUE INDEX `cnpjAgenteIntegracao_UNIQUE` (`cnpjAgenteIntegracao` ASC),
  UNIQUE INDEX `idAgenteIntegracao_UNIQUE` (`idAgenteIntegracao` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`Empresa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Empresa` (
  `idEmpresa` INT NOT NULL AUTO_INCREMENT,
  `cnpjEmpresa` CHAR(14) NOT NULL,
  `nomeEmpresa` VARCHAR(100) NOT NULL,
  `idAgenteIntegracao` INT NULL,
  PRIMARY KEY (`idEmpresa`),
  UNIQUE INDEX `cnpjEmpresa_UNIQUE` (`cnpjEmpresa` ASC),
  INDEX `fk_Empresa_AgenteIntegracao1_idx` (`idAgenteIntegracao` ASC),
  UNIQUE INDEX `idEmpresa_UNIQUE` (`idEmpresa` ASC),
  CONSTRAINT `fk_Empresa_AgenteIntegracao1`
    FOREIGN KEY (`idAgenteIntegracao`)
    REFERENCES `sisgee`.`AgenteIntegracao` (`idAgenteIntegracao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`Convenio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`Convenio` (
  `idConvenio` INT NOT NULL AUTO_INCREMENT,
  `numeroConvenio` CHAR(10) NOT NULL,
  `dataInicioConvenio` DATE NOT NULL,
  `dataFimConvenio` DATE NOT NULL,
  `idEmpresa` INT NOT NULL,
  UNIQUE INDEX `numeroConvenio_UNIQUE` (`numeroConvenio` ASC),
  PRIMARY KEY (`idConvenio`, `idEmpresa`),
  INDEX `fk_Convenio_Empresa1_idx` (`idEmpresa` ASC),
  UNIQUE INDEX `idConvenio_UNIQUE` (`idConvenio` ASC),
  CONSTRAINT `fk_Convenio_Empresa1`
    FOREIGN KEY (`idEmpresa`)
    REFERENCES `sisgee`.`Empresa` (`idEmpresa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`ProfessorOrientador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`ProfessorOrientador` (
  `idProfessorOrientador` INT NOT NULL AUTO_INCREMENT,
  `nomeProfessorOrientador` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`idProfessorOrientador`),
  UNIQUE INDEX `idProfessorOrientador_UNIQUE` (`idProfessorOrientador` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`TermoEstagio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`TermoEstagio` (
  `idTermoEstagio` INT NOT NULL AUTO_INCREMENT,
  `dataInicioTermoEstagio` DATE NOT NULL,
  `dataFimTermoEstagio` DATE NULL,
  `dataRescisaoTermoEstagio` DATE NULL,
  `situacaoTermoEstagio` VARCHAR(25) NOT NULL,
  `cargaHorariaTermoEstagio` TINYINT NOT NULL,
  `valorBolsa` FLOAT NOT NULL,
  `enderecoTermoEstagio` VARCHAR(255) NOT NULL,
  `numeroEnderecoTermoEstagio` VARCHAR(10) NOT NULL,
  `complementoEnderecoTermoEstagio` VARCHAR(150) NOT NULL,
  `bairroEnderecoTermoEstagio` VARCHAR(150) NOT NULL,
  `cepEnderecoTermoEstagio` VARCHAR(15) NOT NULL,
  `cidadeEnderecoTermoEstagio` VARCHAR(150) NOT NULL,
  `estadoEnderecoTermoEstagio` CHAR(2) NOT NULL,
  `eEstagioObrigatorio` TINYINT NOT NULL,
  `idProfessorOrientador` INT NULL,
  `idAluno` INT NOT NULL,
  `idConvenio` INT NOT NULL,
  PRIMARY KEY (`idTermoEstagio`, `idAluno`, `idConvenio`),
  INDEX `fk_TermoEstagio_ProfessorOrientador_idx` (`idProfessorOrientador` ASC),
  INDEX `fk_TermoEstagio_Aluno1_idx` (`idAluno` ASC),
  INDEX `fk_TermoEstagio_Convenio1_idx` (`idConvenio` ASC),
  UNIQUE INDEX `idTermoEstagio_UNIQUE` (`idTermoEstagio` ASC),
  CONSTRAINT `fk_TermoEstagio_ProfessorOrientador`
    FOREIGN KEY (`idProfessorOrientador`)
    REFERENCES `sisgee`.`ProfessorOrientador` (`idProfessorOrientador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TermoEstagio_Aluno1`
    FOREIGN KEY (`idAluno`)
    REFERENCES `sisgee`.`Aluno` (`idAluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TermoEstagio_Convenio1`
    FOREIGN KEY (`idConvenio`)
    REFERENCES `sisgee`.`Convenio` (`idConvenio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sisgee`.`TermoAditivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sisgee`.`TermoAditivo` (
  `idTermoAditivo` INT NOT NULL,
  `dataFimTermoAditivo` DATE NULL,
  `cargaHorariaTermoAditivo` TINYINT NOT NULL,
  `valorBolsaTermoAditivo` FLOAT NOT NULL,
  `enderecoTermoAditivo` VARCHAR(255) NOT NULL,
  `numeroEnderecoTermoAditivo` VARCHAR(10) NOT NULL,
  `complementoEnderecoTermoEstagio` VARCHAR(150) NOT NULL,
  `bairroEnderecoTermoAditivo` VARCHAR(150) NOT NULL,
  `cepEnderecoTermoAditivo` VARCHAR(15) NOT NULL,
  `cidadeEnderecoTermoAditivo` VARCHAR(150) NOT NULL,
  `estadoEnderecoTermoAditivo` VARCHAR(2) NOT NULL,
  `idTermoEstagio` INT NOT NULL,
  PRIMARY KEY (`idTermoAditivo`, `idTermoEstagio`),
  UNIQUE INDEX `idTermoEstagio_UNIQUE` (`idTermoAditivo` ASC),
  INDEX `fk_TermoAditivo_TermoEstagio1_idx` (`idTermoEstagio` ASC),
  CONSTRAINT `fk_TermoAditivo_TermoEstagio1`
    FOREIGN KEY (`idTermoEstagio`)
    REFERENCES `sisgee`.`TermoEstagio` (`idTermoEstagio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


INSERT INTO AgenteIntegracao (nomeAgenteIntegracao, cnpjAgenteIntegracao) VALUES 
('Abr Vencer R. Humanos', 8334959000175), 
('Abre  Ag. Brasileira de Estudante Ltda. ', 10329223000183), 
('Adepe - Assoc. de Desenv. Da Educ. e Prom. Do Estudante', 9525685000164), 
('Afamar – Assessoria RH', 289809000185), 
('Alliage – Consult. Ass. S/C Ltda', 68646500048), 
('Assoc. de Apoio ao Estudante - AERJ', 3543152000129), 
('Cia. de Est. PPM Human Resources Ltda - ME  ', 8029517000115), 
('Ciee – Centro de Integração Empresa Escola', 33661745000150), 
('Clave Consultoria Ltda.', 73574386000119), 
('DSRH – Desafios e Soluções em RH', 5266318000132), 
('Foco R.H. Ltda – Grupo Foco', 3038224000185), 
('Mudes – Fund. Mov. Univ. Desenv. E.S. ', 33663519000109), 
('Gestão de Talentos Seres ', 5316824000105), 
('Inst. Euvaldo Lodi Núcleo Regional - IEL', 9324352000177), 
('Inst. Nacional de Capacit. Educ. p/Trabalho Via de Acesso', 5699372000171), 
('Inst. Capacitare Consult.Empresarial Ltda.', 8466536000109), 
('Natpasi Consult. Empresarial Ltda.', 12076828000102), 
('Nube – Nucleo Bras. de Est. Ltda.', 2704396000183), 
('Parceria Consultoria Empresarial', 1194833000101), 
('People On Time Consult. Planej. e Servs Temporários Ltda.', 31571573000107), 
('Recrutare e Consult. Gestão de R.H.', 7620237000114), 
('Secretaria de Est. Do Trabalho e Renda ( Setrab Cecope )', 28317881000198), 
('Stag Central de Estágios SS Ltda.', 3658267000169), 
('Talentos Consult. Em R.H. Ltda.', 5166464000196)
 
