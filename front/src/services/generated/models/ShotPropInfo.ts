/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EvidenceSpan } from './EvidenceSpan';
/**
 * 单镜中单个道具的提取信息（弱ID/可溯源）。
 */
export type ShotPropInfo = {
    /**
     * 道具键（可为临时ID或归一化名；合并阶段再分配稳定ID）
     */
    prop_key: string;
    /**
     * 本镜文本中出现的写法
     */
    name_in_text?: (string | null);
    /**
     * 外观、材质、颜色、尺寸、特殊标记等
     */
    description?: string;
    /**
     * 当前状态：全新、破损、沾血、打开/关闭等
     */
    state?: string;
    /**
     * 在本镜的使用方式：拿起、丢弃、指向、使用等
     */
    interaction?: string;
    /**
     * 原文依据（可选）
     */
    evidence?: Array<EvidenceSpan>;
    /**
     * 导致以上描述的原始文本片段
     */
    raw_text?: string;
};

