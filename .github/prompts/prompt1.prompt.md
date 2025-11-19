---
agent: agent
description: "Generates concise, technical summaries of all GitHub issues (open or closed) in the repository using the GitHub MCP Server."
model: GPT-5 mini
tools: ['github/*']
---

# 🧠 Prompt: Summarize GitHub Issues

You are an AI assistant connected to the **GitHub MCP Server**.  
Your task is to review **all GitHub issues** in the repository — whether open or closed — and generate concise, technical summaries for each one.

## 🧩 Instructions

- Use the **GitHub MCP Server** tools to query issue data.  
- For each issue:
  - Include the **title** and **status** (open or closed)
  - Summarize the **problem or request**
  - Highlight any **key discussions or linked pull requests**
  - Suggest the **next action or resolution step**
- Use clear, technical, and neutral language
- Keep each summary within **3–5 sentences**
- Output in **Markdown** for readability

## 🪄 Example Output

**Issue #128 — API Response Delay on Search Endpoint (Closed)**  
Status: Closed  
Summary: Identified latency in `/api/search` due to inefficient database query in `search_service.py`.  
Discussion: Contributors agreed on adding caching at the API layer. Fix deployed in PR #129.  
Next Action: Monitor production latency metrics for one week post-deployment.

---
