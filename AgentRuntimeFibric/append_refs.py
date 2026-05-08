import os

refs = """
## 11. 引用的文献

1. Google and AWS split the AI agent stack between control and execution | VentureBeat, https://venturebeat.com/orchestration/google-and-aws-split-the-ai-agent-stack-between-control-and-execution
2. Agents SDK | OpenAI API, https://developers.openai.com/api/docs/guides/agents
3. The next evolution of the Agents SDK - OpenAI, https://openai.com/index/the-next-evolution-of-the-agents-sdk/
4. Scaling Managed Agents: Decoupling the brain from the ... - Anthropic, https://www.anthropic.com/engineering/managed-agents
5. Introducing Gemini Enterprise Agent Platform | Google Cloud Blog, https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform
6. Overview - Amazon Bedrock AgentCore - AWS Documentation, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
7. Configuring Amazon Bedrock AgentCore Gateway for secure access to private resources, https://aws.amazon.com/blogs/machine-learning/configuring-amazon-bedrock-agentcore-gateway-for-secure-access-to-private-resources/
8. Amazon Bedrock AgentCore is now available in AWS GovCloud (US-West), https://aws.amazon.com/about-aws/whats-new/2026/05/bedrock-agentcore-launch-aws-govcloud-us/
9. Kimi K2.5 Tech Blog: Visual Agentic Intelligence, https://www.kimi.com/blog/kimi-k2-5
10. moonshotai/Kimi-K2.5 - Hugging Face, https://huggingface.co/moonshotai/Kimi-K2.5
11. Agent Skills – Codex | OpenAI Developers, https://developers.openai.com/codex/skills
12. Using skills to accelerate OSS maintenance - OpenAI Developers, https://developers.openai.com/blog/skills-agents-sdk
13. Agent-to-Agent Protocol (A2A) vs What is Model Context Protocol (MCP) Which AI Protocol Do You Need?, https://medium.com/@tahirbalarabe2/agent-to-agent-protocol-a2a-vs-what-is-model-context-protocol-mcp-which-ai-protocol-do-you-need-aff602a4571c
14. Securely connect tools and other resources to your Gateway - Amazon Bedrock AgentCore, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
15. Secure AI agents with Amazon Bedrock AgentCore Identity on Amazon ECS | Artificial Intelligence, https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-amazon-bedrock-agentcore-identity-on-amazon-ecs/
16. Kimi K2.5: Still Worth It After Two Weeks?, https://medium.com/@mlabonne/kimi-k2-5-still-worth-it-after-two-weeks-f32abd991e26
17. Agentic AI Comparison: Codex CLI vs OpenAI Codex SDK - AI Agent Store, https://aiagentstore.ai/compare-ai-agents/codex-cli-vs-openai-codex-sdk
18. Codex SDK - OpenAI Developers, https://developers.openai.com/codex/sdk
19. Claude Managed Agents overview - Claude API Docs, https://platform.claude.com/docs/en/managed-agents/overview
20. I Tested Claude's New Managed Agents... What You Need To Know, https://www.youtube.com/watch?v=27Y44JYXZJ8&vl=en
21. Build an agent with ADK and Agents CLI in Agent Platform - Google Cloud Documentation, https://docs.cloud.google.com/gemini-enterprise-agent-platform/agents/quickstart-adk
22. Build an AI Agent with Gemini CLI and Agent Development Kit | by Debi Cabrera - Googler | Google Cloud - Community | Medium, https://medium.com/google-cloud/build-an-ai-agent-with-gemini-cli-and-agent-development-kit-bca4b87c9a35
23. Amazon Bedrock AgentCore Construct Library - AWS Documentation, https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_bedrock_agentcore_alpha/README.html
24. Get started with the AgentCore CLI in TypeScript - AWS Documentation, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli-typescript.html
25. Managed Inference and Agents API with Kimi K2.5 | Heroku Dev Center, https://devcenter.heroku.com/articles/heroku-inference-api-model-kimi-k2-5
26. Kimi API Platform, https://platform.moonshot.ai/
27. Kimi K2.5 quickstart - Together AI Docs, https://docs.together.ai/docs/kimi-k2-5-quickstart
28. A practical guide to building agents | OpenAI, https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
29. 7 Multi-Agent Orchestration Platforms: Build vs Buy in 2026 | Augment Code, https://www.augmentcode.com/tools/multi-agent-orchestration-platforms-build-vs-buy
30. AI Agent Protocols Explained: What Are A2A and MCP and Why They Matter - Knowi, https://www.knowi.com/blog/ai-agent-protocols-explained-what-are-a2a-and-mcp-and-why-they-matter/
31. How OpenAI uses Codex, https://openai.com/business/guides-and-resources/how-openai-uses-codex/
32. Amazon Bedrock AgentCore Documentation, https://docs.aws.amazon.com/bedrock-agentcore/
33. Execute code and analyze data using Amazon Bedrock AgentCore Code Interpreter, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/code-interpreter-tool.html
34. Kimi K2.5: Complete Guide to Moonshot's AI Model - Codecademy, https://www.codecademy.com/article/kimi-k-2-5-complete-guide-to-moonshots-ai-model
35. AI Agents vs Humans: Who Wins at Web Hacking in 2026? | Wiz Blog, https://www.wiz.io/blog/ai-agents-vs-humans-who-wins-at-web-hacking-in-2026
36. I compared sandbox options for AI agents. Here's my ranking. : r/AI_Agents - Reddit, https://www.reddit.com/r/AI_Agents/comments/1sh2x4p/i_compared_sandbox_options_for_ai_agents_heres_my_ranking/
37. Amazon Bedrock AgentCore - Developer Guide, https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-dg.pdf
38. Amazon Bedrock AgentCore - AWS, https://aws.amazon.com/bedrock/agentcore/
39. Build Enterprise AI SaaS on GCP | Gemini Enterprise Architecture Explained, https://www.youtube.com/watch?v=0Y90k3---Bs
40. Building AI Agents with OpenAI SDK | by Sweety Tripathi | Data Science Collective | Medium, https://medium.com/data-science-collective/building-ai-agents-with-openai-sdk-5e48a90dccb2
41. Use Codex with the Agents SDK | OpenAI Developers, https://developers.openai.com/codex/guides/agents-sdk
42. SWE-bench Leaderboards, https://www.swebench.com/
43. Best Agentic AI Frameworks in 2026 for Developers | Uvik Software, https://uvik.net/blog/agentic-ai-frameworks/
44. Best AI Models for Coding in 2026: Claude, Codex & Gemini Compared - TeamAI, https://teamai.com/blog/ai-automation/best-ai-models-for-coding-and-agentic-workflows-2026/
45. Navigating Agentic Protocols: A2A and MCP, https://www.youtube.com/watch?v=_dlcEnsIjtY
46. Agent Interoperability Protocols: MCP, A2A, and OSI Explained - Atlan, https://atlan.com/know/agent-interoperability-protocols/
47. Claude Managed Agents: What It Actually Offers, the Honest Pros and Cons, and How to Run Agents Yourself | by unicodeveloper - Medium, https://medium.com/@unicodeveloper/claude-managed-agents-what-it-actually-offers-the-honest-pros-and-cons-and-how-to-run-agents-52369e5cff14
48. Managed Agents vs. Open Frameworks (LangGraph, CrewAI, etc.) — Which direction are you betting on? : r/LangChain - Reddit, https://www.reddit.com/r/LangChain/comments/1sgh77s/managed_agents_vs_open_frameworks_langgraph/
49. Integrate Vertex AI Agents with Google Workspace, https://codelabs.developers.google.com/vertexai-gws-agents
"""

with open('00-Agent-Platform-Research-summary.md', 'a') as f:
    f.write(refs)

print("References appended successfully.")
