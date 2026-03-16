/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SceneRead = {
    /**
     * 资产 ID
     */
    id: string;
    /**
     * 归属项目 ID（可空=全局资产）
     */
    project_id?: (string | null);
    /**
     * 归属章节 ID（可空）
     */
    chapter_id?: (string | null);
    /**
     * 名称
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
     * 计划为该资产生成的视角图片数量（不含分镜帧）
     */
    view_count?: number;
    /**
     * 缩略图下载地址
     */
    thumbnail?: string;
};

