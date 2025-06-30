## Epic 1: Project Setup & Infrastructure

**Goal:** Lay the groundwork so the team can code, test, and demo without friction.

* **US1.1** — *Initialize repository and CI*

  * **As a** developer
  * **I want** a GitHub repo with a working CI pipeline
  * **So that** every push runs a basic “hello world” build
  * **Acceptance:** Repo created, `npm run build` and `pytest` succeed on CI

* **US1.2** — *Bootstrap frontend & backend skeletons*

  * **As a** developer
  * **I want** a Next.js app and FastAPI app scaffold
  * **So that** we can immediately add features
  * **Acceptance:** Visiting `/` on both yields “Hello, world”

* **US1.3** — *Stub authentication provider*

  * **As a** developer
  * **I want** Auth0/Firebase stub integrated
  * **So that** we can secure routes without full implementation
  * **Acceptance:** Protected endpoint returns 401 when not “logged in”

---

## Epic 2: User Onboarding & Profile Management

**Goal:** Enable users to sign up and set dietary preferences.

* **US2.1** — *User Signup & Login*

  * **As a** new visitor
  * **I want** to create an account (email/password or OAuth)
  * **So that** I can save my settings
  * **Acceptance:** Can register and see a “Welcome” page

* **US2.2** — *Onboarding Questionnaire*

  * **As a** first-time user
  * **I want** a form asking my age, weight, height, activity level, goals, dietary restrictions, budget, and cuisines
  * **So that** the system knows my preferences
  * **Acceptance:** Submitting the form persists a User record with a JSONB `dietary_preferences` and `weekly_budget_cents`

* **US2.3** — *Profile Persistence & Retrieval*

  * **As a** returning user
  * **I want** to load and edit my profile anytime
  * **So that** I can update my preferences
  * **Acceptance:** Profile API returns and updates user fields

---

## Epic 3: Core AI Meal Plan Generation

**Goal:** Generate a 7-day meal plan tailored to the user.

* **US3.1** — *Define MealPlan & Entry Models*

  * **As a** backend developer
  * **I want** `MealPlan` and `MealPlanEntry` tables
  * **So that** I can store plans and their meals
  * **Acceptance:** Database migrations in place, models accessible

* **US3.2** — *Stub AI-Engine Endpoint*

  * **As a** backend developer
  * **I want** `/api/plan/generate` to return dummy 7-day data
  * **So that** frontend can render a plan immediately
  * **Acceptance:** GET returns JSON array of 7 dates × 4 meal slots

* **US3.3** — *Frontend “Generate Plan” Flow*

  * **As a** user
  * **I want** a button that calls the stub and displays the plan
  * **So that** I see a weekly menu in the UI
  * **Acceptance:** Click → spinner → list of 28 recipe titles

---

## Epic 4: Fridge/Pantry Photo-Scan

**Goal:** Let users upload a photo to capture on-hand ingredients.

* **US4.1** — *Photo Upload UI*

  * **As a** user
  * **I want** to snap or upload an image of my fridge/pantry
  * **So that** the system can detect ingredients
  * **Acceptance:** Upload control accepts image and shows preview

* **US4.2** — *Scan Endpoint Stub*

  * **As a** backend developer
  * **I want** `/api/scan` to return hard-coded ingredients (“Milk, Eggs, Spinach”)
  * **So that** the UI can show detection results
  * **Acceptance:** POST image → JSON payload of detected items

* **US4.3** — *Detection Confirmation UI*

  * **As a** user
  * **I want** to review, adjust, and confirm detected items
  * **So that** only correct items enter my inventory
  * **Acceptance:** List displays each item with quantity input and “Confirm” button

---

## Epic 5: Inventory Sync & Shopping List Generation

**Goal:** Merge confirmed items into pantry and adjust shopping list.

* **US5.1** — *PantryItem Upsert*

  * **As a** backend developer
  * **I want** to insert/update `PantryItem` rows from confirmed scans
  * **So that** we track on-hand quantities
  * **Acceptance:** Confirmed items appear in `PantryItem` with `added_via_scan=true`

* **US5.2** — *Compute ShoppingList*

  * **As a** backend developer
  * **I want** to subtract pantry quantities from meal ingredients to build a shopping list
  * **So that** users only buy what they need
  * **Acceptance:** ShoppingList table populated with new items and correct quantities

* **US5.3** — *Shopping List UI*

  * **As a** user
  * **I want** to view a consolidated list of ingredients I still need
  * **So that** I know what to buy
  * **Acceptance:** UI shows list with name, quantity, unit, and cost estimate

---

## Epic 6: Adaptive Plan Editing & Feedback

**Goal:** Allow one-click swaps and collect recipe ratings.

* **US6.1** — *Swap Meal Entry*

  * **As a** user
  * **I want** to click “Swap” on any meal and see a new suggestion
  * **So that** I can customize my plan
  * **Acceptance:** Entry replaced client-side and re-sent to AI stub for re-optimization

* **US6.2** — *Recipe Rating Capture*

  * **As a** user
  * **I want** to rate each meal 1–5 stars and leave a comment
  * **So that** the system can learn my tastes
  * **Acceptance:** Rating stored in `RecipeRating`; average rating viewable in dashboard

---

## Epic 7: Testing, Polish & Demo Preparation

**Goal:** Ensure stability, showcase smoothly, and deploy for judges.

* **US7.1** — *Basic Unit Tests*

  * **As a** QA engineer
  * **I want** tests for auth flows and plan-generation stub
  * **So that** core functionality is verified
  * **Acceptance:** `pytest` and `jest` pass all tests

* **US7.2** — *UI Loading & Error States*

  * **As a** user
  * **I want** spinners and friendly error messages
  * **So that** the app feels polished
  * **Acceptance:** Slow network sim shows loader; API failures show “Try again”

* **US7.3** — *Demo Slide Deck*

  * **As a** presenter
  * **I want** a 5-slide deck (Problem, Solution, Architecture, Live Demo, Next Steps)
  * **So that** I can confidently pitch to judges
  * **Acceptance:** Slides prepared and linked in the repo README

---

This backlog breaks the one-day build into clear Epics and bite-sized User Stories you can assign, plan, and track in your sprint tool of choice (Jira, Trello, GitHub Issues, etc.). Each story ties back to a slice of the vertical end-to-end flow, ensuring you ship a demo-ready MVP by day’s end.
