/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ShotDivision } from './ShotDivision';
import type { ShotElements } from './ShotElements';
/**
 * 单镜信息提取结果。
 */
export type ShotElementExtractionResult = {
    /**
     * 镜头序号（章节内唯一）
     */
    index: number;
    /**
     * 分镜元信息（来自 ScriptDivider 输出）
     */
    shot_division?: (ShotDivision | null);
    /**
     * 提取的元素
     */
    elements: ShotElements;
    /**
     * 提取置信度（0-1）
     */
    confidence?: (number | null);
    /**
     * 提取说明或不确定项
     */
    notes?: (string | null);
};

