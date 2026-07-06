# ISTQB CTFL vocabulary — distilled

Source: ISTQB Certified Tester Foundation Level Syllabus v4.0.1
(https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf),
released 2024-09-15 as a copyright/logo-only update of v4.0; content
unchanged. Distilled for offline use — do not fetch the URL at runtime.

## Core terms

- **Error (mistake)** — a human action producing an incorrect result.
- **Defect (bug, fault)** — an imperfection in a work product (code or
  documents) caused by an error.
- **Failure** — an event where the system deviates from expected behavior,
  caused by a defect being executed (not every defect leads to failure).
- **Root cause** — the fundamental reason a defect was introduced; fix it
  to prevent recurrence.
- **Testing vs debugging** — testing finds failures/defects; debugging
  finds, analyzes, and removes their causes.
- **Verification vs validation** — verification: does the product meet
  specified requirements; validation: does it meet users' needs in
  context.
- **Static vs dynamic testing** — static: reviews and static analysis
  without executing the code (finds defects directly, early, cheaply);
  dynamic: executing the test object with test cases.

## The seven testing principles (syllabus 1.3)

1. Testing shows the presence of defects, not their absence.
2. Exhaustive testing is impossible — use prioritization and risk.
3. Early testing saves time and money ("shift left").
4. Defects cluster together — a few modules contain most defects; focus
   there (basis for risk-based prioritization).
5. Tests wear out (pesticide paradox) — repeated identical tests stop
   finding new defects; revise and add tests. (Exception: regression
   suites, where repetition is the point.)
6. Testing is context dependent — there is no single universal approach.
7. Absence-of-errors is a fallacy — verifying all requirements does not
   guarantee a successful product if the requirements miss user needs.

## Test levels (syllabus 2.2.1)

Each level has its own test objects, test basis, typical defects, and
responsible parties. Independence of testing (someone other than the
author) increases defect-finding effectiveness at higher levels.

1. **Component testing (unit testing)** — tests components in isolation;
   usually done by developers, in the development environment, often
   tool-supported (unit frameworks).
2. **Component integration testing** — interfaces and interactions
   between components; driven by the integration strategy (bottom-up,
   top-down, big-bang).
3. **System testing** — end-to-end behavior of the whole system:
   functional and non-functional; often done by an independent test team
   against specifications, in an environment mirroring production.
4. **System integration testing** — the system's interfaces to other
   systems and external services (third parties, networks, org systems).
5. **Acceptance testing** — validation and release-readiness; typically
   users/business-led. Forms: **user acceptance testing (UAT)**,
   **operational acceptance testing** (backup/restore, monitoring,
   maintenance), **contractual and regulatory acceptance testing**,
   **alpha testing** (at developer site) and **beta testing** (at user
   site).

In iterative SDLCs, all levels can occur within each iteration; in
sequential SDLCs they map to phases. Say which model applies.

## Test types (syllabus 2.2.2)

- **Functional testing** — WHAT the system does: completeness,
  correctness, appropriateness of functional behavior.
- **Non-functional testing** — HOW WELL the system behaves. Characteristics
  per ISO/IEC 25010 (as referenced by the syllabus): performance
  efficiency, compatibility, usability (interaction capability),
  reliability, security, maintainability, portability (flexibility),
  safety. Non-functional testing can and should start early.
- **Black-box testing** — specification-based; derives tests from
  documented requirements/behavior without reference to internal
  structure; measures coverage of specified items.
- **White-box testing** — structure-based; derives tests from the code or
  architecture; measures structural coverage (e.g. statement, branch).
- **Confirmation testing (retesting)** — re-run tests that failed, after
  the defect fix, to confirm the fix.
- **Regression testing** — re-run tests on unchanged areas to detect
  side effects of changes; prime candidate for automation.

All test types can be applied at every test level.

## Test plan contents (syllabus 5.1)

A test plan documents the means and schedule for achieving test
objectives. Typical content:

- Context of testing: scope, objectives, constraints, test basis.
- Assumptions and constraints.
- Stakeholders: roles, responsibilities, relevance to testing, hiring and
  training needs.
- Communication: forms and frequency, documentation templates.
- Risk register: product risks and project risks.
- Test approach: test levels, test types, techniques, deliverables,
  entry/exit criteria, independence of testing, metrics, test data
  requirements, environment requirements, deviations from org test policy.
- Budget and schedule.

## Entry and exit criteria (syllabus 5.1.3)

- **Entry criteria (definition of ready)** — preconditions for starting a
  test activity: resources available (people, tools, environments, data,
  budget, time), testware available (test basis, testable requirements,
  test cases), initial quality level (e.g. smoke test passed).
- **Exit criteria (definition of done)** — measurable conditions for
  declaring an activity complete: coverage achieved (requirements, code,
  risks), thresholds on unresolved defects (count/severity), estimated
  residual risk sufficiently low. Running out of time or budget can also
  end testing — then the residual risk must be reported to and accepted by
  stakeholders.

## Independence of testing (syllabus 5.1, 1.5)

Degrees: author tests own code (least independent) → peers on the same
team → independent test team → external testers (most independent).
Independence finds more failures (fewer author blind spots) but risks
losing developer collaboration and feedback speed; mix levels sensibly.
