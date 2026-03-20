/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Studio 资产草稿（Scene/Prop/Costume）：不含 id，由导入 API 生成。
 */
export type StudioAssetDraft = {
    /**
     * 名称（同项目内建议唯一）
     */
    name: string;
    /**
     * 描述
     */
    description?: string;
    /**
     * 标签
     */
    tags?: Array<string>;
    /**
     * 提示词模板 ID（可空）
     */
    prompt_template_id?: (string | null);
    /**
     * 计划生成视角图数量
     */
    view_count?: number;
};

