
| Time            | Sprint       | Goal / User Story                                                                                  | Tasks                                                                                                                                                                                                  | Definition of Done                                       |
| --------------- | ------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| **8:00–8:30**   | **Sprint 0** | 🚀 **Kickoff & Setup**  As a team, we need a working repo & infra so we can code immediately.      | - Create GitHub repo & branches<br/>- Bootstrap Next.js + FastAPI projects<br/>- Configure Auth0/Firebase stub<br/>- Deploy skeleton to Vercel/AWS                                                     | Repo initialized, CI passes a “hello world” build        |
| **8:30–10:00**  | **Sprint 1** | 🔐 **User Onboarding & Profile**  As a user, I can sign up, set my dietary prefs & budget.         | - Implement signup/login endpoints (FastAPI)<br/>- Build React onboarding form (questions + prefs)<br/>- Persist to Postgres<br/>- Basic form validation                                               | User can create account and see “Profile saved” toast    |
| **10:00–10:15** | **Break**    | —                                                                                                  | Stretch, caffeine                                                                                                                                                                                      | —                                                        |
| **10:15–12:15** | **Sprint 2** | 📅 **AI Meal Plan MVP**  As a user, I can generate a 7-day meal plan.                              | - Wire up AI Engine endpoint (call placeholder LLM with sample prompt)<br/>- Define MealPlan & MealPlanEntry models + migrations<br/>- Hook React “Generate Plan” button to fetch + render a list view | Clicking “Generate” shows 7-day list of dummy recipes    |
| **12:15–1:00**  | **Lunch**    | —                                                                                                  | Fuel up!                                                                                                                                                                                               | —                                                        |
| **1:00–2:30**   | **Sprint 3** | 📷 **Fridge Scan Stub**  As a user, I can upload a fridge photo and see detected items.            | - Add React PhotoUpload component<br/>- Build FastAPI `/scan` endpoint that returns hard-coded JSON of ingredients<br/>- Display detection UI with confirm buttons                                     | Photo uploads → list of “Milk, Eggs, Spinach” appears    |
| **2:30–4:00**   | **Sprint 4** | 🛒 **Shopping List & Inventory Sync**  As a user, I can see a shopping list adjusted by my pantry. | - Merge detected items into PantryItem table on confirmation<br/>- Compute ShoppingList from MealPlan minus pantry quantities<br/>- Show consolidated list in React                                    | Shopping list shows only “new” items, quantities correct |
| **4:00–4:15**   | **Break**    | —                                                                                                  | Quick stand-up, fix blocker                                                                                                                                                                            | —                                                        |
| **4:15–5:15**   | **Sprint 5** | ✅ **Polish & Testing**  As a team, we need basic tests & a stable UI for demo.                     | - Write 2–3 unit tests (Auth, Plan gen stub)<br/>- Add loading & error states in UI<br/>- Quick end-to-end manual test flow                                                                            | No console errors; flows complete without crashes        |
| **5:15–5:45**   | **Sprint 6** | 🎤 **Demo Prep**  As a team, we need to showcase our 1-day build to judges.                        | - Record script/screenshots<br/>- Deploy final build<br/>- Prepare 5-slide deck (problem, solution, live demo, architecture, next steps)                                                               | Demo environment live & slide deck ready                 |
| **5:45–6:00**   | **Sprint 7** | 🏁 **Wrap-Up**  Last-minute bugfixes & commit.                                                     | - Triage any critical bugs found during rehearsal<br/>- Push final commits, tag release                                                                                                                | Master branch green, tagged `v0.1-hackathon`             |

### Roles & Responsibilities (2–3 people)

* **Frontend Engineer**: Onboarding UI, plan & list rendering, photo upload/confirm.
* **Backend Engineer**: FastAPI services—auth, AI stub, scan stub, plan & shopping logic.
* **Full-Stack / QA**: Tie it together, write tests, handle infra & demo slides.

---

**Tips for Success**

* **Keep stubs**: Use hard-coded AI and CV responses early; swap in real models if time permits.
* **Vertical slices**: Always push something demo-able end-to-end in each sprint.
* **Automate early**: A quick CI pipeline prevents late-stage deployment hiccups.
* **Demo script**: Practice the user flow (“upload photo → generate plan → view list”) to hit key points in under 2 minutes.

