"""演员/角色相关 CRUD：Actor / Character / CharacterPropLink / ShotCharacterLink。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import apply_keyword_filter, apply_order, paginate
from app.dependencies import get_db
from app.models.studio import (
    Actor,
    ActorImage,
    AssetViewAngle,
    Chapter,
    Character,
    CharacterImage,
    CharacterPropLink,
    Costume,
    Project,
    Prop,
    Shot,
    ShotCharacterLink,
)
from app.schemas.common import ApiResponse, PaginatedData, paginated_response, success_response
from app.schemas.studio.cast import (
    ActorCreate,
    ActorRead,
    ActorUpdate,
    CharacterCreate,
    CharacterPropLinkCreate,
    CharacterPropLinkRead,
    CharacterPropLinkUpdate,
    CharacterRead,
    CharacterUpdate,
    ShotCharacterLinkCreate,
    ShotCharacterLinkRead,
    ShotCharacterLinkUpdate,
)
from app.schemas.studio.cast_images import ActorImageRead
from app.schemas.studio.assets import AssetImageCreate, AssetImageUpdate, CharacterImageRead

router = APIRouter()

ACTOR_ORDER_FIELDS = {"name", "created_at", "updated_at"}
CHARACTER_ORDER_FIELDS = {"name", "created_at", "updated_at"}
LINK_ORDER_FIELDS = {"index", "id", "created_at", "updated_at"}
IMAGE_ORDER_FIELDS = {"id", "quality_level", "view_angle", "created_at", "updated_at"}
DOWNLOAD_URL_TEMPLATE = "/api/v1/studio/files/{file_id}/download"


async def _ensure_project_exists(db: AsyncSession, project_id: str) -> None:
    if await db.get(Project, project_id) is None:
        raise HTTPException(status_code=400, detail="Project not found")


async def _ensure_actor_exists(db: AsyncSession, actor_id: str) -> None:
    if await db.get(Actor, actor_id) is None:
        raise HTTPException(status_code=400, detail="Actor not found")


async def _ensure_costume_exists(db: AsyncSession, costume_id: str) -> None:
    if await db.get(Costume, costume_id) is None:
        raise HTTPException(status_code=400, detail="Costume not found")


async def _ensure_prop_exists(db: AsyncSession, prop_id: str) -> None:
    if await db.get(Prop, prop_id) is None:
        raise HTTPException(status_code=400, detail="Prop not found")


async def _ensure_shot_exists(db: AsyncSession, shot_id: str) -> None:
    if await db.get(Shot, shot_id) is None:
        raise HTTPException(status_code=400, detail="Shot not found")


async def _ensure_single_primary_character_image(
    db: AsyncSession,
    *,
    character_id: str,
    keep_id: int | None,
) -> None:
    """同一角色下只允许一张主图：把其他行 is_primary 置 false。"""
    stmt = (
        CharacterImage.__table__.update()
        .where(CharacterImage.character_id == character_id)
    )
    if keep_id is not None:
        stmt = stmt.where(CharacterImage.id != keep_id)
    stmt = stmt.values(is_primary=False)
    await db.execute(stmt)


def _download_url(file_id: str) -> str:
    return DOWNLOAD_URL_TEMPLATE.format(file_id=file_id)


async def _resolve_actor_thumbnails(
    db: AsyncSession,
    *,
    actor_ids: list[str],
) -> dict[str, str]:
    if not actor_ids:
        return {}

    stmt = select(ActorImage).where(
        ActorImage.actor_id.in_(actor_ids),
        ActorImage.file_id.is_not(None),
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    best: dict[str, tuple[int, int, int, str]] = {}
    for row in rows:
        file_id = row.file_id
        if not file_id:
            continue
        created_ts = int(row.created_at.timestamp()) if row.created_at else -1
        score = (
            1 if row.view_angle == AssetViewAngle.front else 0,
            created_ts,
            row.id,
        )
        current = best.get(row.actor_id)
        if current is None or score > current[:3]:
            best[row.actor_id] = (*score, file_id)

    return {actor_id: _download_url(score[3]) for actor_id, score in best.items()}


async def _resolve_character_thumbnails(
    db: AsyncSession,
    *,
    character_ids: list[str],
) -> dict[str, str]:
    if not character_ids:
        return {}

    stmt = select(CharacterImage).where(
        CharacterImage.character_id.in_(character_ids),
        CharacterImage.file_id.is_not(None),
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    best: dict[str, tuple[int, int, int, str]] = {}
    for row in rows:
        file_id = row.file_id
        if not file_id:
            continue
        created_ts = int(row.created_at.timestamp()) if row.created_at else -1
        score = (
            1 if row.view_angle == AssetViewAngle.front else 0,
            created_ts,
            row.id,
        )
        current = best.get(row.character_id)
        if current is None or score > current[:3]:
            best[row.character_id] = (*score, file_id)

    return {character_id: _download_url(score[3]) for character_id, score in best.items()}


# ---------- Actor ----------


@router.get(
    "/actors",
    response_model=ApiResponse[PaginatedData[ActorRead]],
    summary="演员列表（分页）",
)
async def list_actors(
    db: AsyncSession = Depends(get_db),
    q: str | None = Query(None, description="关键字，过滤 name/description"),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> ApiResponse[PaginatedData[ActorRead]]:
    stmt = select(Actor)
    stmt = apply_keyword_filter(stmt, q=q, fields=[Actor.name, Actor.description])
    stmt = apply_order(stmt, model=Actor, order=order, is_desc=is_desc, allow_fields=ACTOR_ORDER_FIELDS, default="created_at")
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    thumbnails = await _resolve_actor_thumbnails(db, actor_ids=[x.id for x in items])
    payload = [
        ActorRead.model_validate(x).model_copy(update={"thumbnail": thumbnails.get(x.id, "")})
        for x in items
    ]
    return paginated_response(payload, page=page, page_size=page_size, total=total)


@router.post(
    "/actors",
    response_model=ApiResponse[ActorRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建演员",
)
async def create_actor(
    body: ActorCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ActorRead]:
    exists = await db.get(Actor, body.id)
    if exists is not None:
        raise HTTPException(status_code=400, detail=f"Actor with id={body.id} already exists")
    # Actor 不再归属 project/chapter
    obj = Actor(**body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)

    DEFAULT_VIEW_ANGLES: tuple[AssetViewAngle, ...] = (
        AssetViewAngle.front,
        AssetViewAngle.left,
        AssetViewAngle.right,
        AssetViewAngle.back,
    )
    angles = list(DEFAULT_VIEW_ANGLES[: min(max(obj.view_count, 0), len(DEFAULT_VIEW_ANGLES))])
    for angle in angles:
        db.add(ActorImage(actor_id=obj.id, view_angle=angle))
    if angles:
        await db.flush()

    return success_response(ActorRead.model_validate(obj), code=201)


@router.get(
    "/actors/{actor_id}",
    response_model=ApiResponse[ActorRead],
    summary="获取演员",
)
async def get_actor(
    actor_id: str,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ActorRead]:
    obj = await db.get(Actor, actor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    thumbnails = await _resolve_actor_thumbnails(db, actor_ids=[obj.id])
    return success_response(ActorRead.model_validate(obj).model_copy(update={"thumbnail": thumbnails.get(obj.id, "")}))


@router.patch(
    "/actors/{actor_id}",
    response_model=ApiResponse[ActorRead],
    summary="更新演员",
)
async def update_actor(
    actor_id: str,
    body: ActorUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ActorRead]:
    obj = await db.get(Actor, actor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    return success_response(ActorRead.model_validate(obj))


# ---------- Actor images ----------


@router.get(
    "/actors/{actor_id}/images",
    response_model=ApiResponse[PaginatedData[ActorImageRead]],
    summary="演员图片列表（分页）",
)
async def list_actor_images(
    actor_id: str,
    db: AsyncSession = Depends(get_db),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    stmt = select(ActorImage).where(ActorImage.actor_id == actor_id)
    stmt = apply_order(stmt, model=ActorImage, order=order, is_desc=is_desc, allow_fields=IMAGE_ORDER_FIELDS, default="id")
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    return paginated_response([ActorImageRead.model_validate(x) for x in items], page=page, page_size=page_size, total=total)


@router.post(
    "/actors/{actor_id}/images",
    response_model=ApiResponse[ActorImageRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建演员图片",
)
async def create_actor_image(
    actor_id: str,
    body: AssetImageCreate,
    db: AsyncSession = Depends(get_db),
):
    if await db.get(Actor, actor_id) is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    obj = ActorImage(actor_id=actor_id, **body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return success_response(ActorImageRead.model_validate(obj), code=201)


@router.patch(
    "/actors/{actor_id}/images/{image_id}",
    response_model=ApiResponse[ActorImageRead],
    summary="更新演员图片",
)
async def update_actor_image(
    actor_id: str,
    image_id: int,
    body: AssetImageUpdate,
    db: AsyncSession = Depends(get_db),
):
    obj = await db.get(ActorImage, image_id)
    if obj is None or obj.actor_id != actor_id:
        raise HTTPException(status_code=404, detail="ActorImage not found")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    return success_response(ActorImageRead.model_validate(obj))


@router.delete(
    "/actors/{actor_id}/images/{image_id}",
    response_model=ApiResponse[None],
    summary="删除演员图片",
)
async def delete_actor_image(
    actor_id: str,
    image_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(ActorImage, image_id)
    if obj is None or obj.actor_id != actor_id:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)


@router.delete(
    "/actors/{actor_id}",
    response_model=ApiResponse[None],
    summary="删除演员",
)
async def delete_actor(
    actor_id: str,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(Actor, actor_id)
    if obj is None:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)


# ---------- Character ----------


@router.get(
    "/characters",
    response_model=ApiResponse[PaginatedData[CharacterRead]],
    summary="角色列表（分页）",
)
async def list_characters(
    db: AsyncSession = Depends(get_db),
    project_id: str | None = Query(None, description="按项目过滤"),
    q: str | None = Query(None, description="关键字，过滤 name/description"),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> ApiResponse[PaginatedData[CharacterRead]]:
    stmt = select(Character)
    if project_id is not None:
        stmt = stmt.where(Character.project_id == project_id)
    stmt = apply_keyword_filter(stmt, q=q, fields=[Character.name, Character.description])
    stmt = apply_order(stmt, model=Character, order=order, is_desc=is_desc, allow_fields=CHARACTER_ORDER_FIELDS, default="created_at")
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    thumbnails = await _resolve_character_thumbnails(db, character_ids=[x.id for x in items])
    payload = [
        CharacterRead.model_validate(x).model_copy(update={"thumbnail": thumbnails.get(x.id, "")})
        for x in items
    ]
    return paginated_response(payload, page=page, page_size=page_size, total=total)


@router.post(
    "/characters",
    response_model=ApiResponse[CharacterRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建角色",
)
async def create_character(
    body: CharacterCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterRead]:
    exists = await db.get(Character, body.id)
    if exists is not None:
        raise HTTPException(status_code=400, detail=f"Character with id={body.id} already exists")
    await _ensure_project_exists(db, body.project_id)
    await _ensure_actor_exists(db, body.actor_id)
    if body.costume_id is not None:
        await _ensure_costume_exists(db, body.costume_id)
    obj = Character(**body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return success_response(CharacterRead.model_validate(obj), code=201)


@router.get(
    "/characters/{character_id}",
    response_model=ApiResponse[CharacterRead],
    summary="获取角色",
)
async def get_character(
    character_id: str,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterRead]:
    obj = await db.get(Character, character_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return success_response(CharacterRead.model_validate(obj))


@router.patch(
    "/characters/{character_id}",
    response_model=ApiResponse[CharacterRead],
    summary="更新角色",
)
async def update_character(
    character_id: str,
    body: CharacterUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterRead]:
    obj = await db.get(Character, character_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Character not found")
    update_data = body.model_dump(exclude_unset=True)
    if "project_id" in update_data:
        await _ensure_project_exists(db, update_data["project_id"])
    if "actor_id" in update_data and update_data["actor_id"] is not None:
        await _ensure_actor_exists(db, update_data["actor_id"])
    if "costume_id" in update_data and update_data["costume_id"] is not None:
        await _ensure_costume_exists(db, update_data["costume_id"])
    for k, v in update_data.items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    return success_response(CharacterRead.model_validate(obj))


@router.delete(
    "/characters/{character_id}",
    response_model=ApiResponse[None],
    summary="删除角色",
)
async def delete_character(
    character_id: str,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(Character, character_id)
    if obj is None:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)


# ---------- CharacterPropLink ----------


@router.get(
    "/character-prop-links",
    response_model=ApiResponse[PaginatedData[CharacterPropLinkRead]],
    summary="角色-道具关联列表（分页）",
)
async def list_character_prop_links(
    db: AsyncSession = Depends(get_db),
    character_id: str | None = Query(None),
    prop_id: str | None = Query(None),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> ApiResponse[PaginatedData[CharacterPropLinkRead]]:
    stmt = select(CharacterPropLink)
    if character_id is not None:
        stmt = stmt.where(CharacterPropLink.character_id == character_id)
    if prop_id is not None:
        stmt = stmt.where(CharacterPropLink.prop_id == prop_id)
    stmt = apply_order(stmt, model=CharacterPropLink, order=order, is_desc=is_desc, allow_fields=LINK_ORDER_FIELDS, default="index")
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    return paginated_response([CharacterPropLinkRead.model_validate(x) for x in items], page=page, page_size=page_size, total=total)


@router.post(
    "/character-prop-links",
    response_model=ApiResponse[CharacterPropLinkRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建角色-道具关联",
)
async def create_character_prop_link(
    body: CharacterPropLinkCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterPropLinkRead]:
    if await db.get(Character, body.character_id) is None:
        raise HTTPException(status_code=400, detail="Character not found")
    await _ensure_prop_exists(db, body.prop_id)
    obj = CharacterPropLink(**body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return success_response(CharacterPropLinkRead.model_validate(obj), code=201)


@router.patch(
    "/character-prop-links/{link_id}",
    response_model=ApiResponse[CharacterPropLinkRead],
    summary="更新角色-道具关联",
)
async def update_character_prop_link(
    link_id: int,
    body: CharacterPropLinkUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterPropLinkRead]:
    obj = await db.get(CharacterPropLink, link_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="CharacterPropLink not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    return success_response(CharacterPropLinkRead.model_validate(obj))


@router.delete(
    "/character-prop-links/{link_id}",
    response_model=ApiResponse[None],
    summary="删除角色-道具关联",
)
async def delete_character_prop_link(
    link_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(CharacterPropLink, link_id)
    if obj is None:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)


# ---------- ShotCharacterLink ----------


@router.get(
    "/shot-character-links",
    response_model=ApiResponse[PaginatedData[ShotCharacterLinkRead]],
    summary="镜头-角色关联列表（分页）",
)
async def list_shot_character_links(
    db: AsyncSession = Depends(get_db),
    shot_id: str | None = Query(None),
    character_id: str | None = Query(None),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> ApiResponse[PaginatedData[ShotCharacterLinkRead]]:
    stmt = select(ShotCharacterLink)
    if shot_id is not None:
        stmt = stmt.where(ShotCharacterLink.shot_id == shot_id)
    if character_id is not None:
        stmt = stmt.where(ShotCharacterLink.character_id == character_id)
    stmt = apply_order(stmt, model=ShotCharacterLink, order=order, is_desc=is_desc, allow_fields=LINK_ORDER_FIELDS, default="index")
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    return paginated_response([ShotCharacterLinkRead.model_validate(x) for x in items], page=page, page_size=page_size, total=total)


@router.post(
    "/shot-character-links",
    response_model=ApiResponse[ShotCharacterLinkRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建镜头-角色关联",
)
async def create_shot_character_link(
    body: ShotCharacterLinkCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ShotCharacterLinkRead]:
    await _ensure_shot_exists(db, body.shot_id)
    if await db.get(Character, body.character_id) is None:
        raise HTTPException(status_code=400, detail="Character not found")
    obj = ShotCharacterLink(**body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return success_response(ShotCharacterLinkRead.model_validate(obj), code=201)


@router.patch(
    "/shot-character-links/{link_id}",
    response_model=ApiResponse[ShotCharacterLinkRead],
    summary="更新镜头-角色关联",
)
async def update_shot_character_link(
    link_id: int,
    body: ShotCharacterLinkUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[ShotCharacterLinkRead]:
    obj = await db.get(ShotCharacterLink, link_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ShotCharacterLink not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    return success_response(ShotCharacterLinkRead.model_validate(obj))


@router.delete(
    "/shot-character-links/{link_id}",
    response_model=ApiResponse[None],
    summary="删除镜头-角色关联",
)
async def delete_shot_character_link(
    link_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(ShotCharacterLink, link_id)
    if obj is None:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)


# ---------- CharacterImage ----------


@router.get(
    "/characters/{character_id}/images",
    response_model=ApiResponse[PaginatedData[CharacterImageRead]],
    summary="角色图片列表（分页）",
)
async def list_character_images(
    character_id: str,
    db: AsyncSession = Depends(get_db),
    order: str | None = Query(None),
    is_desc: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> ApiResponse[PaginatedData[CharacterImageRead]]:
    stmt = (
        select(CharacterImage)
        .where(CharacterImage.character_id == character_id)
    )
    stmt = apply_order(
        stmt,
        model=CharacterImage,
        order=order,
        is_desc=is_desc,
        allow_fields=IMAGE_ORDER_FIELDS,
        default="id",
    )
    items, total = await paginate(db, stmt=stmt, page=page, page_size=page_size)
    return paginated_response(
        [CharacterImageRead.model_validate(x) for x in items],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post(
    "/characters/{character_id}/images",
    response_model=ApiResponse[CharacterImageRead],
    status_code=status.HTTP_201_CREATED,
    summary="创建角色图片",
)
async def create_character_image(
    character_id: str,
    body: AssetImageCreate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterImageRead]:
    parent = await db.get(Character, character_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Character not found")
    obj = CharacterImage(character_id=character_id, **body.model_dump())
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    if obj.is_primary:
        await _ensure_single_primary_character_image(
            db,
            character_id=character_id,
            keep_id=obj.id,
        )
        await db.refresh(obj)
    return success_response(CharacterImageRead.model_validate(obj), code=201)


@router.patch(
    "/characters/{character_id}/images/{image_id}",
    response_model=ApiResponse[CharacterImageRead],
    summary="更新角色图片",
)
async def update_character_image(
    character_id: str,
    image_id: int,
    body: AssetImageUpdate,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[CharacterImageRead]:
    obj = await db.get(CharacterImage, image_id)
    if obj is None or obj.character_id != character_id:
        raise HTTPException(status_code=404, detail="CharacterImage not found")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(obj, k, v)
    await db.flush()
    await db.refresh(obj)
    if update_data.get("is_primary") is True:
        await _ensure_single_primary_character_image(
            db,
            character_id=character_id,
            keep_id=obj.id,
        )
        await db.refresh(obj)
    return success_response(CharacterImageRead.model_validate(obj))


@router.delete(
    "/characters/{character_id}/images/{image_id}",
    response_model=ApiResponse[None],
    summary="删除角色图片",
)
async def delete_character_image(
    character_id: str,
    image_id: int,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse[None]:
    obj = await db.get(CharacterImage, image_id)
    if obj is None or obj.character_id != character_id:
        return success_response(None)
    await db.delete(obj)
    await db.flush()
    return success_response(None)

