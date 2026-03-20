/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Studio 角色草稿：不含 id，由导入 API 生成。
 */
export type StudioCharacterDraft = {
    /**
     * 角色名称（同项目内建议唯一）
     */
    name: string;
    /**
     * 角色描述
     */
    description?: string;
    /**
     * 标签（可选）
     */
    tags?: Array<string>;
    /**
     * 服装名称（可选，导入时映射到 costume_id）
     */
    costume_name?: (string | null);
    /**
     * 角色常用道具名称列表（可选）
     */
    prop_names?: Array<string>;
};

