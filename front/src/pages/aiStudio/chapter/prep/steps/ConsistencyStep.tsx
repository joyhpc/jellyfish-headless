import { useEffect, useMemo, useState } from 'react'
import { Button, Card, Empty, List, Modal, Space, Input, Tag, message } from 'antd'
import { EditOutlined, ReloadOutlined, SaveOutlined, ThunderboltOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { ScriptProcessingService, StudioChaptersService } from '../../../../../services/generated'
import { usePrepFlow } from '../usePrepFlow'

export default function ConsistencyStep() {
  const {
    projectId,
    chapterId,
    workingScriptText,
    setWorkingScriptText,
    baseRawText,
    setBaseRawText,
    consistencyResult,
    setConsistencyResult,
    setConsistencyDone,
  } = usePrepFlow()
  const navigate = useNavigate()

  const [checking, setChecking] = useState(false)
  const [optimizing, setOptimizing] = useState(false)
  const [saving, setSaving] = useState(false)

  const [manualOpen, setManualOpen] = useState(false)
  const [manualValue, setManualValue] = useState(workingScriptText)

  const [optimizeOpen, setOptimizeOpen] = useState(false)
  const [optimizedValue, setOptimizedValue] = useState('')
  const [ignoredIssueKeys, setIgnoredIssueKeys] = useState<Record<string, true>>({})

  const issues = useMemo(() => {
    const list = (consistencyResult?.issues as any[] | undefined) ?? []
    return Array.isArray(list) ? list : []
  }, [consistencyResult])

  const hasIssues = !!consistencyResult?.has_issues
  const busy = checking || optimizing || saving

  useEffect(() => {
    // 新一轮检查结果出来后，重置忽略状态（避免上一轮残留）
    setIgnoredIssueKeys({})
  }, [consistencyResult])

  const runCheck = async () => {
    if (!workingScriptText.trim()) {
      message.warning('请先输入剧本原文')
      return
    }
    setChecking(true)
    try {
      const res = await ScriptProcessingService.checkConsistencyApiV1ScriptProcessingCheckConsistencyPost({
        requestBody: { script_text: workingScriptText },
      })
      const data = res.data
      if (!data) {
        message.error(res.message || '一致性检查失败')
        return
      }
      setConsistencyResult(data as any)
      setConsistencyDone(true)
      if (data.has_issues) message.warning(`发现 ${data.issues?.length ?? 0} 个角色混淆问题`)
      else message.success('未发现角色混淆问题')
    } catch (e: any) {
      message.error(e?.message || '一致性检查失败')
    } finally {
      setChecking(false)
    }
  }

  const runOptimize = async () => {
    if (!workingScriptText.trim()) {
      message.warning('请先输入剧本原文')
      return
    }
    if (!consistencyResult) {
      message.info('请先运行一致性检查')
      return
    }
    setOptimizing(true)
    try {
      const res = await ScriptProcessingService.optimizeScriptApiV1ScriptProcessingOptimizeScriptPost({
        requestBody: {
          script_text: workingScriptText,
          consistency: consistencyResult as any,
        },
      })
      const data = res.data
      if (!data) {
        message.error(res.message || '自动优化失败')
        return
      }
      setOptimizedValue(data.optimized_script_text)
      setOptimizeOpen(true)
    } catch (e: any) {
      message.error(e?.message || '自动优化失败')
    } finally {
      setOptimizing(false)
    }
  }

  const openManualEdit = () => {
    setManualValue(workingScriptText)
    setManualOpen(true)
  }

  const ignoreAndContinue = () => {
    navigate(`/projects/${projectId}/chapters/${chapterId}/prep/divide`)
  }

  const ignoreIssue = (key: string) => {
    setIgnoredIssueKeys((prev) => ({ ...prev, [key]: true }))
  }

  const ignoreAllIssues = () => {
    const next: Record<string, true> = {}
    issues.forEach((it, idx) => {
      const k = String(it?.description ?? idx)
      next[k] = true
    })
    setIgnoredIssueKeys(next)
  }

  const ignoredCount = useMemo(() => {
    if (!consistencyResult) return 0
    let n = 0
    issues.forEach((it, idx) => {
      const k = String(it?.description ?? idx)
      if (ignoredIssueKeys[k]) n += 1
    })
    return n
  }, [consistencyResult, ignoredIssueKeys, issues])

  const allIgnored = consistencyResult && issues.length > 0 && ignoredCount >= issues.length

  const saveToChapter = async (scriptText: string) => {
    if (!scriptText.trim()) {
      message.warning('剧本文本不能为空')
      return
    }
    setSaving(true)
    try {
      const res = await StudioChaptersService.updateChapterApiV1StudioChaptersChapterIdPatch({
        chapterId,
        requestBody: { raw_text: scriptText },
      })
      if (!res.data) {
        message.error(res.message || '保存失败')
        return
      }
      setWorkingScriptText(scriptText)
      setBaseRawText(scriptText)
      setConsistencyDone(false)
      setConsistencyResult(null)
      message.success('已保存到章节原文')
    } catch (e: any) {
      message.error(e?.message || '保存失败')
    } finally {
      setSaving(false)
    }
  }

  const recheckFrom = async (scriptText: string) => {
    if (!scriptText.trim()) {
      message.warning('剧本文本不能为空')
      return
    }
    setWorkingScriptText(scriptText)
    setConsistencyResult(null)
    setConsistencyDone(false)
    await runCheck()
  }

  return (
    <Card
      title="Step 1 / 3：角色混淆一致性检查"
      style={{ flex: 1, minHeight: 0, overflow: 'auto' }}
      bodyStyle={{ padding: 12 }}
      extra={
        <Space>
          <Button icon={<ReloadOutlined />} loading={checking} disabled={busy} onClick={() => void runCheck()}>
            运行检查
          </Button>
        </Space>
      }
    >
      {!consistencyResult ? (
        <Empty description="尚未运行检查。建议先运行检查，若有冲突再选择忽略/手改/自动优化。" />
      ) : issues.length === 0 ? (
        <Empty description="未发现问题，可以继续下一步" image={Empty.PRESENTED_IMAGE_SIMPLE}>
          <Button type="primary" disabled={busy} onClick={ignoreAndContinue}>
            进入下一步
          </Button>
        </Empty>
      ) : (
        <div className="space-y-3">
          <Card size="small" title="摘要">
            <Space wrap>
              <Tag color={hasIssues ? 'red' : 'green'}>{hasIssues ? '发现问题' : '无问题'}</Tag>
              <Tag>issues：{issues.length}</Tag>
              <Tag color={allIgnored ? 'green' : 'default'}>已忽略：{ignoredCount}/{issues.length}</Tag>
            </Space>
            {consistencyResult?.summary ? (
              <div className="text-xs text-gray-500 mt-2">{String(consistencyResult.summary)}</div>
            ) : null}
          </Card>
          <Card
            size="small"
            title="问题列表"
            extra={
              <Space>
                <Button icon={<EditOutlined />} disabled={busy} onClick={openManualEdit}>
                  手动修改
                </Button>
                <Button type="primary" icon={<ThunderboltOutlined />} disabled={busy} loading={optimizing} onClick={() => void runOptimize()}>
                  自动优化剧本
                </Button>
                <Button disabled={busy} onClick={ignoreAllIssues}>忽略全部</Button>
              </Space>
            }
          >
            <List
              size="small"
              dataSource={issues}
              renderItem={(it: any, idx) => (
                <List.Item
                  actions={[
                    <Button
                      key="ignore"
                      size="small"
                      disabled={busy || ignoredIssueKeys[String(it?.description ?? idx)]}
                      onClick={() => ignoreIssue(String(it?.description ?? idx))}
                    >
                      {ignoredIssueKeys[String(it?.description ?? idx)] ? '已忽略' : '忽略'}
                    </Button>,
                  ]}
                >
                  <div className="min-w-0">
                    <div className="font-medium">
                      {it?.issue_type ? `[${it.issue_type}] ` : ''}
                      Issue {idx + 1}
                    </div>
                    <div className="text-sm">{it?.description}</div>
                    {it?.character_candidates?.length ? (
                      <div className="text-xs text-gray-500 mt-1">候选角色：{it.character_candidates.join('、')}</div>
                    ) : null}
                    {it?.suggestion ? (
                      <div className="text-xs text-gray-500 mt-1">建议：{it.suggestion}</div>
                    ) : null}
                    {it?.affected_lines ? (
                      <div className="text-xs text-gray-400 mt-1">
                        影响范围：{it.affected_lines.start_line ?? '-'}–{it.affected_lines.end_line ?? '-'}
                      </div>
                    ) : null}
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </div>
      )}

      <Modal
        title="手动修改（可再次检查或直接保存）"
        open={manualOpen}
        onCancel={() => (busy ? null : setManualOpen(false))}
        footer={
          <Space>
            <Button disabled={busy} onClick={() => setManualOpen(false)}>关闭</Button>
            <Button icon={<ReloadOutlined />} disabled={busy} loading={checking} onClick={() => void recheckFrom(manualValue)}>
              再次检查
            </Button>
            <Button
              icon={<SaveOutlined />}
              type="primary"
              disabled={busy}
              loading={saving}
              onClick={() => void saveToChapter(manualValue)}
            >
              直接保存
            </Button>
          </Space>
        }
        width={900}
      >
        <Input.TextArea
          value={manualValue}
          onChange={(e) => setManualValue(e.target.value)}
          rows={16}
          className="font-mono text-sm"
        />
      </Modal>

      <Modal
        title="自动优化对比（可编辑优化结果）"
        open={optimizeOpen}
        onCancel={() => (busy ? null : setOptimizeOpen(false))}
        footer={
          <Space>
            <Button disabled={busy} onClick={() => setOptimizeOpen(false)}>关闭</Button>
            <Button
              icon={<SaveOutlined />}
              type="primary"
              disabled={busy}
              loading={saving}
              onClick={() => void saveToChapter(optimizedValue)}
            >
              直接保存
            </Button>
          </Space>
        }
        width={1000}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <div className="text-xs text-gray-600 mb-1">原文</div>
            <Input.TextArea value={baseRawText} readOnly rows={16} className="font-mono text-sm" />
          </div>
          <div>
            <div className="text-xs text-gray-600 mb-1">优化后（可编辑）</div>
            <Input.TextArea
              value={optimizedValue}
              onChange={(e) => setOptimizedValue(e.target.value)}
              rows={16}
              className="font-mono text-sm"
              disabled={busy}
            />
          </div>
        </div>
      </Modal>
    </Card>
  )
}

