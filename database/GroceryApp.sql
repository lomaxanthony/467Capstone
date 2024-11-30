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
  `profile_pic_url` VARCHAR(2083),
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

CREATE INDEX `idx_recipes_user_id` ON `GroceryApp`.`Recipes` (`user_id` ASC) VISIBLE;

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

-- Insert the 100 most common foods into `AllFoods`
INSERT INTO `GroceryApp`.`AllFoods` (`food_name`, `expiration_days`, `food_type`, `recipe_id`)
VALUES
('Apple', 7, 'Fruit', 1),
('Banana', 7, 'Fruit', 2),
('Carrot', 30, 'Vegetable', 3),
('Chicken Breast', 5, 'Protein', 4),
('Spinach', 5, 'Vegetable', 5),
('Tomato', 7, 'Vegetable', 6),
('Potato', 30, 'Vegetable', 7),
('Onion', 30, 'Vegetable', 8),
('Garlic', 30, 'Vegetable', 9),
('Lettuce', 7, 'Vegetable', 10),
('Egg', 14, 'Protein', 11),
('Cheese', 30, 'Dairy', 12),
('Milk', 7, 'Dairy', 13),
('Yogurt', 14, 'Dairy', 14),
('Bread', 7, 'Grain', 15),
('Rice', 180, 'Grain', 16),
('Pasta', 180, 'Grain', 17),
('Beef', 5, 'Protein', 18),
('Pork', 5, 'Protein', 19),
('Salmon', 3, 'Protein', 20),
('Tuna', 3, 'Protein', 21),
('Cucumber', 7, 'Vegetable', 22),
('Bell Pepper', 7, 'Vegetable', 23),
('Zucchini', 14, 'Vegetable', 24),
('Sweet Potato', 30, 'Vegetable', 25),
('Avocado', 7, 'Fruit', 26),
('Strawberry', 7, 'Fruit', 27),
('Blueberry', 7, 'Fruit', 28),
('Peach', 7, 'Fruit', 29),
('Grapes', 7, 'Fruit', 30),
('Pineapple', 7, 'Fruit', 31),
('Mango', 7, 'Fruit', 32),
('Papaya', 7, 'Fruit', 33),
('Melon', 7, 'Fruit', 34),
('Lemon', 14, 'Fruit', 35),
('Orange', 14, 'Fruit', 36),
('Coconut', 30, 'Fruit', 37),
('Kiwi', 7, 'Fruit', 38),
('Plum', 7, 'Fruit', 39),
('Cherries', 7, 'Fruit', 40),
('Raspberries', 7, 'Fruit', 41),
('Blackberries', 7, 'Fruit', 42),
('Ginger', 30, 'Spice', 43),
('Cinnamon', 180, 'Spice', 44),
('Turmeric', 180, 'Spice', 45),
('Nutmeg', 180, 'Spice', 46),
('Chili Powder', 180, 'Spice', 47),
('Cumin', 180, 'Spice', 48),
('Paprika', 180, 'Spice', 49),
('Oregano', 180, 'Herb', 50),
('Basil', 7, 'Herb', 51),
('Thyme', 7, 'Herb', 52),
('Rosemary', 7, 'Herb', 53),
('Parsley', 7, 'Herb', 54),
('Sage', 7, 'Herb', 55),
('Dill', 7, 'Herb', 56),
('Bay Leaves', 180, 'Herb', 57),
('Mint', 7, 'Herb', 58),
('Chives', 7, 'Herb', 59),
('Coriander', 7, 'Herb', 60),
('Fennel', 7, 'Herb', 61),
('Almonds', 180, 'Nuts', 62),
('Walnuts', 180, 'Nuts', 63),
('Pistachios', 180, 'Nuts', 64),
('Cashews', 180, 'Nuts', 65),
('Peanuts', 180, 'Nuts', 66),
('Hazelnuts', 180, 'Nuts', 67),
('Chia Seeds', 180, 'Seeds', 68),
('Flax Seeds', 180, 'Seeds', 69),
('Pumpkin Seeds', 180, 'Seeds', 70),
('Sunflower Seeds', 180, 'Seeds', 71),
('Sesame Seeds', 180, 'Seeds', 72),
('Quinoa', 180, 'Grain', 73),
('Barley', 180, 'Grain', 74),
('Buckwheat', 180, 'Grain', 75),
('Millet', 180, 'Grain', 76),
('Farro', 180, 'Grain', 77),
('Oats', 180, 'Grain', 78),
('Chickpeas', 180, 'Legume', 79),
('Lentils', 180, 'Legume', 80),
('Black Beans', 180, 'Legume', 81),
('Kidney Beans', 180, 'Legume', 82),
('Peas', 180, 'Legume', 83),
('Edamame', 180, 'Legume', 84),
('Soybeans', 180, 'Legume', 85),
('Tofu', 7, 'Protein', 86),
('Tempeh', 7, 'Protein', 87),
('Seitan', 7, 'Protein', 88),
('Mushrooms', 7, 'Vegetable', 89),
('Soy Milk', 7, 'Dairy', 90),
('Almond Milk', 7, 'Dairy', 91),
('Coconut Milk', 7, 'Dairy', 92),
('Rice Milk', 7, 'Dairy', 93),
('Butter', 30, 'Dairy', 94),
('Olive Oil', 180, 'Oil', 95),
('Coconut Oil', 180, 'Oil', 96),
('Vegetable Oil', 180, 'Oil', 97),
('Canola Oil', 180, 'Oil', 98),
('Avocado Oil', 180, 'Oil', 99),
('Sunflower Oil', 180, 'Oil', 100);

-- Insert recipes for common foods without user_id
INSERT INTO `GroceryApp`.`Recipes` (`recipe_name`, `recipe_url`)
VALUES
('Apple Pie', 'https://www.allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/'),
('Banana Bread', 'https://www.allrecipes.com/recipe/20144/banana-banana-bread/'),
('Carrot Cake', 'https://www.allrecipes.com/recipe/17481/carrot-cake-iii/'),
('Chicken Alfredo', 'https://www.allrecipes.com/recipe/20119/chicken-alfredo/'),
('Spinach Salad', 'https://www.allrecipes.com/recipe/14103/spinach-salad/'),
('Tomato Soup', 'https://www.allrecipes.com/recipe/16408/old-fashioned-tomato-soup/'),
('Potato Salad', 'https://www.allrecipes.com/recipe/20144/potato-salad/'),
('Onion Rings', 'https://www.allrecipes.com/recipe/22291/beer-battered-fried-onion-rings/'),
('Garlic Bread', 'https://www.allrecipes.com/recipe/21060/garlic-bread/'),
('Lettuce Wraps', 'https://www.allrecipes.com/recipe/229156/lettuce-wraps/'),
('Egg Salad', 'https://www.allrecipes.com/recipe/220751/egg-salad/'),
('Cheese Omelet', 'https://www.allrecipes.com/recipe/16311/cheese-omelet/'),
('Milkshake', 'https://www.allrecipes.com/recipe/23404/milkshake/'),
('Yogurt Parfait', 'https://www.allrecipes.com/recipe/229156/lettuce-wraps/'),
('Grilled Cheese', 'https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/'),
('Fried Rice', 'https://www.allrecipes.com/recipe/229960/fried-rice/'),
('Spaghetti', 'https://www.allrecipes.com/recipe/158140/spaghetti/'),
('Beef Stew', 'https://www.allrecipes.com/recipe/14685/beef-stew/'),
('Pork Chops', 'https://www.allrecipes.com/recipe/16271/pork-chops/'),
('Salmon Fillet', 'https://www.allrecipes.com/recipe/147312/salmon-fillets/'),
('Tuna Salad', 'https://www.allrecipes.com/recipe/220751/tuna-salad/'),
('Cucumber Salad', 'https://www.allrecipes.com/recipe/14103/spinach-salad/'),
('Bell Pepper Stir-Fry', 'https://www.allrecipes.com/recipe/16468/bell-pepper-stir-fry/'),
('Zucchini Noodles', 'https://www.allrecipes.com/recipe/229960/zucchini-noodles/'),
('Sweet Potato Fries', 'https://www.allrecipes.com/recipe/223042/sweet-potato-fries/'),
('Avocado Toast', 'https://www.allrecipes.com/recipe/229960/avocado-toast/'),
('Strawberry Shortcake', 'https://www.allrecipes.com/recipe/17481/strawberry-shortcake/'),
('Blueberry Muffins', 'https://www.allrecipes.com/recipe/20144/blueberry-muffins/'),
('Peach Cobbler', 'https://www.allrecipes.com/recipe/20144/peach-cobbler/'),
('Grapes Salad', 'https://www.allrecipes.com/recipe/14103/grape-salad/'),
('Pineapple Upside-Down Cake', 'https://www.allrecipes.com/recipe/12682/pineapple-upside-down-cake/'),
('Mango Salsa', 'https://www.allrecipes.com/recipe/229960/mango-salsa/'),
('Papaya Salad', 'https://www.allrecipes.com/recipe/229960/papaya-salad/'),
('Melon Salad', 'https://www.allrecipes.com/recipe/14103/melon-salad/'),
('Lemon Bars', 'https://www.allrecipes.com/recipe/12682/lemon-bars/'),
('Orange Chicken', 'https://www.allrecipes.com/recipe/229960/orange-chicken/'),
('Coconut Shrimp', 'https://www.allrecipes.com/recipe/147312/coconut-shrimp/'),
('Kiwi Sorbet', 'https://www.allrecipes.com/recipe/229960/kiwi-sorbet/'),
('Plum Sauce', 'https://www.allrecipes.com/recipe/229960/plum-sauce/'),
('Cherries Jubilee', 'https://www.allrecipes.com/recipe/17481/cherries-jubilee/'),
('Raspberry Jam', 'https://www.allrecipes.com/recipe/14103/raspberry-jam/'),
('Blackberry Cobbler', 'https://www.allrecipes.com/recipe/12682/blackberry-cobbler/'),
('Gingerbread Cookies', 'https://www.allrecipes.com/recipe/17481/gingerbread-cookies/'),
('Cinnamon Rolls', 'https://www.allrecipes.com/recipe/9704/cinnamon-rolls/'),
('Turmeric Rice', 'https://www.allrecipes.com/recipe/229960/turmeric-rice/'),
('Nutmeg Cake', 'https://www.allrecipes.com/recipe/12682/nutmeg-cake/'),
('Chili Powder Chicken', 'https://www.allrecipes.com/recipe/229960/chili-powder-chicken/'),
('Cumin Lamb', 'https://www.allrecipes.com/recipe/229960/cumin-lamb/'),
('Paprika Potatoes', 'https://www.allrecipes.com/recipe/229960/paprika-potatoes/'),
('Oregano Chicken', 'https://www.allrecipes.com/recipe/229960/oregano-chicken/'),
('Basil Pesto', 'https://www.allrecipes.com/recipe/229960/basil-pesto/'),
('Thyme Roasted Chicken', 'https://www.allrecipes.com/recipe/229960/thyme-roasted-chicken/'),
('Rosemary Lamb', 'https://www.allrecipes.com/recipe/229960/rosemary-lamb/'),
('Parsley Potatoes', 'https://www.allrecipes.com/recipe/13351/parsley-potatoes/'),
('Sage Stuffing', 'https://www.allrecipes.com/recipe/229960/sage-stuffing/'),
('Dill Pickles', 'https://www.allrecipes.com/recipe/14349/dill-pickles/'),
('Bay Leaves Soup', 'https://www.allrecipes.com/recipe/24713/bay-leaves-soup/'),
('Mint Tea', 'https://www.allrecipes.com/recipe/229960/mint-tea/'),
('Chives Butter', 'https://www.allrecipes.com/recipe/229960/chives-butter/'),
('Coriander Chutney', 'https://www.allrecipes.com/recipe/229960/coriander-chutney/'),
('Fennel Salad', 'https://www.allrecipes.com/recipe/229960/fennel-salad/'),
('Almond Milkshake', 'https://www.allrecipes.com/recipe/229960/almond-milkshake/'),
('Walnut Brownies', 'https://www.allrecipes.com/recipe/229960/walnut-brownies/'),
('Pistachio Ice Cream', 'https://www.allrecipes.com/recipe/19209/pistachio-ice-cream/'),
('Cashew Butter', 'https://www.allrecipes.com/recipe/229960/cashew-butter/'),
('Peanut Butter', 'https://www.allrecipes.com/recipe/229960/peanut-butter/'),
('Hazelnut Cake', 'https://www.allrecipes.com/recipe/229960/hazelnut-cake/'),
('Chia Pudding', 'https://www.allrecipes.com/recipe/229960/chia-pudding/'),
('Flax Seed Smoothie', 'https://www.allrecipes.com/recipe/229960/flax-seed-smoothie/'),
('Pumpkin Seed Butter', 'https://www.allrecipes.com/recipe/229960/pumpkin-seed-butter/'),
('Sunflower Seed Granola', 'https://www.allrecipes.com/recipe/229960/sunflower-seed-granola/'),
('Sesame Seed Snack', 'https://www.allrecipes.com/recipe/229960/sesame-seed-snack/'),
('Quinoa Salad', 'https://www.allrecipes.com/recipe/229960/quinoa-salad/'),
('Barley Soup', 'https://www.allrecipes.com/recipe/16017/barley-soup/'),
('Buckwheat Pancakes', 'https://www.allrecipes.com/recipe/22883/buckwheat-pancakes/'),
('Millet Porridge', 'https://www.allrecipes.com/recipe/26788/millet-porridge/'),
('Farro Salad', 'https://www.allrecipes.com/recipe/245688/farro-salad/'),
('Oats Porridge', 'https://www.allrecipes.com/recipe/23447/oats-porridge/'),
('Chickpea Curry', 'https://www.allrecipes.com/recipe/26106/chickpea-curry/'),
('Lentil Soup', 'https://www.allrecipes.com/recipe/158140/lentil-soup/'),
('Black Bean Tacos', 'https://www.allrecipes.com/recipe/229960/black-bean-tacos/'),
('Kidney Bean Chili', 'https://www.allrecipes.com/recipe/229960/kidney-bean-chili/'),
('Pea Soup', 'https://www.allrecipes.com/recipe/15459/pea-soup/'),
('Edamame Salad', 'https://www.allrecipes.com/recipe/229960/edamame-salad/'),
('Soybean Stir Fry', 'https://www.allrecipes.com/recipe/229960/soybean-stir-fry/'),
('Tofu Stir Fry', 'https://www.allrecipes.com/recipe/229960/tofu-stir-fry/'),
('Tempeh Tacos', 'https://www.allrecipes.com/recipe/229960/tempeh-tacos/'),
('Seitan Roast', 'https://www.allrecipes.com/recipe/229960/seitan-roast/'),
('Mushroom Risotto', 'https://www.allrecipes.com/recipe/229960/mushroom-risotto/'),
('Soy Milk Latte', 'https://www.allrecipes.com/recipe/229960/soy-milk-latte/'),
('Almond Milk Latte', 'https://www.allrecipes.com/recipe/229960/almond-milk-latte/'),
('Coconut Milk Smoothie', 'https://www.allrecipes.com/recipe/229960/coconut-milk-smoothie/'),
('Rice Milk Pudding', 'https://www.allrecipes.com/recipe/229960/rice-milk-pudding/'),
('Butter Chicken', 'https://www.allrecipes.com/recipe/22518/butter-chicken/'),
('Olive Oil Dressing', 'https://www.allrecipes.com/recipe/13455/olive-oil-dressing/'),
('Coconut Oil Cake', 'https://www.allrecipes.com/recipe/240269/coconut-oil-cake/'),
('Vegetable Oil Fries', 'https://www.allrecipes.com/recipe/24835/vegetable-oil-fries/'),
('Canola Oil Bread', 'https://www.allrecipes.com/recipe/23447/canola-oil-bread/'),
('Avocado Oil Salad', 'https://www.allrecipes.com/recipe/26946/avocado-oil-salad/'),
('Sunflower Oil Cake', 'https://www.allrecipes.com/recipe/229960/sunflower-oil-cake/')

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
