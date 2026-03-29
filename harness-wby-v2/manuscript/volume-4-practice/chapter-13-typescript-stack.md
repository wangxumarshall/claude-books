# 第13章：起步阶段（TypeScript栈）

### TypeScript起步阶段技术栈架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TypeScript起步阶段技术栈                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    应用层 (Application)                               │   │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │   │
│   │  │   Mastra   │    │    Zod     │    │  TypeScript │          │   │
│   │  │   Agent    │    │   Schema   │    │   类型系统  │          │   │
│   │  └─────────────┘    └─────────────┘    └─────────────┘          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                          │
│                                    ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    编排层 (Orchestration)                            │   │
│   │  ┌─────────────────────────────────────────────────────────────┐  │   │
│   │  │                      Inngest                                │  │   │
│   │  │   Durable Execution | 断点续传 | Cron调度 | Memoization   │  │   │
│   │  └─────────────────────────────────────────────────────────────┘  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                          │
│                                    ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    工具层 (Tools)                                    │   │
│   │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │   │
│   │  │    MCP     │    │   File     │    │   HTTP     │          │   │
│   │  │  Protocol  │    │   System   │    │   Client   │          │   │
│   │  └─────────────┘    └─────────────┘    └─────────────┘          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   数据流：用户输入 → Mastra Agent → Zod验证 → Inngest编排 → MCP工具执行    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Step 1: Mastra + Zod搭建

完整代码示例：

```typescript
import { z } from 'zod';
import { Agent, createTool } from '@mastra/core';

// 定义Agent状态Schema
const AgentStateSchema = z.object({
  phase: z.enum(['planning', 'executing', 'reviewing', 'completed', 'failed']),
  tools: z.array(z.object({
    name: z.string(),
    arguments: z.record(z.unknown())
  })),
  result: z.union([z.string(), z.null()])
});

// 创建工具
const fileReadTool = createTool({
  id: 'file_read',
  inputSchema: z.object({
    path: z.string()
  }),
  execute: async ({ path }) => {
    // 实现文件读取逻辑
    return { content: '...' };
  }
});

// 创建Agent
const myAgent = new Agent({
  name: 'my-agent',
  instructions: '...',
  tools: { fileReadTool }
});
```

## Step 2: Inngest集成

```typescript
import { inngest } from './client';

export const myWorkflow = inngest.createFunction(
  { id: 'my-workflow' },
  { event: 'app/workflow.start' },
  async ({ event, step }) => {
    // Step 1: 分析任务
    const analysis = await step.run('analyze', async () => {
      return analyzeTask(event.data);
    });

    // Step 2: 执行
    const result = await step.run('execute', async () => {
      return executeTask(analysis);
    });

    // Step 3: 验证
    const validated = await step.run('validate', async () => {
      return validateResult(result);
    });

    return validated;
  }
);
```