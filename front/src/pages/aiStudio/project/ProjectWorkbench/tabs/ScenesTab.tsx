import { useEffect, useMemo, useState } from 'react'
import { Button, Card, Empty, Input, Modal, Space, message } from 'antd'
import { LinkOutlined, PlusOutlined } from '@ant-design/icons'
import { useParams, useNavigate } from 'react-router-dom'
import { StudioAssetsService, StudioShotLinksService } from '../../../../../services/generated'
import type { ProjectSceneLinkRead, SceneRead } from '../../../../../services/generated'
import { buildFileDownloadUrl, resolveAssetUrl } from '../../../assets/utils'
import { DisplayImageCard } from '../../../assets/components/DisplayImageCard'

export function ScenesTab() {
  const navigate = useNavigate()
  const { projectId } = useParams<{ projectId: string }>()

  const [links, setLinks] = useState<ProjectSceneLinkRead[]>([])
  const [linksLoading, setLinksLoading] = useState(false)
  const [scenesById, setScenesById] = useState<Record<string, SceneRead>>({})

  const [linkModalOpen, setLinkModalOpen] = useState(false)
  const [scenes, setScenes] = useState<SceneRead[]>([])
  const [scenesLoading, setScenesLoading] = useState(false)
  const [search, setSearch] = useState('')
  const [linkingId, setLinkingId] = useState<string | null>(null)
  const [unlinkingId, setUnlinkingId] = useState<number | null>(null)

  const loadLinks = async () => {
    if (!projectId) return
    setLinksLoading(true)
    try {
      const res = await StudioShotLinksService.listProjectSceneLinksApiV1StudioShotLinksSceneGet({
        projectId,
        chapterId: null,
        shotId: null,
        sceneId: null,
        order: null,
        isDesc: false,
        page: 1,
        pageSize: 100,
      })
      const items = res.data?.items ?? []
      setLinks(items)

      const ids = Array.from(new Set(items.map((l) => l.scene_id)))
      const fetched = await Promise.all(
        ids.map((id) =>
          StudioAssetsService.getSceneApiV1StudioAssetsScenesSceneIdGet({ sceneId: id })
            .then((r) => r.data ?? null)
            .catch(() => null),
        ),
      )
      const next: Record<string, SceneRead> = {}
      fetched.filter(Boolean).forEach((s) => {
        next[(s as SceneRead).id] = s as SceneRead
      })
      setScenesById(next)
    } catch {
      message.error('加载项目场景关联失败')
      setLinks([])
      setScenesById({})
    } finally {
      setLinksLoading(false)
    }
  }

  const loadScenes = async (searchQuery?: string) => {
    setScenesLoading(true)
    try {
      const q = (searchQuery !== undefined ? searchQuery : search).trim()
      const res = await StudioAssetsService.listScenesApiV1StudioAssetsScenesGet({
        q: q ? q : null,
        order: 'updated_at',
        isDesc: true,
        page: 1,
        pageSize: 100,
      })
      setScenes(res.data?.items ?? [])
    } catch {
      message.error('加载场景失败')
      setScenes([])
    } finally {
      setScenesLoading(false)
    }
  }

  useEffect(() => {
    void loadLinks()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId])

  useEffect(() => {
    if (linkModalOpen) void loadScenes('')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [linkModalOpen])

  const linkedSceneIdSet = useMemo(() => new Set(links.map((l) => l.scene_id)), [links])
  const availableScenes = useMemo(() => scenes.filter((s) => !linkedSceneIdSet.has(s.id)), [scenes, linkedSceneIdSet])

  const toThumbUrl = (thumbnail?: string) => {
    const url = resolveAssetUrl(thumbnail)
    if (url) return url
    // 兼容后端返回 file_id 的情况
    if (thumbnail && !thumbnail.includes('/') && !thumbnail.includes(':')) return buildFileDownloadUrl(thumbnail)
    return undefined
  }

  const handleLinkScene = async (scene: SceneRead) => {
    if (!projectId) return
    setLinkingId(scene.id)
    try {
      await StudioShotLinksService.createProjectSceneLinkApiV1StudioShotLinksScenePost({
        requestBody: { project_id: projectId, chapter_id: null, shot_id: null, asset_id: scene.id },
      })
      message.success(`已关联场景「${scene.name}」到项目`)
      setLinkModalOpen(false)
      await loadLinks()
    } catch {
      message.error('关联失败')
    } finally {
      setLinkingId(null)
    }
  }

  const handleUnlinkScene = async (link: ProjectSceneLinkRead) => {
    setUnlinkingId(link.id)
    try {
      await StudioShotLinksService.deleteProjectSceneLinkApiV1StudioShotLinksSceneLinkIdDelete({ linkId: link.id })
      message.success('已取消关联')
      await loadLinks()
    } catch {
      message.error('取消关联失败')
    } finally {
      setUnlinkingId(null)
    }
  }

  if (!projectId) return null

  return (
    <>
      <Card
        title="项目场景"
        extra={
          <Space>
            <Button
              type="primary"
              icon={<LinkOutlined />}
              onClick={() => {
                setSearch('')
                setLinkModalOpen(true)
              }}
            >
              从资产库关联
            </Button>
            <Button icon={<PlusOutlined />} onClick={() => navigate('/assets?tab=scene')}>
              前往资产管理
            </Button>
          </Space>
        }
      >
        {links.length === 0 && !linksLoading ? (
          <Empty description="暂无项目场景，可从资产库关联场景到本项目" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {links.map((l) => {
              const s = scenesById[l.scene_id]
              return (
                <DisplayImageCard
                  key={l.id}
                  title={<div className="truncate">{s?.name ?? l.scene_id}</div>}
                  imageUrl={toThumbUrl(l.thumbnail ?? s?.thumbnail)}
                  imageAlt={s?.name ?? l.scene_id}
                  extra={
                    <Button
                      size="small"
                      danger
                      loading={unlinkingId === l.id}
                      onClick={() => {
                        Modal.confirm({
                          title: `取消关联「${s?.name ?? l.scene_id}」？`,
                          okText: '取消关联',
                          cancelText: '取消',
                          okButtonProps: { danger: true },
                          onOk: () => handleUnlinkScene(l),
                        })
                      }}
                    >
                      取消关联
                    </Button>
                  }
                  meta={
                    <div className="space-y-1">
                      <div className="text-xs text-gray-600 line-clamp-2">{s?.description ?? '—'}</div>
                      <div className="text-xs text-gray-500 truncate">scene_id：{l.scene_id}</div>
                    </div>
                  }
                />
              )
            })}
          </div>
        )}
      </Card>

      <Modal
        title="从资产库关联场景"
        open={linkModalOpen}
        onCancel={() => setLinkModalOpen(false)}
        footer={null}
        width={560}
      >
        <div className="mb-3">
          <Input.Search
            placeholder="搜索场景名称"
            allowClear
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onSearch={(value) => loadScenes(value)}
          />
        </div>
        <div className="max-h-[60vh] overflow-y-auto">
          {scenesLoading ? (
            <div className="py-8 text-center text-gray-500">加载中...</div>
          ) : availableScenes.length === 0 ? (
            <Empty description={scenes.length === 0 ? '暂无场景，请先在资产管理中创建场景' : '当前项目已关联全部搜索结果'} />
          ) : (
            <div className="space-y-2">
              {availableScenes.map((scene) => (
                <div
                  key={scene.id}
                  className="flex items-center justify-between gap-3 rounded border border-gray-200 p-2 hover:bg-gray-50"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    {toThumbUrl(scene.thumbnail) ? (
                      <img
                        src={toThumbUrl(scene.thumbnail)}
                        alt=""
                        className="w-10 h-10 rounded object-cover shrink-0"
                      />
                    ) : (
                      <div className="w-10 h-10 rounded bg-gray-100 flex items-center justify-center text-gray-400 shrink-0">
                        —
                      </div>
                    )}
                    <div className="min-w-0">
                      <div className="font-medium truncate">{scene.name}</div>
                      {scene.description && <div className="text-xs text-gray-500 truncate">{scene.description}</div>}
                    </div>
                  </div>
                  <Button type="primary" size="small" loading={linkingId === scene.id} onClick={() => handleLinkScene(scene)}>
                    关联到项目
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>
    </>
  )
}
