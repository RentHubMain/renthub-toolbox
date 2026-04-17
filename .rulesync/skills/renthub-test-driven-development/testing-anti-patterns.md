# 测试反模式

**在以下情况加载本参考：** 编写或修改测试、增加 mock，或想给生产代码加仅测试用的方法时。

## 概述

测试必须验证真实行为，不是 mock 行为。mock 是隔离手段，不是被测对象。

**核心原则：** 测代码做什么，不要测 mock 做什么。

**严格 TDD 可避免这些反模式。**

## 铁律

```
1. 绝不测试 mock 行为
2. 绝不给生产类加仅测试用的方法
3. 绝不在未理解依赖的情况下 mock
```

## 反模式 1：测试 mock 行为

**违规：**
```typescript
// ❌ 不好：在测 mock 是否存在
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**为何错误：**
- 你在验证 mock 能用，不是组件能用
- mock 在就通过，不在就失败
- 对真实行为一无所知

**协作伙伴的纠正：** 「我们在测 mock 的行为吗？」

**修复：**
```typescript
// ✅ 好：测真实组件，或不 mock
test('renders sidebar', () => {
  render(<Page />);  // 不要 mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// 或若 sidebar 必须 mock 以隔离：
// 不要对 mock 断言 — 测 Page 在 sidebar 存在时的行为
```

### 门禁

```
在对任何 mock 元素断言之前：
  问：「我在测真实组件行为，还是仅 mock 存在？」

  若测的是 mock 存在：
    停 — 删掉该断言或取消 mock

  改测真实行为
```

## 反模式 2：生产代码中的仅测试方法

**违规：**
```typescript
// ❌ 不好：destroy() 仅在测试中使用
class Session {
  async destroy() {  // 看起来像生产 API！
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// 测试中
afterEach(() => session.destroy());
```

**为何错误：**
- 生产类被仅测试代码污染
- 若在生产误调用很危险
- 违背 YAGNI 与职责分离
- 混淆对象生命周期与实体生命周期

**修复：**
```typescript
// ✅ 好：测试工具负责测试清理
// Session 无 destroy() — 在生产中无状态

// 在 test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// 测试中
afterEach(() => cleanupSession(session));
```

### 门禁

```
在给生产类加任何方法之前：
  问：「这是否仅被测试使用？」

  若是：
    停 — 不要加
    放进测试工具

  问：「该类是否拥有该资源的生命周期？」

  若否：
    停 — 放错类了
```

## 反模式 3：未理解就 mock

**违规：**
```typescript
// ❌ 不好：mock 破坏了测试逻辑
test('detects duplicate server', () => {
  // mock 阻止了测试依赖的配置写入！
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // 应抛错 — 但不会！
});
```

**为何错误：**
- 被 mock 的方法有测试依赖的副作用（写配置）
- 过度 mock「求稳」反而破坏真实行为
- 测试因错误原因通过或神秘失败

**修复：**
```typescript
// ✅ 好：在正确层次 mock
test('detects duplicate server', () => {
  // 只 mock 慢的部分，保留测试需要的行为
  vi.mock('MCPServerManager'); // 只 mock 慢速服务启动

  await addServer(config);  // 配置已写入
  await addServer(config);  // 检测到重复 ✓
});
```

### 门禁

```
在 mock 任何方法之前：
  停 — 先不要 mock

  1. 问：「真实方法有什么副作用？」
  2. 问：「本测试是否依赖其中任一副作用？」
  3. 问：「我是否完全理解本测试需要什么？」

  若依赖副作用：
    在更低层 mock（真正的慢/外部操作）
    或使用保留必要行为的测试替身
    不要 mock 测试所依赖的高层方法

  若不确定测试依赖什么：
    先用真实实现跑测试
    观察实际需要什么
    再在正确位置加最少 mock

  红旗：
    - 「我 mock 一下求稳」
    - 「可能慢，不如 mock」
    - 不理解依赖链就 mock
```

## 反模式 4：不完整 mock

**违规：**
```typescript
// ❌ 不好：部分 mock — 只填你以为需要的字段
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // 缺：下游代码会用到的 metadata
};

// 稍后：代码访问 response.metadata.requestId 时崩
```

**为何错误：**
- **部分 mock 隐藏结构假设** — 只 mock 你知道的字段
- **下游可能依赖你未包含的字段** — 静默失败
- **测试通过但联调失败** — mock 不完整，真实 API 完整
- **虚假信心** — 测试对真实行为什么也证明不了

**铁律：** mock **完整**的数据结构，如现实中那样，不要只 mock 当前测试立刻用到的字段。

**修复：**
```typescript
// ✅ 好：镜像真实 API 的完整性
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // 真实 API 返回的全部字段
};
```

### 门禁

```
在创建 mock 响应之前：
  查：「真实 API 响应包含哪些字段？」

  行动：
    1. 从文档/示例查看真实 API 响应
    2. 包含下游可能消费的全部字段
    3. 验证 mock 与真实响应 schema 完全一致

  关键：
    做 mock 就必须理解**整个**结构
    部分 mock 在代码依赖被省略字段时会静默失败

  若不确定：包含文档中的全部字段
```

## 反模式 5：集成测试当后话

**违规：**
```
✅ 实现完成
❌ 未写测试
「可以测了」
```

**为何错误：**
- 测试是实现的一部分，不是可选后续
- TDD 本可早发现
- 没有测试不能算完成

**修复：**
```
TDD 循环：
1. 写失败测试
2. 实现至通过
3. 重构
4. 再声称完成
```

## mock 过于复杂时

**警示：**
- mock 搭建比测试逻辑还长
- 为让测试通过而 mock 一切
- mock 缺少真实组件有的方法
- mock 一变测试就挂

**协作伙伴会问：** 「这里真的需要 mock 吗？」

**考虑：** 用真实组件的集成测试往往比复杂 mock 更简单

## TDD 如何避免这些反模式

**为何有帮助：**
1. **先写测试** → 迫使你想清到底在测什么
2. **看它失败** → 确认测的是真实行为而非 mock
3. **最少实现** → 仅测试方法不会悄悄混进来
4. **真实依赖** → mock 前你已看到测试实际需要什么

**若你在测 mock 行为，你已违背 TDD** — 没先看对真实代码失败就加了 mock。

## 速查

| 反模式 | 修复 |
|--------------|-----|
| 对 mock 元素断言 | 测真实组件或取消 mock |
| 生产中的仅测试方法 | 移到测试工具 |
| 不理解就 mock | 先理解依赖，最少 mock |
| 不完整 mock | 完整镜像真实 API |
| 测试当后话 | TDD — 测试先行 |
| mock 过度复杂 | 考虑集成测试 |

## 红旗

- 断言检查 `*-mock` 测试 ID
- 方法仅出现在测试文件中
- mock 搭建占测试一半以上
- 去掉 mock 测试就挂
- 说不清为何需要 mock
- 「mock 一下求稳」

## 结论

**mock 是隔离工具，不是被测对象。**

若 TDD 让你发现自己在测 mock 行为，你已经走偏了。

修复：测真实行为，或质疑是否根本不该在这里 mock。
