/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EvidenceSpan } from './EvidenceSpan';
/**
 * 单镜中单个角色的提取信息（弱ID/可溯源）。
 */
export type ShotCharacterInfo = {
    /**
     * 角色键（可为临时ID或归一化名；合并阶段再分配稳定ID）
     */
    character_key: string;
    /**
     * 本镜文本中出现的写法（昵称/小名等）
     */
    name_in_text?: (string | null);
    /**
     * 外貌描述：年龄感、体型、发型、五官、疤痕、肤色等
     */
    appearance?: string;
    /**
     * 本镜服装描述：款式、颜色、材质、状态（破损、湿透、沾泥等）
     */
    clothing?: string;
    /**
     * 配饰、眼镜、帽子、首饰等
     */
    accessories?: string;
    /**
     * 本镜临时状态：情绪主导、受伤、脏污、疲惫等
     */
    state?: string;
    /**
     * 原文依据（可选）
     */
    evidence?: Array<EvidenceSpan>;
    /**
     * 导致 appearance 字段的原始剧本片段
     */
    raw_appearance_text?: string;
    /**
     * 导致 clothing 字段的原始剧本片段
     */
    raw_clothing_text?: string;
    /**
     * 导致 state 字段的原始剧本片段
     */
    raw_state_text?: string;
};

