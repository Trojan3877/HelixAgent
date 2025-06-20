## 📑 Summary
<!-- Short explanation of WHAT you are changing and WHY. -->

Fixes #<!-- issue ID here, e.g. 42 -->

---

### ✅ PR Checklist
- [ ] Title follows **Conventional Commits** (`feat:`, `fix:`, `docs:` …)
- [ ] Code compiles locally (`make test` passes)
- [ ] Added/updated unit tests
- [ ] Updated documentation (`README`, `docs/api_reference.md`, or inline comments)
- [ ] Added/updated CHANGELOG entry
- [ ] Checked for security implications (secrets, PII, OWASP)
- [ ] If introducing new env vars, updated Helm `values.yaml` + Terraform

---

### 🔬 Testing Steps
<!-- Explicit commands or curl calls reviewers can run. -->

```bash
# Example
uvicorn app.api:app --reload
curl -X POST http://localhost:8000/predict -d '{"demo":1}'
