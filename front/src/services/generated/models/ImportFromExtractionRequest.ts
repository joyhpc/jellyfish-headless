/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StudioAssetDraft } from './StudioAssetDraft';
import type { StudioCharacterDraft } from './StudioCharacterDraft';
import type { StudioShotDraft } from './StudioShotDraft';
/**
 * 导入请求：直接复用 StudioScriptExtractionDraft 结构。
 */
export type ImportFromExtractionRequest = {
    /**
     * 项目 ID（必填）
     */
    project_id: string;
    /**
     * 章节 ID（必填，用于创建 shots/links）
     */
    chapter_id: string;
    /**
     * 剧本文本（可为优化后版本）
     */
    script_text: string;
    characters?: Array<StudioCharacterDraft>;
    scenes?: Array<StudioAssetDraft>;
    props?: Array<StudioAssetDraft>;
    costumes?: Array<StudioAssetDraft>;
    /**
     * 镜头草稿列表
     */
    shots?: Array<StudioShotDraft>;
    on_conflict?: string;
    force_overwrite?: boolean;
};

