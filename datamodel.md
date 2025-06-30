## Entities & Attributes

### 1. **User**

Stores user profile, preferences, and settings.

| Column                | Type         | Notes                                           |
| --------------------- | ------------ | ----------------------------------------------- |
| user\_id (PK)         | UUID         |                                                 |
| email                 | VARCHAR(255) | Unique, indexed                                 |
| password\_hash        | VARCHAR(255) |                                                 |
| signup\_date          | TIMESTAMP    |                                                 |
| name                  | VARCHAR(100) |                                                 |
| date\_of\_birth       | DATE         |                                                 |
| height\_cm            | INT          |                                                 |
| weight\_kg            | DECIMAL(5,2) |                                                 |
| activity\_level       | VARCHAR(50)  | e.g. ‘sedentary’, ‘moderate’, etc.              |
| dietary\_preferences  | JSONB        | e.g. `{ "vegan": true, "allergies": ["nuts"] }` |
| weekly\_budget\_cents | INT          |                                                 |
| preferred\_cuisines   | TEXT\[]      |                                                 |

---

### 2. **Recipe**

Master catalog of recipes.

| Column                | Type         | Notes                                                    |
| --------------------- | ------------ | -------------------------------------------------------- |
| recipe\_id (PK)       | UUID         |                                                          |
| title                 | VARCHAR(255) |                                                          |
| description           | TEXT         |                                                          |
| instructions          | TEXT         |                                                          |
| prep\_time\_minutes   | INT          |                                                          |
| cook\_time\_minutes   | INT          |                                                          |
| serving\_size         | INT          | Number of servings                                       |
| nutrition             | JSONB        | `{ calories, protein_g, fat_g, carbs_g, micros: {...} }` |
| cuisine\_type         | VARCHAR(50)  |                                                          |
| cost\_estimate\_cents | INT          |                                                          |
| image\_url            | TEXT         |                                                          |

---

### 3. **Ingredient**

Library of ingredients.

| Column               | Type         | Notes                         |
| -------------------- | ------------ | ----------------------------- |
| ingredient\_id (PK)  | UUID         |                               |
| name                 | VARCHAR(100) |                               |
| default\_unit        | VARCHAR(20)  | e.g. “g”, “cup”, “tbsp”       |
| nutrition\_per\_unit | JSONB        | Macro/micro per default\_unit |

---

### 4. **RecipeIngredient**

Joins recipes to ingredients with quantities.

| Column              | Type                         | Notes                                        |
| ------------------- | ---------------------------- | -------------------------------------------- |
| recipe\_id (FK)     | UUID                         | References Recipe                            |
| ingredient\_id (FK) | UUID                         | References Ingredient                        |
| quantity            | DECIMAL(8,2)                 |                                              |
| unit                | VARCHAR(20)                  | Overrides Ingredient.default\_unit if needed |
| PRIMARY KEY         | (recipe\_id, ingredient\_id) |                                              |

---

### 5. **PantryItem**

User’s stored inventory (manual + auto from scans).

| Column                | Type         | Notes                          |
| --------------------- | ------------ | ------------------------------ |
| pantry\_item\_id (PK) | UUID         |                                |
| user\_id (FK)         | UUID         | References User                |
| ingredient\_id (FK)   | UUID         | References Ingredient          |
| quantity              | DECIMAL(8,2) |                                |
| unit                  | VARCHAR(20)  |                                |
| added\_via\_scan      | BOOLEAN      | True if from fridge photo scan |
| last\_updated         | TIMESTAMP    |                                |

---

### 6. **PhotoScan**

Stores metadata & results of a fridge/pantry photo.

| Column          | Type      | Notes                                                       |
| --------------- | --------- | ----------------------------------------------------------- |
| scan\_id (PK)   | UUID      |                                                             |
| user\_id (FK)   | UUID      |                                                             |
| photo\_url      | TEXT      | S3 location                                                 |
| scan\_timestamp | TIMESTAMP |                                                             |
| detected\_items | JSONB     | `[{"ingredient_id": ..., "quantity": ..., "unit": ...}, …]` |
| user\_confirmed | BOOLEAN   | Has user reviewed the detections?                           |

---

### 7. **MealPlan**

A generated weekly meal plan instance.

| Column                | Type      | Notes                                 |
| --------------------- | --------- | ------------------------------------- |
| plan\_id (PK)         | UUID      |                                       |
| user\_id (FK)         | UUID      |                                       |
| generated\_at         | TIMESTAMP |                                       |
| start\_date           | DATE      | First day of the 7-day plan           |
| end\_date             | DATE      | start\_date + 6 days                  |
| preferences\_snapshot | JSONB     | Copy of user prefs at generation time |

---

### 8. **MealPlanEntry**

Individual meal slots within a plan.

| Column          | Type        | Notes                                        |
| --------------- | ----------- | -------------------------------------------- |
| entry\_id (PK)  | UUID        |                                              |
| plan\_id (FK)   | UUID        | References MealPlan                          |
| date            | DATE        |                                              |
| meal\_type      | VARCHAR(20) | e.g. ‘breakfast’, ‘lunch’, ‘dinner’, ‘snack’ |
| recipe\_id (FK) | UUID        | References Recipe                            |
| is\_swapped     | BOOLEAN     | True if user manually swapped it             |

---

### 9. **ShoppingList**

Generated shopping list per plan.

| Column        | Type      | Notes |
| ------------- | --------- | ----- |
| list\_id (PK) | UUID      |       |
| plan\_id (FK) | UUID      |       |
| created\_at   | TIMESTAMP |       |

---

### 10. **ShoppingListItem**

Line items in a shopping list.

| Column                | Type         | Notes                   |
| --------------------- | ------------ | ----------------------- |
| list\_item\_id (PK)   | UUID         |                         |
| list\_id (FK)         | UUID         | References ShoppingList |
| ingredient\_id (FK)   | UUID         |                         |
| quantity              | DECIMAL(8,2) |                         |
| unit                  | VARCHAR(20)  |                         |
| cost\_estimate\_cents | INT          |                         |

---

### 11. **RecipeRating**

User feedback on recipes.

| Column               | Type      | Notes                               |
| -------------------- | --------- | ----------------------------------- |
| rating\_id (PK)      | UUID      |                                     |
| user\_id (FK)        | UUID      |                                     |
| recipe\_id (FK)      | UUID      |                                     |
| plan\_entry\_id (FK) | UUID      | References MealPlanEntry (nullable) |
| rating               | SMALLINT  | 1–5                                 |
| comment              | TEXT      | Optional                            |
| rated\_at            | TIMESTAMP |                                     |

---

## Relationships & Notes

* **1–M**: User → MealPlan, PhotoScan, PantryItem, RecipeRating.
* **1–M**: MealPlan → MealPlanEntry → Recipe.
* **1–1** or **1–M**: MealPlan → ShoppingList → ShoppingListItem.
* **M–N** via RecipeIngredient: Recipe ↔ Ingredient.
* **Inventory Sync**: On PhotoScan confirmation, upsert into PantryItem.
* **Plan Generation**: AI Engine reads User, PantryItem, Recipe & Nutrition to populate MealPlan and related entries & shopping list.

---
