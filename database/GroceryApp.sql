-- MySQL Script generated from MySQL Workbench
-- Edited: Wed Oct 23 16:19:01 2024

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema GroceryApp
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `GroceryApp` ;

-- -----------------------------------------------------
-- Schema GroceryApp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `GroceryApp` ;
USE `GroceryApp` ;

-- -----------------------------------------------------
-- Table `GroceryApp`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`Users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(50) NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `profile_pic_url` VARCHAR(50),
  `email` VARCHAR(50) NOT NULL,
  `phone_number` VARCHAR(15) NULL DEFAULT NULL,
  `password` CHAR(60) NOT NULL,
  `receive_sms_notifications` TINYINT NULL DEFAULT TRUE,
  `receive_email_notifications` TINYINT NULL DEFAULT TRUE,
  `preferred_notification_time` TIME NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE (`user_name`),
  UNIQUE (`email`)
);

-- -----------------------------------------------------
-- Table `GroceryApp`.`AllFoods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`AllFoods` (
  `food_id` INT NOT NULL AUTO_INCREMENT,
  `food_name` VARCHAR(50) NOT NULL,
  `expiration_days` INT NOT NULL CHECK (expiration_days > 0),
  `food_type` VARCHAR(50) NOT NULL,
  `recipe_id` INT NULL,
  PRIMARY KEY (`food_id`),
  UNIQUE (`food_name`),
  CONSTRAINT `fk_allfoods_recipe_id`
    FOREIGN KEY (`recipe_id`)
    REFERENCES `GroceryApp`.`Recipes` (`recipe_id`)
    ON DELETE SET NULL
);

-- -----------------------------------------------------
-- Table `GroceryApp`.`Recipes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`Recipes` (
  `recipe_id` INT NOT NULL AUTO_INCREMENT,
  `recipe_name` VARCHAR(50) NOT NULL,
  `recipe_url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`recipe_id`),
  UNIQUE (`recipe_name`)
);

-- -----------------------------------------------------
-- Table `GroceryApp`.`Inventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`Inventory` (
  `inventory_id` INT NOT NULL AUTO_INCREMENT,
  `food_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `user_id` INT NOT NULL,
  `expiration_date` DATE NOT NULL,
  `date_purchase` DATE NOT NULL,
  `status` ENUM('fresh', 'used', 'spoiled') NOT NULL DEFAULT 'fresh',
  `category` ENUM('green', 'yellow', 'red') NOT NULL DEFAULT 'green',
  PRIMARY KEY (`inventory_id`),
  CONSTRAINT `fk_inventory_food_id`
    FOREIGN KEY (`food_id`)
    REFERENCES `GroceryApp`.`AllFoods` (`food_id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_inventory_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `GroceryApp`.`Users` (`user_id`)
    ON DELETE CASCADE
);

CREATE INDEX `idx_inventory_food_id` ON `GroceryApp`.`Inventory` (`food_id` ASC) VISIBLE;
CREATE INDEX `idx_inventory_user_id` ON `GroceryApp`.`Inventory` (`user_id` ASC) VISIBLE;

-- -----------------------------------------------------
-- Table `GroceryApp`.`Ingredients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`Ingredients` (
  `ingredient_id` INT NOT NULL AUTO_INCREMENT,
  `recipe_id` INT NOT NULL,
  `food_id` INT NOT NULL,
  `quantity_required` INT NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  CONSTRAINT `fk_ingredients_recipe_id`
    FOREIGN KEY (`recipe_id`)
    REFERENCES `GroceryApp`.`Recipes` (`recipe_id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_ingredients_food_id`
    FOREIGN KEY (`food_id`)
    REFERENCES `GroceryApp`.`AllFoods` (`food_id`)
    ON DELETE CASCADE
);

CREATE INDEX `idx_ingredients_food_id` ON `GroceryApp`.`Ingredients` (`food_id` ASC) VISIBLE;

-- -------------------------------------------------------
-- Table `GroceryApp`.`UserUsage`
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `GroceryApp`.`UserUsage` (
  `usage_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `food_id` INT NOT NULL,
  `times_used` INT NOT NULL DEFAULT 0,
  `times_spoiled` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`usage_id`),
  CONSTRAINT `fk_userusage_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `GroceryApp`.`Users` (`user_id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_userusage_food_id`
    FOREIGN KEY (`food_id`)
    REFERENCES `GroceryApp`.`AllFoods` (`food_id`)
    ON DELETE CASCADE,
  CONSTRAINT `uc_userusage_user_id_food_id` UNIQUE (`user_id`, `food_id`)
);

CREATE INDEX `idx_userusage_user_id` ON `GroceryApp`.`UserUsage` (`user_id` ASC) VISIBLE;
CREATE INDEX `idx_userusage_food_id` ON `GroceryApp`.`UserUsage` (`food_id` ASC) VISIBLE;

-- -----------------------------------------------------
-- View `GroceryApp`.`RecipeSuggestions`
-- -----------------------------------------------------
CREATE OR REPLACE VIEW `RecipeSuggestions` AS
SELECT 
    r.recipe_id, 
    r.recipe_name, 
    r.recipe_url, 
    i.user_id
FROM 
    Recipes r
JOIN 
    Ingredients ing ON r.recipe_id = ing.recipe_id
JOIN 
    Inventory i ON ing.food_id = i.food_id
WHERE 
    i.category = 'yellow' OR i.category = 'red';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
