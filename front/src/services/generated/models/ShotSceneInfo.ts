/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EvidenceSpan } from './EvidenceSpan';
/**
 * 单镜场景描述（弱ID/可溯源）。
 */
export type ShotSceneInfo = {
    /**
     * 场景键（可为临时ID或归一化名；合并阶段再分配稳定ID）
     */
    scene_key: string;
    /**
     * 场景名称（可选）
     */
    name?: (string | null);
    /**
     * 具体地点描述：老旧客厅、雨中街头、废弃工厂等
     */
    location_detail?: string;
    /**
     * 氛围、光线、色调、声音暗示等
     */
    atmosphere?: string;
    /**
     * 时间+天气补充（如果文本中有）
     */
    time_weather?: string;
    /**
     * 原文依据（可选）
     */
    evidence?: Array<EvidenceSpan>;
    /**
     * 场景相关的主要描述原文
     */
    raw_description_text?: string;
};

