/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * 完整工作流请求。
 */
export type FullProcessRequest = {
    /**
     * 完整剧本文本
     */
    script_text: string;
    /**
     * 项目 ID
     */
    project_id: string;
    /**
     * 章节 ID
     */
    chapter_id: string;
    /**
     * 发现角色混淆问题时是否自动优化剧本
     */
    auto_optimize?: boolean;
};

