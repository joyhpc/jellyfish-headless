import { useNavigate, useParams } from 'react-router-dom'
import type { AssetViewAngle } from '../../../../services/generated'
import type { CharacterImageRead, CharacterRead } from '../../../../services/generated'
import { StudioCastService, StudioImageTasksService } from '../../../../services/generated'
import { AssetEditPageBase } from '../../assets/components/AssetEditPageBase'

type UpdateImagePayload = {
  file_id: string
  width?: number | null
  height?: number | null
  format?: string | null
}

function normalizeUpdateImagePayload(payload: UpdateImagePayload): UpdateImagePayload {
  return {
    ...payload,
    format: payload.format ?? 'png',
  }
}

export default function RoleDetailPage() {
  const navigate = useNavigate()
  const { projectId, characterId } = useParams<{ projectId: string; characterId: string }>()

  if (!characterId) {
    return null
  }

  return (
    <AssetEditPageBase<CharacterRead, CharacterImageRead>
      assetId={characterId}
      missingAssetIdText="缺少 character_id"
      assetDisplayName="角色"
      backTo={projectId ? `/projects/${projectId}?tab=roles` : '/projects'}
      relationType="character_image"
      getAsset={async (id) => {
        const res = await StudioCastService.getCharacterApiV1StudioCastCharactersCharacterIdGet({ characterId: id })
        return (res.data ?? null) as CharacterRead | null
      }}
      updateAsset={async (id, payload) => {
        const res = await StudioCastService.updateCharacterApiV1StudioCastCharactersCharacterIdPatch({
          characterId: id,
          requestBody: payload,
        })
        return (res.data ?? null) as CharacterRead | null
      }}
      listImages={async (id) => {
        const res = await StudioCastService.listCharacterImagesApiV1StudioCastCharactersCharacterIdImagesGet({
          characterId: id,
          page: 1,
          pageSize: 100,
        })
        return (res.data?.items ?? []) as CharacterImageRead[]
      }}
      createImageSlot={async (id, angle: AssetViewAngle) => {
        await StudioCastService.createCharacterImageApiV1StudioCastCharactersCharacterIdImagesPost({
          characterId: id,
          requestBody: { view_angle: angle },
        })
      }}
      updateImage={async (id, imageId, payload) => {
        await StudioCastService.updateCharacterImageApiV1StudioCastCharactersCharacterIdImagesImageIdPatch({
          characterId: id,
          imageId,
          requestBody: normalizeUpdateImagePayload(payload),
        })
      }}
      createGenerationTask={async (id, imageId) => {
        const res = await StudioImageTasksService.createCharacterImageGenerationTaskApiV1StudioImageTasksCharactersCharacterIdImageTasksPost({
          characterId: id,
          requestBody: { image_id: imageId, model_id: null },
        })
        return res.data?.task_id ?? null
      }}
      onNavigate={(to, replace) => navigate(to, replace ? { replace: true } : undefined)}
    />
  )
}

