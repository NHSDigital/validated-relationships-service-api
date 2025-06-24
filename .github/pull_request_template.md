# Pull Request Template

## 🧾 Ticket Link

<!-- Add the Jira ticket link here -->

https://nhsd-jira.digital.nhs.uk/browse/NPA-XXXX

---

## 📝 PR Title Format

Must follow format: `NPA-XXXX: Short Description of the Change`

---

## 📄 Description/Summary of Changes

<!-- Describe the changes made in this PR. Include the purpose/scope/impact of the changes -->

- <!-- Add bullet points summarising key changes -->
- <!-- Add bullet points summarising key changes -->
- <!-- Add bullet points summarising key changes -->

---

## 🧪 How to Test

<!-- Describe how to test the changes. Include: -->
<!-- - Testing environment details (e.g. sandbox/local setup) -->
<!-- - Steps to verify the changes -->
<!-- - Any automated tests added or updated (with links to test cases if applicable) -->
<!-- - Evidence that each acceptance criterion from the Jira ticket is met -->

- <!-- Add bullet points for testing instructions -->
- <!-- Add bullet points for testing instructions -->
- <!-- Add bullet points for testing instructions -->

---

## ✅ Developer Checklist

<!-- Complete before submitting the PR -->

- [ ] PR title follows the format: `NPA-XXXX: <short-description>`
- [ ] Branch name follows the convention: `<type>/NPA-XXXX-<short-description>`
- [ ] Commit messages follow the template: `NPA-XXXX: <short-description>`
- [ ] All acceptance criteria from the Jira ticket are addressed
- [ ] Automated tests (unit/integration/API/infrastructure etc. tests) are added or updated
- [ ] The [traceability matrix](https://nhsd-confluence.digital.nhs.uk/display/NPA/Traceability+matrix) is updated with
      new tests or requirements
- [ ] Assignees and appropriate labels (e.g. `terraform`, `documentation`) are added

---

## 👀 Reviewer Checklist

<!-- To be completed by the reviewer -->

- [ ] Changes meet the acceptance criteria of the Jira ticket
- [ ] Code is able to be merged (no conflicts and adheres to coding standards)
- [ ] Sufficient test evidence is provided (manual and/or automated)
- [ ] Infrastructure/operational/build changes are validated (if applicable)

---

## 🚀 Post-merge

<!-- Actions to complete after merging -->
After merging and deploying changes to the sandbox, Postman collection or spec examples please run the Run Postman
collection workflow.

This will run the tests within the collection to check that the sandbox is working as expected once deployed.
