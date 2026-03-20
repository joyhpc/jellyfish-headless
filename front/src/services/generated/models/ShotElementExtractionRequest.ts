/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * 镜头元素提取请求。
 */
export type ShotElementExtractionRequest = {
    /**
     * 镜头序号（章节内唯一）
     */
    index: number;
    /**
     * 镜头的文本内容
     */
    shot_text: string;
    /**
     * 前文摘要（可选）
     */
    context_summary?: (string | null);
    /**
     * 分镜元信息（可选；来自 ScriptDivider 的 ShotDivision 序列化）
     */
    shot_division?: (Record<string, any> | null);
};

